# database.py
from sqlalchemy.orm import sessionmaker
from models import engine, Category, Product, AdditionalField, Make, Model, Year, ProductSummary
from datetime import datetime
import logging
from concurrent.futures import ThreadPoolExecutor

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a session factory
Session = sessionmaker(bind=engine)

def insert_data(data):
    session = Session()
    try:
        # Insert category
        category_data = data['category']
        category = Category(
            id=category_data['id'],
            name=category_data['name'],
            description=category_data.get('description'),
            product_description=category_data.get('productDescription'),
            image=category_data['image'],
            banner_image=category_data.get('bannerImage')
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
            brief_description=data.get('briefDescription'),
            full_description=data.get('fullDescription'),
            fitting_instructions=data['fittingInstructions'],
            fitting_instructions_qr=data['fittingInstructionsQR'],
            coversheet=data['coversheet'],
            date_created=datetime.fromisoformat(data['dateCreated']),
            date_modified=datetime.fromisoformat(data['dateModified']),
            ean=data['ean'],
            site_price=data['sitePrice'],
            dealer_price_gbp=data.get('dealerPriceGBP'),
            dealer_price_usd=data.get('dealerPriceUSD'),
            dealer_price_eur=data.get('dealerPriceEUR')
        )
        session.merge(product)

        # Insert product summary
        product_summary = ProductSummary(
            id=data['id'],
            sku=data['sku'],
            date_created=datetime.fromisoformat(data['dateCreated']),
            date_modified=datetime.fromisoformat(data['dateModified']),
            site_price=data['sitePrice']
        )
        session.merge(product_summary)

        # Insert additional fields
        for field in data['additionalFields']:
            additional_field = AdditionalField(
                product_id=product.id,
                name=field['name'],
                value=field['value']
            )
            session.merge(additional_field)

        # Insert makes (bikes), models, and years
        for make_data in data['bikes']:
            make = Make(
                id=make_data['id'],
                name=make_data['name'],
                image=make_data['image']
            )
            session.merge(make)
            
            for model_data in make_data['models']:
                model = Model(
                    id=model_data['id'],
                    name=model_data['name'],
                    make_id=make.id,
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
    except Exception as e:
        logging.error(f"Error inserting data: {e}")
        session.rollback()
    finally:
        session.close()

def insert_product_data(api, product):
    sku = product['sku']
    data = api.get_product_details(sku)
    insert_data(data)

def populate_database(api):
    all_products = api.search_products()

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(insert_product_data, api, product) for product in all_products]

        for future in futures:
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error processing data: {e}")

    logging.info("Data inserted successfully.")
