import os
import json
import requests
import logging

from pathlib import Path
from dotenv import load_dotenv




BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

log_file_path = os.path.join(BASE_DIR/"logs", 'units.log')
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=log_file_path, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO
)

units_file_path = os.path.join(BASE_DIR/"from_units", 'units.json')

login_url = os.getenv('LOGIN_URL')
login_success_url = os.getenv('LOGIN_SUCCESS_URL')
protected_url = os.getenv('PROTECTED_URL_BASE')
username = os.getenv('LOGIN_USERNAME')
password = os.getenv('LOGIN_PASSWORD')

payload = {
    'usernameOrEmail': username,
    'password': password
}

# Scraping logic
session = requests.Session()
units = []

try: 
    
    login_response = session.post(login_url, data=payload)
    
    if login_response.url == login_success_url:
        logger.info("Login was successful. This is the success URL: %s", login_response.url)
        
        for unit_id in range(45):
            response = session.get(f"{protected_url}unit/{unit_id}/edit")
            
            if response.headers.get('Content-Type') != 'application/json':    
                logger.info(f"No data to fetch for unitID[{unit_id}], skipping...")
                continue
            
            logger.info(f"Fetching data for unitID[{unit_id}] from: {protected_url}unit/{unit_id}/edit")
            data = response.json()
            units.append(data)
        
        try:
            with open(units_file_path, 'w') as file:
                json.dump(
                    units,
                    file,
                    indent=3
                )
                logger.info(f"All scraped data successfully written into {units_file_path}")        
                print(f"All unit data fetched and written into {units_file_path}.")
        except Exception:
            logger.exception(f"Error writing data to file {units_file_path}:")
    else:
        logger.error("Login failed. Please check your credentials.")
except Exception:
    logger.exception("An error occurred during the scraping process:")