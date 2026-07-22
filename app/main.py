from decimal import Decimal
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, timedelta
from app.schema import PaymentCallbackRequest
import uuid


# Import our database setup and models
from app.database import engine, get_db
from app.models import Passage, ETag, AdminAlert, QRToken, Transaction
from app.schema import VehicleArrivalRequest, ArrivalResponse

app = FastAPI(title="Global Toll Management System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/db-check")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "success", "database_connected": True}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.post("/api/lane/vehicle-arrival", response_model=ArrivalResponse)
def process_vehicle_arrival(request: VehicleArrivalRequest, db: Session = Depends(get_db)):
    """
    Core Logic Endpoint: Handles E-Tag Dual-Validation, Stolen Vehicle Triggers, and QR Generation.
    """
    try:
        # --- 1. CREATE THE PASSAGE RECORD ---
        new_passage = Passage(
            lane_id=request.lane_id,
            captured_plate=request.captured_plate
        )
        db.add(new_passage)
        db.commit()      # Committing triggers our PostgreSQL silent theft check!
        db.refresh(new_passage) # Pull the updated row back from PostgreSQL

        # --- 2. CHECK FOR STOLEN VEHICLE (PostgreSQL Trigger Magic) ---
        # If the DB trigger caught a stolen car, it changed the payment_method_used to 'None_Silent_Flag'
        if new_passage.payment_method_used == 'None_Silent_Flag':
            return ArrivalResponse(
                status="success",
                message="Barrier opened. (Silent alert dispatched to admin dashboard)",
                passage_id=new_passage.passage_id,
                requires_qr=False
            )

        # --- 3. DUAL-FACTOR E-TAG VALIDATION ---
        if request.e_tag_id:
            e_tag_record = db.query(ETag).filter(ETag.e_tag_id == request.e_tag_id).first()
            
            if e_tag_record:
                # Security Check: Does the tag belong to the car the camera sees?
                if e_tag_record.registered_plate != request.captured_plate:
                    # FRAUD DETECTED: Log an alert, ignore the E-Tag, fallback to QR
                    fraud_alert = AdminAlert(
                        passage_id=new_passage.passage_id,
                        alert_type="ETag_Plate_Mismatch",
                        details=f"Fraud Attempt: Tag {request.e_tag_id} does not match Plate {request.captured_plate}"
                    )
                    db.add(fraud_alert)
                    db.commit()
                
                elif e_tag_record.balance >= Decimal("50.00"): # Assuming standard toll is $50.00
                    # SUCCESS: Deduct balance and open gate
                    e_tag_record.balance -= Decimal("50.00")
                    new_passage.payment_method_used = 'E_Tag'
                    new_passage.exit_timestamp = datetime.now()
                    
                    # Log financial transaction
                    txn = Transaction(
                        passage_id=new_passage.passage_id,
                        amount_charged=Decimal("50.00"),
                        payment_gateway='Internal_ETag',
                        status='Settled'
                    )
                    db.add(txn)
                    db.commit()
                    
                    return ArrivalResponse(
                        status="success",
                        message="E-Tag Verified. Toll Deducted. Barrier Opened.",
                        passage_id=new_passage.passage_id,
                        requires_qr=False
                    )

        # --- 4. FALLBACK: GENERATE 180-SECOND DYNAMIC QR CODE ---
        # If no E-Tag, insufficient balance, or tag fraud detected, generate a QR.
        expiration_time = datetime.now() + timedelta(minutes=3)
        qr_record = QRToken(
            passage_id=new_passage.passage_id,
            expires_at=expiration_time
        )
        db.add(qr_record)
        db.commit()
        db.refresh(qr_record)

        return ArrivalResponse(
            status="pending_payment",
            message="Barrier closed. Please scan the QR code to pay.",
            passage_id=new_passage.passage_id,
            requires_qr=True,
            qr_token=qr_record.secure_token
        )

    except Exception as e:
        db.rollback() # Undo everything if a critical error occurs
        raise HTTPException(status_code=500, detail=f"Transaction failed: {str(e)}")

@app.post("/api/webhooks/payment-callback")
def payment_webhook(request: PaymentCallbackRequest, db: Session = Depends(get_db)):

    try:
        # 1. Look up the QR Token in the database
        qr_record = db.query(QRToken).filter(QRToken.secure_token == request.qr_token).first()
        
        # 2. Validation Checks
        if not qr_record:
            raise HTTPException(status_code=404, detail="Invalid QR Token.")
            
        if qr_record.status == 'Utilized':
            return {"status": "error", "message": "This QR code has already been paid."}
            
        if qr_record.expires_at < datetime.now():
            qr_record.status = 'Expired'
            db.commit()
            return {"status": "error", "message": "QR code expired. Please request a new one."}
            
        # 3. Mark Token as Paid
        qr_record.status = 'Utilized'

        gateway_mapping = {
            'Mobile': 'Mobile_Wallet_Webhook',
            'Cash': 'Manual_Cash_Collection',
            'E-Tag': 'E_Tag_Delayed_TopUp'
        }
        gateway_used = gateway_mapping.get(request.payment_method, 'Unknown_Gateway')
        
        # 4. Create the Settled Transaction in the Ledger
        txn = Transaction(
            passage_id=qr_record.passage_id,
            amount_charged=Decimal(str(request.amount_paid)),
            payment_gateway=gateway_used,
            status='Settled'
        )
        
        # 5. Update the Passage (Open the barrier!)
        passage = db.query(Passage).filter(Passage.passage_id == qr_record.passage_id).first()
        if passage:
            passage.payment_method_used = 'QR_Code'
            passage.exit_timestamp = datetime.now()
            
        db.add(txn)
        db.commit()
        
        return {
            "status": "success",
            "message": f"Payment of Rs. {request.amount_paid} received. Barrier OPENED."
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))