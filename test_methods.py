import os
import json
import requests
import logging

from pathlib import Path
from dotenv import load_dotenv




BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

log_file_path = os.path.join(BASE_DIR/"logs", 'test_methods.log')
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=log_file_path, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO
)

testmethod_file_path = os.path.join(BASE_DIR/"from_testmethod", 'test_methods.json')

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
test_methods = []

try: 
    
    login_response = session.post(login_url, data=payload)
    
    if login_response.url == login_success_url:
        logger.info("Login was successful. This is the success URL: %s", login_response.url)
        
        for testmethod_id in range(100):
            response = session.get(f"{protected_url}test_method/{testmethod_id}/edit")
            
            if response.headers.get('Content-Type') != 'application/json':    
                logger.info(f"No data to fetch for testmethodID[{testmethod_id}], skipping...")
                continue
            
            logger.info(f"Fetching data for testmethodID[{testmethod_id}] from: {protected_url}test_method/{testmethod_id}/edit")
            data = response.json()
            test_methods.append(data)
            
        print("All data fetched, now writing to file...")
        
        try:
            with open(testmethod_file_path, 'w') as file:
                json.dump(
                    test_methods,
                    file,
                    indent=3
                )
                logger.info(f"All scraped data successfully written into {testmethod_file_path}")        
        except Exception:
            logger.exception(f"Error writing data to file {testmethod_file_path}:")
    else:
        logger.error("Login failed. Please check your credentials.")
except Exception:
    logger.exception("An error occurred during the scraping process:")