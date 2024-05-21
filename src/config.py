"""# Configuration file for the RandG API."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API and database configuration
API_KEY = os.environ.get('api_key')
BASE_URL = "https://dealers.api.rg-racing.com"
DB_HOST = os.environ.get("INSTANCE_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

# Google Sheets credentials
GOOGLE_SHEETS_CREDENTIALS = os.environ.get('PMGCPKEY')

# Database connection string
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"