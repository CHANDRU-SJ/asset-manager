import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env once
load_dotenv()

# Database settings
DATABASE_URL = os.getenv("DATABASE_URL")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

# Reports directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent
REPORTS_DIR = Path(os.getenv("REPORTS_DIR", BASE_DIR / "reports"))
REPORTS_DIR.mkdir(exist_ok=True)

# PDF settings
PDF_TITLE = os.getenv("PDF_TITLE", "Assets Report")
