import os
import json
import requests
import logging

from pathlib import Path
from dotenv import load_dotenv


logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='short_codes.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO
)


BASE_DIR = Path(__file__).resolve().parent
file_path = os.path.join(BASE_DIR/'from_shortcodes', 'shortcodes.json')

load_dotenv(BASE_DIR/ '.env')

# fetch env variables
login_url = os.getenv('LOGIN_URL')
protected_url = os.getenv('PROTECTED_URL_BASE')
username = os.getenv('LOGIN_USERNAME')
password = os.getenv('LOGIN_PASSWORD')


# Scraping logic
session = requests.Session()

payload = {
    'usernameOrEmail': username,
    'password': password
}

login_response = session.post(login_url, data=payload)

try:
    
    if login_response.status_code == 200:
        logger.info(f"Login successful! This is the success URL: {login_response.url}")
        
        response = session.get(f"{protected_url}shortcode?_=1763835813693")
        logging.info(f"Fetched shortcodes from {protected_url}shortcode?_=1763835813693")
        
        if response.status_code == 200:
            shortcodes = response.json()
            
            try:
                with open(file_path, 'w') as json_file:
                    json.dump(
                        shortcodes,
                        json_file,
                        indent=4
                    )
                logger.info(f"Shortcodes successfully written to {file_path}")
           
            except Exception as e:
                logger.exception("Error while writing to file")
        
        else:
            logger.error(f"Failed to fetch shortcodes, status code: {response.status_code}")
            
    else:
        logger.error(f"Login failed with status code: {login_response.status_code}")
        
except Exception as e:
    logger.exception("An error occurred during the scraping process")