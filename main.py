import os
import json
import requests
import logging 

from pathlib import Path
from dotenv import load_dotenv




logger = logging.getLogger(__name__)
logging.basicConfig(filename='scraper_main.log', level=logging.INFO)

BASE_DIR = Path(__file__).resolve().parent
def set_file_name(name):
    return os.path.join(BASE_DIR, f'{name}-tests.json' if name else 'tests.json')

load_dotenv(BASE_DIR / '.env')

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
    10: "Molecular Biology",
    11: "Immunology",
    12: "Parasitology",
    21: "Cytogenetics",
    23: "Others",
    26: "Package",
    30: "Clinical Pathology",
    31: "Molecular Pathology",
    33: "Cytopthology"
}

try:
    login_response = session.post(login_url, data=payload)
    
    if login_response.status_code == 200:
        logger.info(f"Login successful!, This is the success URL: {login_response.url}")
        
        for key, value in enumerate(range(34), start=1):
            if key not in index_mapping:
                logger.info(f"{key} not in mapping, skipping...")
                continue
            data_response = session.get(f"{protected_url}testresult/get_tests/{key}")
            logger.info(f"Fetching data from: {protected_url}testresult/get_tests/{key}")
            label = index_mapping[key]
            logger.info(f"Scraping data for category: {label}")

            if data_response.status_code == 200:
                scraped_data = data_response.json()
            
            try:
                with open(set_file_name(label), 'w') as file:
                    json.dump(
                        scraped_data,
                        file,
                        indent=4
                    )
                    logger.info(f"Text from scraped content successfully written into {set_file_name(label)}")
            except Exception:
                logger.exception(f"Error writing to file {set_file_name(label)}:") 
        
    else:
        logger.error(f"Login failed. Status Code: {login_response.status_code}")

except Exception:
    logger.exception("An error occurred during scraping:")






























