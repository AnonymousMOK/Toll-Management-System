```markdown
# 🛣️ Highway Toll Management System (Full-Stack Prototype)

An enterprise-grade, domain-agnostic toll management system built with Python, FastAPI, and PostgreSQL. This system handles high-throughput vehicle transit operations, automated fraud detection, and multi-gateway payment processing. 

Currently configured with localized data and UI interfaces for the **Central Expressway (Shahrah-e-Bhutto)**.

---

## ✨ Key Features

* **Silent Theft Interception (PostgreSQL Triggers):** Utilizes native database triggers (`BEFORE INSERT`) to instantly cross-reference ANPR (Automatic Number Plate Recognition) camera reads with the national `excise` database. Stolen vehicles are silently flagged to the administration, opening the barrier to avoid traffic bottlenecks and suspect alertness.
* **Dual-Factor E-Tag Validation:** Prevents toll evasion (e.g., swapping passenger car tags onto commercial trucks) by cross-referencing overhead RFID scans with ANPR plate reads. Mismatches trigger a fraud alert and default the lane to a temporary QR code fallback.
* **Dynamic QR Session Tokens:** Unrecognized vehicles, low-balance accounts, or fraudulent E-Tags automatically generate a single-use, cryptographically secure QR token mapped strictly to that transit session (expires exactly 180 seconds after generation).
* **Multi-Gateway Settlement:** Dedicated webhook endpoints elegantly handle payments from distinct physical and digital gateways (`Mobile` app wallets, physical `Cash` insertion, or `E-Tag` top-ups).
* **Role-Specific UI Dashboards:** Includes standalone HTML/JS frontends (Driver Kiosk, Operator Dashboard, Analytics Infographic) that connect directly to the FastAPI backend via the Fetch API.

---

## 🛠️ Tech Stack

* **Backend Framework:** FastAPI (Python 3.9+)
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy 2.0
* **Data Validation:** Pydantic
* **Server:** Uvicorn
* **Frontend Dashboards:** Vanilla HTML5, JavaScript (Fetch API), Tailwind CSS (CDN), Chart.js

---

## 📂 Project Structure

```text
toll_management_system/
│
├── .env                        # Database connection string
├── requirements.txt            # Python dependencies
├── init_db.py                  # Automated SQLAlchemy schema & trigger generator
├── Data.sql                    # SQL Script to seed mock citizens, vehicles, and tags
├── swagger_test_suite.csv      # SQA test vectors for API validation
│
├── Standalone UIs/             # Frontend Prototypes (Double-click to run)
│   ├── index.html              # Executive Analytics & Presentation Infographic
│   ├── driverKiosk.html        # Automated Driver-Facing Kiosk UI
│   ├── standalone_kiosk.html   # Offline Simulated Kiosk (No backend needed)
│   └── operator_dashboard.html # Manual Lane Operator Terminal UI
│
└── app/                        # Core Backend Application
    ├── __init__.py       
    ├── database.py             # SQLAlchemy engine & FastAPI dependency injection
    ├── models.py               # ORM mappings (3NF across 3 Schemas)
    ├── schema.py               # Pydantic models for request/response validation
    └── main.py                 # FastAPI application and route endpoints

```

---

## 🚀 Setup & Installation Guide

### 1. Prerequisites

* **Python 3.9+** installed on your system.
* **PostgreSQL (pgAdmin 4)** installed and running locally.

### 2. Install Python Dependencies

Open your terminal in the root directory and install the required packages:

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv pydantic

```

### 3. Configure Environment Variables

Create or verify the `.env` file in your root directory. Make sure a blank database named `central_toll_system` is created inside pgAdmin first:

```env
DATABASE_URL=postgresql://postgres:mokpost@localhost:5432/central_toll_system

```

### 4. Initialize Database Architecture

Run the automated bootstrapping script. This will construct the isolated `excise`, `toll`, and `payment` schemas, generate all SQL tables via SQLAlchemy, and inject the PostgreSQL silent theft interception trigger:

```bash
python init_db.py

```

### 5. Inject Mock Ground-Truth Data

Open **pgAdmin 4**, open the Query Tool for `central_toll_system`, and execute the contents of `Data.sql` to populate the ledger with test citizen profiles, registered vehicles, toll plazas, and varying E-Tag balance states.

---

## 🚦 Running the System

### Step 1: Start the Fast API Backend Server

Launch the local Uvicorn server with hot-reloading enabled. The built-in CORS middleware allows local HTML files to communicate with the endpoints effortlessly:

```bash
uvicorn app.main:app --reload

```

* **Live API Base:** `http://127.0.0.1:8000`
* **Interactive Swagger UI:** `http://127.0.0.1:8000/docs`

### Step 2: Launch the Frontend Interfaces

No Node.js configuration or separate web server is required. Simply double-click any of the HTML files in your file explorer to open them instantly in any browser:

* **`driverKiosk.html`**: Simulates the automated smart toll lane. Use the bottom presenter panel to simulate vehicle arrivals (`KHI-123`, `LHR-456`, `ISB-789`).
* **`operator_dashboard.html`**: Simulates a hybrid/manual booth worker's touch terminal.
* **`index.html`**: Displays executive throughput analytics, KPI metrics, and system flow visualizers.
* **`standalone_kiosk.html`**: An offline-only presentation fallback that simulates all network delays and visual states entirely in the browser.

---

## 🧪 SQA Testing & Validation Matrix

When demonstrating the live API via Swagger UI (`http://127.0.0.1:8000/docs`), use the test vectors from `swagger_test_suite.csv` to verify core operational logic:

### Scenario 1: Automated E-Tag Transit (Success)

* **Endpoint:** `POST /api/lane/vehicle-arrival`
* **PayloadBody:**

```json
{
  "lane_id": 101,
  "captured_plate": "KHI-881",
  "e_tag_id": "TAG-PK-101"
}

```

* **System Response:** `200 OK`. Deducts Rs. 50.00 from the tag balance, logs a settled transaction, and signals the physical barrier to open.

### Scenario 2: Insufficient Funds Fallback

* **Endpoint:** `POST /api/lane/vehicle-arrival`
* **PayloadBody:**

```json
{
  "lane_id": 101,
  "captured_plate": "ISB-505",
  "e_tag_id": "TAG-PK-103"
}

```

* **System Response:** `200 OK` (`pending_payment`). Detects low balance (Rs. 15.00), aborts the deduction, and generates a secure 180-second `qr_token`.

### Scenario 3: Silent Police Interception (Stolen Car holding Valid Tag)

* **Endpoint:** `POST /api/lane/vehicle-arrival`
* **PayloadBody:**

```json
{
  "lane_id": 101,
  "captured_plate": "FSD-808",
  "e_tag_id": "TAG-PK-110"
}

```

* **System Response:** `200 OK`. Queries the security registry first, identifies the vehicle as stolen, ignores the active tag balance entirely, and triggers silent barrier opening while logging an active law enforcement dispatch flag.

### Scenario 4: Multi-Gateway Webhook Settlement

Once a QR token is generated for an un-tagged vehicle, copy the returned `"qr_token"` string and test the settlement webhook:

* **Endpoint:** `POST /api/webhooks/payment-callback`
* **PayloadBody:**

```json
{
  "qr_token": "PASTE_THE_COPIED_TOKEN_HERE",
  "amount_paid": 50.00,
  "payment_method": "Mobile"
}

```

* **System Response:** `200 OK`. Validates token freshness, logs the transaction against the specified gateway (`Mobile`, `Cash`, or `E-Tag`), marks the session as settled, and issues the barrier open signal.

```

```
