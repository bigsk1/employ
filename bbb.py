import os
import requests

from dotenv import load_dotenv

load_dotenv()

def letter_to_numeric(letter_grade):
    letter_to_score = {
        'A+': 97, 'A': 94, 'A-': 90,
        'B+': 87, 'B': 84, 'B-': 80,
        'C+': 77, 'C': 74, 'C-': 70,
        'D+': 67, 'D': 64, 'D-': 60,
        'F': 0
    }
    return letter_to_score.get(letter_grade, 0)


def get_bbb_rating(business_name, location, api_details_logger, ratings_logger):
    # Load the token from the .env file
    bbb_token = os.getenv("BBB_API_TOKEN")
    
    # Your API endpoint and parameters here
    url = f"https://api.bbb.org/api/orgs/search?primaryOrganizationName={business_name}&city={location}"
    headers = {
        "Authorization": f"Bearer {bbb_token}"
    }
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    # Log the raw API data using api_details_logger
    api_details_logger.info("===================================")
    api_details_logger.info(f"BBB API Request for Business: {business_name}, Location: {location}")
    api_details_logger.info(f"API URL: {url}")
    api_details_logger.info(f"Headers: {headers}")
    api_details_logger.info("===================================")
    api_details_logger.info(f"BBB API Raw Response: {data}")
    
    # Initialize scaled_rating
    scaled_rating = 0

    search_results = data.get('SearchResults', [])
    if search_results:
        # Assuming the first result is the business we are interested in
        business_data = search_results[0]
        
        # Extract the BBB rating
        bbb_rating = business_data.get('RatingIcons', [{}])[0].get('Url', '').split('-')[-1].replace('.png', '')
        
        # Log the real raw rating
        ratings_logger.info(f"Raw BBB Rating: {bbb_rating}")
        
        try:
            # Check if the rating is numeric (1-5)
            bbb_rating = float(bbb_rating)
            scaled_rating = (bbb_rating / 5) * 100
        except ValueError:
            # Convert letter grade to numeric score based on BBB scale
            bbb_rating = letter_to_numeric(bbb_rating)
            scaled_rating = (bbb_rating / 100) * 100  # Already scaled to 100

    if scaled_rating == 0:
        ratings_logger.info("No BBB rating found for the business.")

    return bbb_rating, scaled_rating  # Return both raw and scaled ratings



