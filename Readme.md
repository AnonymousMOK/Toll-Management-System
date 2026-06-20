 Highway Toll Management System (Full-Stack Prototype)

An enterprise-grade, domain-agnostic toll management system built with Python, FastAPI, and PostgreSQL. This system handles high-throughput vehicle transit operations, automated fraud detection, and multi-gateway payment processing.

Currently configured with localized data and UI interfaces for the Central Expressway (Shahrah-e-Bhutto).

 Key Features

Silent Theft Interception (PostgreSQL Triggers): Utilizes native database triggers (BEFORE INSERT) to instantly cross-reference ANPR (Automatic Number Plate Recognition) camera reads with the national excise database. Stolen vehicles are silently flagged to the administration, opening the barrier to avoid traffic bottlenecks and suspect alertness.

Dual-Factor E-Tag Validation: Prevents toll evasion (e.g., swapping passenger car tags onto commercial trucks) by cross-referencing overhead RFID scans with ANPR plate reads. Mismatches trigger a fraud alert and default the lane to a temporary QR code fallback.

Dynamic QR Session Tokens: Unrecognized vehicles, low-balance accounts, or fraudulent E-Tags automatically generate a single-use, cryptographically secure QR token mapped strictly to that transit session (expires in 180 seconds).

Multi-Gateway Settlement: Dedicated webhook endpoints elegantly handle payments from different physical and digital gateways (Mobile Wallets, Cash Insertions, or E-Tag Top-ups).

Role-Specific UI Dashboards: Includes three distinct vanilla HTML/JS frontends (Driver Kiosk, Operator Dashboard, Analytics Infographic) that connect directly to the FastAPI backend.

 Tech Stack

Backend Framework: FastAPI (Python 3.9+)

Database: PostgreSQL (pgAdmin 4)

ORM: SQLAlchemy 2.0

Data Validation: Pydantic

Server: Uvicorn

Frontend: Vanilla HTML5, JavaScript (Fetch API), Tailwind CSS (CDN), Chart.js

📂 Project Structure

toll_management_system/
│
├── .env                        # Database connection string
├── requirements.txt            # Python dependencies
├── init_db.py                  # Automated SQLAlchemy schema & trigger generator
├── Data.sql                    # SQL Script to seed mock citizens, vehicles, and tags
├── swagger_test_suite.csv      # Test vectors for Swagger/Postman API validation
│
├── Frontend Interfaces/        # Standalone UIs (Double-click to run)
│   ├── index.html              # High-level Analytics & Presentation Infographic
│   ├── driverKiosk.html        # Automated Driver-Facing Kiosk UI
│   └── operator_dashboard.html # Manual Lane Operator Terminal UI
│
└── app/                        # Core Backend Application
    ├── __init__.py       
    ├── database.py             # SQLAlchemy engine & FastAPI dependency injection
    ├── models.py               # ORM mappings (3NF across 3 Schemas)
    ├── schema.py               # Pydantic models for request/response validation
    └── main.py                 # FastAPI application and route endpoints


 Setup & Installation Guide

1. Prerequisites

Python 3.9+ installed.

PostgreSQL (pgAdmin 4) installed and running locally.

2. Install Dependencies

Open your terminal in the root directory and install the required packages:

pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv pydantic


3. Environment Variables

Ensure the .env file in your root directory contains your active PostgreSQL connection string. Create a blank database named central_toll_system in pgAdmin.

DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/central_toll_system


4. Initialize the Database Architecture

Run the initialization script to drop old data, create the excise, toll, and payment schemas, generate tables, and inject the PostgreSQL silent theft trigger.

python init_db.py


5. Inject Mock Data

Open pgAdmin 4, open the Query Tool for your database, and execute the Data.sql script to populate the database with mock Pakistani citizens, vehicles, toll plazas, and varying E-Tag financial states.

 Running the System

Step 1: Start the Backend Server

Start the local Uvicorn server with hot-reloading enabled. The CORS middleware allows the local HTML files to communicate with it.

uvicorn app.main:app --reload


API Base URL: http://127.0.0.1:8000

Swagger API Docs: http://127.0.0.1:8000/docs

Step 2: Launch the Frontend UIs

No Node.js or web server is required for the frontend. Simply double-click any of the HTML files to open them in your browser:

Open driverKiosk.html to simulate the automated lane experience. Use the presenter buttons at the bottom to trigger Backend calls.

Open operator_dashboard.html to simulate a manual booth worker's interface.

Open index.html to view the live executive dashboard and system architecture.

 Testing & Validation

Automated Testing (Swagger UI)

Navigate to http://127.0.0.1:8000/docs. You can reference the swagger_test_suite.csv file included in the repository for a complete matrix of exact JSON payloads to test edge cases.

Example Scenario 1: Silent Stolen Vehicle Interception

{
  "lane_id": 101,
  "captured_plate": "ISB-789"
}


Result: The DB trigger intercepts the transaction, logs a critical administrative alert, and instructs the application to open the barrier normally without alerting the driver.

Example Scenario 2: Webhook Payment Callback When a QR code is generated for a driver with no E-Tag, copy the returned qr_token and use the /api/webhooks/payment-callback endpoint to simulate a mobile payment:

{
  "qr_token": "PASTE_TOKEN_HERE",
  "amount_paid": 50.00,
  "payment_method": "Mobile"
}


Result: Updates the token state to 'Utilized', commits the transaction to the ledger, and signals the lane barrier to open.
