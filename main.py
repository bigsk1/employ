import os
import requests
import yaml
import logging
from yelp import get_yelp_rating
from bbb import get_bbb_rating
from google import get_google_rating

# logging.root.disabled = True

# Initialize logging for ratings.log
log_filename = 'ratings.log'
if not os.path.exists(log_filename):
    with open(log_filename, 'w') as f:
        pass  # Create an empty file

ratings_logger = logging.getLogger('ratings')
ratings_logger.setLevel(logging.INFO)
ratings_fh = logging.FileHandler(log_filename)
ratings_formatter = logging.Formatter('%(asctime)s - %(message)s')
ratings_fh.setFormatter(ratings_formatter)
ratings_logger.addHandler(ratings_fh)

# Initialize logging for api_details.log
api_log_filename = 'api_details.log'
if not os.path.exists(api_log_filename):
    with open(api_log_filename, 'w') as f:
        pass  # Create an empty file

api_details_logger = logging.getLogger('api_details')
api_details_logger.setLevel(logging.INFO)
api_fh = logging.FileHandler(api_log_filename)
api_formatter = logging.Formatter('%(asctime)s - %(message)s')
api_fh.setFormatter(api_formatter)
api_details_logger.addHandler(api_fh)

# Load YAML configuration
with open("employ.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
        business_name = config.get('business_name', '')  # Default to an empty string if not present
        location = config.get('location', '')  # Default to an empty string if not present
    except yaml.YAMLError as exc:
        ratings_logger.error(f"Error in configuration file: {exc}")  # Use ratings_logger

# Log separator and business name
ratings_logger.info(f"Business Name: {business_name}")
ratings_logger.info("===================================")


# Initialize variables
weights = {
    'yelp': config['yelp']['weight'],
    'turnover': config['turnover']['weight'],
    'credit_score': config['credit_score']['weight'],
    'bbb': config.get('bbb', {}).get('weight', 0),
    'google': config['google']['weight'],
    # Add other services here
}

# Initialize overall score and sum of weights
overall_score = 0
sum_of_weights = 0

# Yelp Rating
try:
    raw_yelp_rating, scaled_yelp_rating = get_yelp_rating(business_name, location, ratings_logger, api_details_logger)
    if raw_yelp_rating and scaled_yelp_rating:
        overall_score += scaled_yelp_rating * weights['yelp']
        sum_of_weights += weights['yelp']
        ratings_logger.info(f"Scaled Yelp Rating: {scaled_yelp_rating}")
        ratings_logger.info(f"Weighted Yelp Rating: {scaled_yelp_rating * weights['yelp']}")
except Exception as e:
    ratings_logger.error(f"Could not get Yelp rating: {e}")

# Add other services here

# Employee Turnover Rate
try:
    turnover_rate = config['turnover']['rate']
    scaled_turnover = (100 - turnover_rate)
    overall_score += scaled_turnover * weights['turnover']
    sum_of_weights += weights['turnover']
    ratings_logger.info(f"Raw Turnover Rate: {turnover_rate}")  # Use ratings_logger
    ratings_logger.info(f"Scaled Turnover Rate: {scaled_turnover}")  # Use ratings_logger
    ratings_logger.info(f"Weighted Turnover Rate: {scaled_turnover * weights['turnover']}")  # Use ratings_logger
except Exception as e:
    ratings_logger.error(f"Could not get turnover rate: {e}")  # Use ratings_logger

# Credit Score
try:
    scaled_credit_score = (config['credit_score']['score'] / 800) * 100
    overall_score += scaled_credit_score * weights['credit_score']
    sum_of_weights += weights['credit_score']
    ratings_logger.info(f"Scaled Credit Score: {scaled_credit_score}")  # Use ratings_logger
    ratings_logger.info(f"Weighted Credit Score: {scaled_credit_score * weights['credit_score']}")  # Use ratings_logger
except Exception as e:
    ratings_logger.error(f"Could not get Credit Score: {e}")  # Use ratings_logger

    
# BBB Rating
bbb_token = os.getenv("BBB_API_TOKEN")  # Assuming you've stored your token in an environment variable
if bbb_token:  # Check if BBB token exists
    try:
        raw_bbb_rating, scaled_bbb_rating = get_bbb_rating(business_name, location, api_details_logger, ratings_logger)
        if raw_bbb_rating and scaled_bbb_rating:
            overall_score += scaled_bbb_rating * weights['bbb']
            sum_of_weights += weights['bbb']
            ratings_logger.info(f"Scaled BBB Rating: {scaled_bbb_rating}")
            ratings_logger.info(f"Weighted BBB Rating: {scaled_bbb_rating * weights['bbb']}")
    except IndexError:
        ratings_logger.error("BBB rating: Business not found or data unavailable.")
    except Exception as e:
        ratings_logger.error(f"Could not get BBB rating: {e}")
else:
    ratings_logger.info("Skipping BBB rating as token is not available.")

# Google Places Rating
try:
    google_rating = get_google_rating(business_name, location, ratings_logger, api_details_logger)
    if google_rating:
        overall_score += google_rating * weights['google']
        sum_of_weights += weights['google']
        ratings_logger.info(f"Scaled Google Rating: {google_rating}")
        ratings_logger.info(f"Weighted Google Rating: {google_rating * weights['google']}")
except Exception as e:
    pass


# Calculate the overall score
if sum_of_weights > 0:
    overall_score = overall_score / sum_of_weights
    print(f"The overall score for the business is {overall_score:.2f}/100")
    ratings_logger.info(f"The overall score for the business is {overall_score:.2f}/100")  # Use ratings_logger
    ratings_logger.info("===================================")  # Use ratings_logger, Separator
    with open("overall_score.txt", "w") as f:
        f.write(f"The overall score for the business is {overall_score:.2f}/100")
else:
    print("No data available to calculate the score.")
    ratings_logger.info("No data available to calculate the score.")  # Use ratings_logger
    ratings_logger.info("===================================")  # Use ratings_logger, Separator












