import asyncio

import requests
from pydantic import BaseModel, ValidationError


class ApiResult(BaseModel):
    regular_market_price: float


class StockData(BaseModel):
    results: list[ApiResult]


class BrApiDevRepository:

    def __init__(self, api_key):
        self.api_key = api_key

    def get_price(self, symbol: str) -> float:
        # Ensure the symbol format is valid
        symbol_w_suffix = str(symbol)

        # Retrieve the API key from an environment variable
        api_key = self.api_key
        if not api_key:
            raise ValueError("BRAPI_DEV environment variable not set")

        # Define the API URL with the symbol and API key
        url = f"https://brapi.dev/api/quote/{symbol_w_suffix}?token={api_key}"

        try:
            # Asynchronously send a GET request to the API and obtain the response body as a string
            response = requests.get(url)
            response.raise_for_status()
            regular_market_price = response.json()["results"][0]['regularMarketPrice']

            # Parse the price from the StockData and return it
            return regular_market_price
        except (requests.RequestException, ValidationError) as e:
            print(f"Error during request: {e}")
            raise


# Example usage:
async def main():
    symbol = "PETR4"  # Replace with your symbol
    repository = BrApiDevRepository()
    try:
        price = await repository.get_price(symbol)
        print(f"The price of {symbol} is {price}")
    except ValueError as ve:
        print(ve)



def test_get_price():
    asyncio.run(main())