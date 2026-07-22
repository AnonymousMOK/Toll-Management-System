from sqlalchemy import text
from app.database import engine, Base

# IMPORTANT: You must import your models here so SQLAlchemy knows they exist
# If you don't import them, Base.metadata.create_all() won't see any tables to build.
import app.models

def initialize_database():
    print("1. Creating database schemas...")
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS excise;"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS toll;"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS payment;"))
        conn.commit()
    print("Schemas verified.")

    print("2. Generating tables from SQLAlchemy models...")
    # This reads app/models.py and builds the tables in Postgres
    Base.metadata.create_all(bind=engine)
    print("Tables generated successfully.")

    print("3. Injecting PostgreSQL Triggers for Silent Theft Detection...")
    with engine.connect() as conn:
        # Create the trigger function
        conn.execute(text("""
            CREATE OR REPLACE FUNCTION toll.check_vehicle_theft()
            RETURNS TRIGGER AS $$
            BEGIN
                IF EXISTS (SELECT 1 FROM excise.vehicles WHERE plate_number = NEW.captured_plate AND status = 'Stolen') THEN
                    -- ADD gen_random_uuid() HERE
                    INSERT INTO toll.admin_alerts (alert_id, passage_id, alert_type, details)
                    VALUES (gen_random_uuid(), NEW.passage_id, 'Stolen_Vehicle_Detected', 'CRITICAL: Stolen vehicle plate ' || NEW.captured_plate || ' detected at toll barrier.');
                    NEW.payment_method_used := 'None_Silent_Flag';
                END IF;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """))        
        # Attach the trigger to the passages table
        conn.execute(text("DROP TRIGGER IF EXISTS trg_silent_theft_detect ON toll.passages;"))
        conn.execute(text("""
            CREATE TRIGGER trg_silent_theft_detect
            BEFORE INSERT ON toll.passages
            FOR EACH ROW EXECUTE FUNCTION toll.check_vehicle_theft();
        """))
        conn.commit()
    print("Triggers active. Database initialization complete!")

if __name__ == "__main__":
    initialize_database()