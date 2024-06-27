# price_scraper.py
"""
This module scrapes financial data from investing.com.
It provides functions to fetch the current price of the Nasdaq 100 index or whatever investing.com url is input
"""

import requests
from bs4 import BeautifulSoup
import json

def scrape_prices(urls=None):
    """
    Scrape financial data from specified URLs.

    This function sends requests to the given URLs (or a default URL for the Nasdaq 100),
    parses the HTML content, and extracts the company name and current price.

    Args:
        urls (list of str, optional): List of URLs to scrape. If None, defaults to ['https://www.investing.com/indices/nq-100'].

    Returns:
        dict: A dictionary where keys are company names and values are dictionaries containing 'company' and 'price'.
              For example: {'Nasdaq 100 (NDX)': {'company': 'Nasdaq 100 (NDX)', 'price': '20,000.00'}}

    Raises:
        requests.RequestException: If there's an error fetching data from a URL.
        AttributeError: If there's an error parsing data from the fetched content.
    """
  
    if urls is None:
        urls = [
            'https://www.investing.com/indices/nq-100'
        ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    data_hashmap = {}

    for url in urls:
        try:
            page = requests.get(url, headers=headers)
            page.raise_for_status()  # Raise an exception for bad status codes
            soup = BeautifulSoup(page.content, 'html.parser')

            # grabs company name
            company_element = soup.find('h1', class_='mb-2.5 text-left text-xl font-bold leading-7 text-[#232526] md:mb-2 md:text-3xl md:leading-8 rtl:soft-ltr')
            company = company_element.text.strip() if company_element else "N/A"

            # grabs price
            price_element = soup.find('div', class_='text-5xl/9 font-bold text-[#232526] md:text-[42px] md:leading-[60px]', attrs={"data-test": "instrument-price-last"})
            price = price_element.text.strip() if price_element else "N/A"

            # store in hashmap
            data_hashmap[company] = {
                "company": company,
                "price": price
            }

        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
        except AttributeError as e:
            print(f"Error parsing data from {url}: {e}")

    # if no url returns: 
    # {'Nasdaq 100 (NDX)': {'company': 'Nasdaq 100 (NDX)', 'price': '20,000.00'}}
    return data_hashmap

def ndx_price():
    """
    Fetch the current price of the Nasdaq 100 index.

    This function calls scrape_prices() to get Nasdaq 100 price

    Returns:
        str: The current price of the Nasdaq 100 index as a string.
             For example: '20,000.00'

    Raises:
        KeyError: If the Nasdaq 100 data is not found in the scraped data.
    """
  
    nq_scrape = scrape_prices()

    # return '20,000.00' as a string
    return nq_scrape['Nasdaq 100 (NDX)']['price']

# This allows the script to be run standalone as well
if __name__ == "__main__":
    print(ndx_price())
