# models.py
from sqlalchemy import create_engine, Column, Integer, String, Text, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship
from config import DATABASE_URL

# Connect to the database
engine = create_engine(DATABASE_URL)
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

class Make(Base):
    __tablename__ = 'makes'
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