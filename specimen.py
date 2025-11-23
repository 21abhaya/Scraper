import os
import json
import requests
import logging

from pathlib import Path
from dotenv import load_dotenv




BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

log_file_path = os.path.join(BASE_DIR/"logs", 'specimen.log')
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=log_file_path, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO
)

specimens_file_path = os.path.join(BASE_DIR/"from_specimen", 'specimens.json')

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
all_data = []

try: 
    
    login_response = session.post(login_url, data=payload)
    
    if login_response.url == login_success_url:
        logger.info("Login was successful. This is the success URL: %s", login_response.url)
        
        for specimen_id in range(115):
            response = session.get(f"{protected_url}specimen/{specimen_id}/edit")
            
            if response.headers.get('Content-Type') != 'application/json':    
                logger.info(f"No data to fetch for specimenID[{specimen_id}], skipping...")
                continue
            
            logger.info(f"Fetching data for specimenID[{specimen_id}] from: {protected_url}specimen/{specimen_id}/edit")
            data = response.json()
            all_data.append(data)
            
        try:
            with open(specimens_file_path, 'w') as file:
                json.dump(
                    all_data,
                    file,
                    indent=3
                )
                logger.info(f"All scraped data successfully written into {specimens_file_path}")        
        except Exception:
            logger.exception(f"Error writing data to file {specimens_file_path}:")
    else:
        logger.error("Login failed. Please check your credentials.")
except Exception:
    logger.exception("An error occurred during the scraping process:")