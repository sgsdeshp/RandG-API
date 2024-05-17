import requests
import pandas as pd
from typing import Any, Dict, List, Union
import os
from dotenv import load_dotenv
import time
import gspread


sa = gspread.service_account(filename=os.environ.get('PMGCPKEY'))

load_dotenv()

API_KEY = os.getenv('api_key')
BASE_URL = "https://dealers.api.rg-racing.com"

def sh_write(df, wbook, wsheet):
    # establish connection
    sh = sa.open(wbook)
    wks = sh.worksheet(wsheet)
    wks.clear()
    # writing to sheet
    wks.update([df.columns.values.tolist()] + df.values.tolist(), raw=False)
    
class RGDealersAPI:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
        }

    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_all_bikes(self) -> List[Dict[str, Any]]:
        endpoint = "bikes/all"
        return self._make_request(endpoint)

    def get_all_brands(self) -> List[Dict[str, Any]]:
        endpoint = "brands/all"
        return self._make_request(endpoint)

    def get_all_categories(self) -> List[Dict[str, Any]]:
        endpoint = "categories/all"
        return self._make_request(endpoint)

    def get_product_details(self, product_id: int) -> Dict[str, Any]:
        endpoint = f"product/get/{product_id}?includeExtendedProperties=true"
        return self._make_request(endpoint)

    def search_products(self) -> List[Dict[str, Any]]:
        endpoint = "product/search"

        return self._make_request(endpoint)
    
if __name__ == '__main__':
    # Create an instance of the RGDealersAPI class
    api = RGDealersAPI(API_KEY, BASE_URL)
    """
    # Retrieve all bikes 
    all_bikes = api.get_all_bikes()
    # Normalize the JSON to flatten the 'models' and 'years' structure
    df = pd.json_normalize(
        all_bikes, 
        record_path=['models', 'years'],
        meta=[
            'id',
            'name',
            'image',
            ['models', 'id'],
            ['models', 'name'],
            ['models', 'image']
        ],
        record_prefix='year_',
        meta_prefix='make_',
        errors='ignore'
    )

    # Renaming the columns to more readable names
    df.columns = df.columns.str.replace('make_', 'make_', regex=False).str.replace('models_', 'model_', regex=False)
    # Fill missing values with empty strings
    df = df.fillna('')
    sh_write(df, 'RandG', 'Bikes')
    

    
    # Retrieve all brands
    all_brands = api.get_all_brands()
    print("\nAll Brands:")
    print(all_brands)
    df = pd.json_normalize(all_brands)
    df = df.fillna('')
    sh_write(df, 'RandG', 'Brands')
    """
    # Retrieve all categories
    all_categories = api.get_all_categories()
    print("\nAll Categories:")
    df = pd.json_normalize(all_categories)
    df = df.fillna('')
    sh_write(df, 'RandG', 'Categories')
    
    
    product_details = api.get_product_details("CP0546BL")
    print("\nProduct Details:")
    print(product_details)
    df = pd.json_normalize(product_details)
    df = df.fillna('')
    #print(df)
    
    """
    print("\nProduct Details:")
    df = pd.DataFrame()
    #print(product_details)
    for item in all_categories:
        print(item['name'])
        try:
            search_results = api.search_products(item['name'])

            df1 = pd.DataFrame(search_results)
            df = pd.concat([df, df1], ignore_index=True, axis=0)
            
        except Exception as e:
            print(f"Error occurred: {item['name']}")
        time.sleep(2)
    
    # dropping ALL duplicate values
    df.drop_duplicates(subset="sku", keep='first', inplace=True)
    # Specify the file path where you want to save the Excel file
    file_path = "C:\\Users\\hello\\Desktop\\PM Projects\\RandG\\product_details.xlsx"
    # Save the DataFrame to an Excel file
    df.to_excel(file_path, index=False)
    print("\nSearch Results:")
    
    #print(search_results)
    

    df = pd.read_excel("R&G_product_details.xlsx")
    pd_df = pd.DataFrame()
    for item in df['sku']:
        print(item)
        try:
            product_details = api.get_product_details(item)
            pd_df1 = pd.DataFrame(product_details)
            pd_df = pd.concat([pd_df, pd_df1], ignore_index=True, axis=0)
            
        except Exception as e:
            print(f"Error occurred: {e}")
           
    # Specify the file path where you want to save the Excel file
    file_path = "C:\\Users\\hello\\Desktop\\PM Projects\\RandG\\product_details.xlsx"
    # Save the DataFrame to an Excel file
    pd_df.to_excel(file_path, index=False)
    """