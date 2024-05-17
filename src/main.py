# main.py
from api import RGDealersAPI
from database import populate_database
from config import BASE_URL

def main():
    api = RGDealersAPI(BASE_URL)
    populate_database(api)

if __name__ == '__main__':
    main()