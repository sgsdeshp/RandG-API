import json
import os
import requests
import pandas as pd
from typing import Any, Dict, List, Union
import os
from dotenv import load_dotenv
import time
import gspread
from sqlalchemy import create_engine, Column, Integer, String, Text, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
from main import RGDealersAPI


sa = gspread.service_account(filename=os.environ.get('PMGCPKEY'))

load_dotenv()

API_KEY = os.getenv('api_key')
BASE_URL = "https://dealers.api.rg-racing.com"


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

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    product_description = Column(Text)
    image = Column(String(255))
    banner_image = Column(String(255))

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    sku = Column(String(255))
    name = Column(String(255))
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category")
    product_type = Column(String(255))
    brand = Column(String(255))
    brief_description = Column(Text)
    full_description = Column(Text)
    fitting_instructions = Column(String(255))
    fitting_instructions_qr = Column(String(255))
    coversheet = Column(String(255))
    date_created = Column(TIMESTAMP)
    date_modified = Column(TIMESTAMP)
    ean = Column(String(255))
    site_price = Column(Numeric)
    dealer_price_gbp = Column(Numeric)
    dealer_price_usd = Column(Numeric)
    dealer_price_eur = Column(Numeric)

class AdditionalField(Base):
    __tablename__ = 'additional_fields'
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    name = Column(String(255), primary_key=True)
    value = Column(String(255))

class Bike(Base):
    __tablename__ = 'bikes'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    image = Column(String(255))

class Model(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    bike_id = Column(Integer, ForeignKey('bikes.id'))
    bike = relationship("Bike")
    image = Column(String(255))

class Year(Base):
    __tablename__ = 'years'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    model_id = Column(Integer, ForeignKey('models.id'))
    model = relationship("Model")
    mic = Column(String(255))
    image = Column(String(255))

# Create tables
Base.metadata.create_all(engine)

# Insert data into tables
def insert_data(data):
    # Insert category
    category_data = data['category']
    category = Category(
        id=category_data['id'],
        name=category_data['name'],
        description=category_data['description'],
        product_description=category_data['productDescription'],
        image=category_data['image'],
        banner_image=category_data['bannerImage']
    )
    session.merge(category)
    
    # Insert product
    product = Product(
        id=data['id'],
        sku=data['sku'],
        name=data['name'],
        category_id=category.id,
        product_type=data['productType'],
        brand=data['brand'],
        brief_description=data['briefDescription'],
        full_description=data['fullDescription'],
        fitting_instructions=data['fittingInstructions'],
        fitting_instructions_qr=data['fittingInstructionsQR'],
        coversheet=data['coversheet'],
        date_created=datetime.fromisoformat(data['dateCreated']),
        date_modified=datetime.fromisoformat(data['dateModified']),
        ean=data['ean'],
        site_price=data['sitePrice'],
        dealer_price_gbp=data['dealerPriceGBP'],
        dealer_price_usd=data['dealerPriceUSD'],
        dealer_price_eur=data['dealerPriceEUR']
    )
    session.merge(product)

    # Insert additional fields
    for field in data['additionalFields']:
        additional_field = AdditionalField(
            product_id=product.id,
            name=field['name'],
            value=field['value']
        )
        session.merge(additional_field)

    # Insert bikes, models, and years
    for bike_data in data['bikes']:
        bike = Bike(
            id=bike_data['id'],
            name=bike_data['name'],
            image=bike_data['image']
        )
        session.merge(bike)
        
        for model_data in bike_data['models']:
            model = Model(
                id=model_data['id'],
                name=model_data['name'],
                bike_id=bike.id,
                image=model_data['image']
            )
            session.merge(model)
            
            for year_data in model_data['years']:
                year = Year(
                    id=year_data['id'],
                    name=year_data['name'],
                    model_id=model.id,
                    mic=year_data['mic'],
                    image=year_data.get('image')
                )
                session.merge(year)

    session.commit()

if __name__ == '__main__':
    api = RGDealersAPI(API_KEY, BASE_URL)
    all_products = api.search_products()
    for i, product in enumerate(all_products):
        print(i, product['sku'])
        data = api.get_product_details(product['sku'])
        # Insert data
        insert_data(data)

    # Close the session
    session.close()

    print("Data inserted successfully.")
