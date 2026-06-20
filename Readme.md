# 🛣️ Highway Toll Management System (API Backend)

An enterprise-grade, domain-agnostic toll management system built with Python, FastAPI, and PostgreSQL. This system handles high-throughput vehicle transit operations, automated fraud detection, and multi-gateway payment processing.

Currently configured with localized data for the **Central Expressway (Shahrah-e-Bhutto)**.

## ✨ Key Features

* **Silent Theft Interception:** Utilizes native PostgreSQL triggers to instantly cross-reference ANPR (Automatic Number Plate Recognition) camera reads with the national `excise` database. Stolen vehicles are silently flagged to the administration without physically locking down the lane, ensuring traffic continuity and safety.
* **Dual-Factor E-Tag Validation:** Prevents toll evasion (e.g., swapping passenger car tags onto commercial trucks) by cross-referencing overhead RFID scans with ANPR plate reads. Mismatches trigger a fraud alert and default the lane to a temporary QR code fallback.
* **Dynamic QR Session Tokens:** Unrecognized vehicles, low-balance accounts, or fraudulent E-Tags automatically generate a single-use, cryptographically secure QR token mapped strictly to that transit session. Tokens expire exactly 180 seconds after generation.
* **Monolithic Database / Multi-Schema Architecture:** Cleanly isolates domains (`excise`, `toll`, `payment`) within a single database instance to ensure ACID compliance without the overhead of microservices.

## 🛠️ Tech Stack

* **Framework:** FastAPI (Python)
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy 2.0
* **Data Validation:** Pydantic
* **Server:** Uvicorn

## 📂 Project Structure

```text
toll_backend_project/
│
├── .env                  # Database connection string (Environment Variables)
├── requirements.txt      # Python dependencies
├── init_db.py            # Automated SQLAlchemy schema & trigger generator
├── README.md             # Project documentation
│
└── app/                  # Core Application Module
    ├── __init__.py       
    ├── database.py       # SQLAlchemy engine & FastAPI dependency injection
    ├── models.py         # ORM mappings for PostgreSQL tables
    ├── schemas.py        # Pydantic models for request/response validation
    └── main.py           # FastAPI application and route endpoints

```

## 🚀 Setup & Installation Guide

### 1. Prerequisites

* **Python 3.9+** installed.
* **PostgreSQL (pgAdmin 4)** installed and running locally.

### 2. Install Dependencies

Open your terminal in the root directory and install the required packages:

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv pydantic

```

### 3. Environment Variables

Create a `.env` file in the root directory and add your PostgreSQL connection string. Replace `YOUR_PASSWORD` with your actual local database password:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/shahrah_toll_system

```

*(Ensure a blank database named `toll_management_system` is created in pgAdmin first).*

### 4. Initialize the Database Architecture

Run the initialization script. This will drop old data, create the `excise`, `toll`, and `payment` schemas, generate all tables via SQLAlchemy, and inject the PostgreSQL silent theft trigger.

```bash
python init_db.py

```

### 5. Inject Mock Data

Open **pgAdmin 4**, open the Query Tool for `toll_management_system`, and execute the localized DML script (provided separately) to populate the database with mock Pakistani citizens, vehicles, toll plazas, and E-Tags.

---

## 🚦 Running the Server

Start the local Uvicorn server with hot-reloading enabled:

```bash
uvicorn app.main:app --reload

```

The API will be available at: `http://127.0.0.1:8000`
The Interactive API Documentation (Swagger UI) is available at: **`http://127.0.0.1:8000/docs`**

---

## 🧪 Testing the API via Swagger UI

Navigate to the `/docs` endpoint and test the `POST /api/lane/vehicle-arrival` route using these specific JSON payloads to demonstrate core business logic:

### Test Case 1: The Perfect E-Tag Scan

Simulates a valid vehicle with a funded, matching E-Tag.

```json
{
  "lane_id": 101,
  "captured_plate": "KHI-123",
  "e_tag_id": "TAG-PK-001"
}

```

* **Expected Result:** `200 OK`. $50.00 is deducted from the balance, and the barrier opens.

### Test Case 2: Fraudulent E-Tag Mismatch

Simulates a heavy commercial truck attempting to use a passenger car's E-Tag.

```json
{
  "lane_id": 101,
  "captured_plate": "TKG-999",
  "e_tag_id": "TAG-PK-001"
}

```

* **Expected Result:** `200 OK` (Pending Payment status). The system detects the mismatch, logs a fraud alert in `toll.admin_alerts`, and falls back to generating a 180-second dynamic QR token.

### Test Case 3: Silent Stolen Vehicle Interception

Simulates a flagged stolen vehicle passing through the plaza.

```json
{
  "lane_id": 101,
  "captured_plate": "ISB-789"
}

```

* **Expected Result:** `200 OK`. The PostgreSQL trigger intercepts the transaction, logs a critical administrative alert, and instructs the application to open the barrier normally without alerting the driver.
