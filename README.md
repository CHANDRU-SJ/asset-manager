# 🧾 Asset Manager API

A **FastAPI-based** backend service for managing assets, generating PDF reports, and executing background tasks asynchronously.  
Built with **async SQLAlchemy**, **ReportLab**, and **PyPDF2** for efficient and non-blocking performance.

---

## 🚀 Features

- ⚡ **Asynchronous** database operations using SQLAlchemy Async  
- 🧱 **CRUD APIs** for asset management  
- 📄 **PDF report generation** with ReportLab + PyPDF2  
- 🧰 **Background tasks** for non-blocking PDF creation  
- 🌱 **Environment variable management** using `.env`  
- ✅ **Clean architecture** (models, CRUD, routes, utils separation)

---

## 🗂️ Project Structure

```
asset_manager/
│
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic models
│   ├── database.py          # Async database engine and session
│   ├── crud.py              # CRUD operations
│   ├── routes/
│   │   └── assets.py        # Asset API endpoints
│   ├── utils/
│   │   ├── config.py        # Loads .env variables
│   │   └── pdf_generator.py # Generic PDF generation utility
│   ├── tests/               # Unit / integration tests
│   │   ├── test_assets_api.py   # Tests for asset CRUD endpoints
│   │   ├── test_pdf_report.py      # Tests for PDF generation utilities
│   │   └── conftest.py      # Pytest fixtures (DB session, test client, etc.)
│   └── __init__.py
│
├── reports/                 # Generated PDF files (outside the app folder)
├── database.sql             # database schema
├── AssetManager.postman_collection.json # postman collection
├── .env                     # Environment configuration
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```
git clone https://github.com/CHANDRU-SJ/asset-manager.git
cd asset-manager
```
### 2️⃣ Setup environment

Using Pipenv (recommended):
```
pipenv install
pipenv shell
```

Or using venv:
```
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows
pip install -r requirements.txt
```

### Database Setup
- Create the database (if not exists):
```
mysql -u {username} -p -e "CREATE DATABASE {db name};"
```
    You will be prompted to enter your password {password}.

- Import the schema:

`mysql -u {username} -p {db name} < database.sql`

     {username} → your MySQL username
     {password} → your MySQL password (you’ll be prompted interactively)

- database.sql
```
CREATE TABLE assets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    purchase_date DATE NOT NULL,
    serial_number VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 🔑 Environment Configuration

Create a `.env` file in the project root:
```
.env
# -------------------------------
# Database configuration
# -------------------------------
DATABASE_URL=mysql+aiomysql://{username}:{password}@{host}:{port}/{db_name}
TEST_DATABASE_URL=mysql+aiomysql://{username}:{password}@{host}:{port}/{db_name}

# -------------------------------
# Reports directory
# -------------------------------
# REPORTS_DIR=./reports

# -------------------------------
# PDF report settings
# -------------------------------
PDF_TITLE=Assets Report
```

### Run
`uvicorn app.main:app --reload`


**API available at:**  
`👉 http://127.0.0.1:8000`

**Interactive docs:**  
📘 Swagger UI → `http://127.0.0.1:8000/docs`  
📗 ReDoc → `http://127.0.0.1:8000/redoc`

---

## 📚 API Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| POST   | /assets/ | Create a new asset |
| GET    | /assets/ | List all assets |
| GET    | /assets/{id} | Retrieve asset by ID |
| PUT    | /assets/{id} | Update asset details |
| DELETE | /assets/{id} | Delete an asset |
| GET    | /assets/report/pdf | Generate a PDF report of all assets (runs in background) |

---

## 📄 PDF Reports

PDF generation runs **asynchronously** in a background task.  
Reports are stored in the `/reports` directory.

Filenames include timestamps, e.g.:

`reports/assets_report_20251025T183045.pdf`


**Example response:**
```
{
"message": "Report generation started",
"file_path": "reports/assets_report_20251025T183045.pdf"
}
```
---

### API Testing (Postman)

- Open Postman.
- Import the provided Postman collection (`AssetManager.postman_collection.json`).

- Update the environment variable for base_url:
`http://127.0.0.1:8000`

You can now test APIs like:
```
GET /assets → List all assets
POST /assets → Create a new asset
GET /assets → Get an asset
PUT /assets/{id} → Update an asset
DELETE /assets/{id} → Delete an asset
GET /assets/report/pdf -> Generate PDF report
```
---
## 🧠 Design Highlights

✅ Async DB queries for scalability  
✅ Background task to avoid blocking API responses  
✅ Centralized config loader (`utils/config.py`)  
✅ Generic and reusable PDF generator (`utils/pdf_generator.py`)  
✅ Uses `Path` from `pathlib` for cross-platform file safety

---

## 🧪 Running Tests

`pytest app/tests -v`

---

## 🧰 Tech Stack

| Component | Technology |
|-----------|-------------|
| Framework | FastAPI |
| ORM | SQLAlchemy (Async) |
| Database | PostgreSQL |
| Task Handling | BackgroundTasks |
| PDF Generation | ReportLab + PyPDF2 |
| Environment Config | python-dotenv |
| Validation | Pydantic |

---

## 📦 Deployment

Run in production using **Uvicorn**:

`uvicorn app.main:app --host 0.0.0.0 --port 8000`
