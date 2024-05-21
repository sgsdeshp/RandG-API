"""
This module provides an API client for the RandG Dealers API.

The API client provides methods for fetching data from the API, such as:

* All bikes
* All brands
* All categories
* Product details
* Search products

"""


from typing import Any, Dict, List
import requests
from requests.exceptions import RequestException
import backoff
from config import API_KEY

@backoff.on_exception(backoff.expo, RequestException, max_tries=5)
def fetch_data(url):
    """
    Fetches data from the RandG Dealers API.

    Args:
        url: The URL of the API endpoint.

    Returns:
        A dictionary containing the API response.

    Raises:
        RequestException: If there is an error fetching the data.
    """

    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()

class RGDealersAPI:
    """
    An API client for the RandG Dealers API.

    Args:
        base_url: The base URL of the API.
    """

    def __init__(self, base_url: str):
        """
        Initializes the API client.

        Args:
            base_url: The base URL of the API.
        """

        self.base_url = base_url

    def get_all_bikes(self) -> List[Dict[str, Any]]:
        """
        Returns a list of all bikes in the API.

        Returns:
            A list of dictionaries, each representing a bike.
        """

        endpoint = "bikes/all"
        return fetch_data(f"{self.base_url}/{endpoint}")

    def get_all_brands(self) -> List[Dict[str, Any]]:
        """
        Returns a list of all brands in the API.

        Returns:
            A list of dictionaries, each representing a brand.
        """

        endpoint = "brands/all"
        return fetch_data(f"{self.base_url}/{endpoint}")

    def get_all_categories(self) -> List[Dict[str, Any]]:
        """
        Returns a list of all categories in the API.

        Returns:
            A list of dictionaries, each representing a category.
        """

        endpoint = "categories/all"
        return fetch_data(f"{self.base_url}/{endpoint}")

    def get_product_details(self, product_id: int) -> Dict[str, Any]:
        """
        Returns the details of a specific product.

        Args:
            product_id: The ID of the product.

        Returns:
            A dictionary containing the product details.
        """

        endpoint = f"product/get/{product_id}?includeExtendedProperties=true"
        return fetch_data(f"{self.base_url}/{endpoint}")

    def search_products(self) -> List[Dict[str, Any]]:
        """
        Searches for products based on a given query.

        Returns:
            A list of dictionaries, each representing a product.
        """

        endpoint = "product/search"
        return fetch_data(f"{self.base_url}/{endpoint}")
