import json
import os
from sqlalchemy import create_engine, Column, Integer, String, Numeric, TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from main import RGDealersAPI
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('api_key')
BASE_URL = "https://dealers.api.rg-racing.com"

# Load the JSON file
with open('sampleexten.json') as f:
    data = json.load(f)

# Database connection details
DB_HOST = os.environ.get("INSTANCE_HOST")
DB_NAME = "randg"
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

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

# Insert data into tables
def insert_data(data):
    # Insert product
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
    api = RGDealersAPI(API_KEY, BASE_URL)
    # Retrieve all bikes 
    all_products = api.search_products()
    for data in all_products:
        # Insert data
        insert_data(data)

    # Close the session
    session.close()

    print("Data inserted successfully.")
