import os
import json
import requests
import logging 

from pathlib import Path
from dotenv import load_dotenv




BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

log_file_path = os.path.join(BASE_DIR/"logs", 'scraper_main.log')
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=log_file_path, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO
)

def set_file_name_to_keep_scraped_data(name):
    return os.path.join(BASE_DIR/"from_parameters", f'{name}-tests.json')

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

index_mapping = {
    1: "Biochemistry",
    2: "Microbiology",
    3: "Haematology",
    6: "Serology",
    7: "Histopathology",
    8: "Immunoassay",
    9: "ImmunoHistoChemistry",
    10: "Molecular-Biology",
    11: "Immunology",
    12: "Parasitology",
    21: "Cytogenetics",
    23: "Others",
    26: "Package",
    30: "Clinical-Pathology",
    31: "Molecular-Pathology",
    33: "Cytopthology"
}

try:
    login_response = session.post(login_url, data=payload)
    
    ## TODO: for if condition below, change status code check to URL check, because status code is 200 even on failed login
    if login_response.status_code == 200:
        logger.info(f"Login successful! This is the success URL: {login_response.url}")
        
        for key, value in enumerate(range(34), start=1):
            
            if key not in index_mapping:
                logger.info(f"{key} not in mapping, skipping...")
                continue
            
            response = session.get(f"{protected_url}testresult/get_tests/{key}")

            if response.status_code == 200:
                logger.info(f"Fetching data from: {protected_url}testresult/get_tests/{key}")
                label = index_mapping[key]
                logger.info(f"Scraping data for category: {label}")
                scraped_data = response.json()
            
                try:
                    with open(set_file_name_to_keep_scraped_data(label), 'w') as file:
                        json.dump(
                            scraped_data,
                            file,
                            indent=4
                        )
                        logger.info(f"Scraped data successfully written into {set_file_name_to_keep_scraped_data(label)}")
                except Exception:
                    logger.exception(f"Error writing to file {set_file_name_to_keep_scraped_data(label)}:") 
                    
            else:
                logger.error(f"Failed to fetch data from {protected_url}testresult/get_tests/{key}. Status Code: {response.status_code}")
        
    else:
        logger.error(f"Login failed. Status Code: {login_response.status_code}")

except Exception:
    logger.exception("An error occurred during scraping:")






























