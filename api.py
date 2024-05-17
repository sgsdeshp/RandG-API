import json
import os
from sqlalchemy import create_engine, Column, Integer, String, Numeric, TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = "https://dealers.api.rg-racing.com"

# Database connection details
DB_HOST = os.getenv("INSTANCE_HOST")
DB_NAME = "randg"
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

# Connect to the database
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Define the models
Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    sku = Column(String(255))
    date_created = Column(TIMESTAMP)
    date_modified = Column(TIMESTAMP)
    ean = Column(String(255))
    site_price = Column(Numeric)

# Create tables
Base.metadata.create_all(engine)

def fetch_data_from_api(api_key, base_url):
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get(f"{base_url}/products", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

# Insert data into tables
def insert_data(data):
    product = Product(
        id=data['id'],
        sku=data['sku'],
        date_created=datetime.fromisoformat(data['dateCreated']),
        date_modified=datetime.fromisoformat(data['dateModified']),
        ean=data['ean'],
        site_price=data['sitePrice']
    )
    session.merge(product)
    session.commit()

if __name__ == '__main__':
    try:
        # Fetch data from API
        all_products = fetch_data_from_api(API_KEY, BASE_URL)
        
        # Insert each product into the database
        for data in all_products:
            insert_data(data)

        print("Data inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the session
        session.close()
