# api.py
import requests
from requests.exceptions import RequestException
import backoff
from config import API_KEY, BASE_URL

# Backoff strategy
@backoff.on_exception(backoff.expo, RequestException, max_tries=5)
def fetch_data(url):
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

class RGDealersAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_all_bikes(self):
        endpoint = "bikes/all"
        return fetch_data(f"{self.base_url}/{endpoint}")

    def get_all_brands(self):
        endpoint = "brands/all"
        return fetch_data(f"{self.base_url}/{endpoint}")

    def get_all_categories(self):
        endpoint = "categories/all"
        return fetch_data(f"{self.base_url}/{endpoint}")

    def get_product_details(self, product_id):
        endpoint = f"product/get/{product_id}?includeExtendedProperties=true"
        return fetch_data(f"{self.base_url}/{endpoint}")

    def search_products(self):
        endpoint = "product/search"
        return fetch_data(f"{self.base_url}/{endpoint}")