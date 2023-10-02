import os
import requests
from dotenv import load_dotenv

load_dotenv()

YELP_API_KEY = os.getenv("YELP_API_KEY")

def search_business_id(business_name, location):
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {
        "Authorization": f"Bearer {YELP_API_KEY}"
    }
    params = {
        "term": business_name,
        "location": location
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    # Filter the results to find the exact business
    for business in data['businesses']:
        if business['name'].lower() == business_name.lower() and business['location']['city'].lower() == location.lower():
            return business['id']

def get_yelp_rating(business_name, location, ratings_logger, api_details_logger):
    business_id = search_business_id(business_name, location)
    url = f"https://api.yelp.com/v3/businesses/{business_id}"
    headers = {
        "Authorization": f"Bearer {YELP_API_KEY}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    
    # Log API details
    api_details_logger.info("===================================")
    api_details_logger.info(f"Yelp API Request for Business: {business_name}, Location: {location}")
    api_details_logger.info(f"API URL: {url}")
    api_details_logger.info(f"Headers: {headers}")
    api_details_logger.info("===================================")
    api_details_logger.info(f"Yelp API Raw Response: {response.json()}")
    
    raw_rating = data['rating']  # This is the raw Yelp rating
    # Log the real raw rating
    ratings_logger.info(f"Raw Yelp Rating: {raw_rating}")
        
    # Scale the rating to 0-100
    scaled_rating = (raw_rating / 5) * 100
    
    return raw_rating, scaled_rating  # Return both raw and scaled ratings





