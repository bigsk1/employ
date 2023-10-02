import requests
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def get_google_rating(business_name, location, ratings_logger, api_details_logger):
    try:
        business_name = business_name.replace(" ", "+")
        location = location.replace(" ", "+")
        
        url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={business_name}+{location}&inputtype=textquery&fields=place_id&key={GOOGLE_API_KEY}"
        
        response = requests.get(url)
        data = response.json()
        place_id = data['candidates'][0]['place_id']
        
        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=rating&key={GOOGLE_API_KEY}"
        response = requests.get(url)
        data = response.json()
        rating = data['result']['rating']
        
        # Log the real raw rating
        ratings_logger.info(f"Raw Google Rating: {rating}")

        scaled_rating = rating * 20  # Assuming you're scaling it to 0-100

        # Log API details
        api_details_logger.info("===================================")
        api_details_logger.info(f"Google API Request for Business: {business_name}, Location: {location}")
        api_details_logger.info(f"API URL: {url}")
        api_details_logger.info("===================================")
        api_details_logger.info(f"Google API Raw Response: {response.json()}")
             
        return scaled_rating

    except IndexError:
        ratings_logger.error("Google rating: Business not found or data unavailable.")
        raise  # re-raise the exception
    except Exception as e:
        ratings_logger.error(f"Could not fetch Google rating: {e}")
        raise  


