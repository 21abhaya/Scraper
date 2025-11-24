import os
import json
import requests
import logging

from pathlib import Path
from dotenv import load_dotenv




BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

log_file_path = os.path.join(BASE_DIR/"logs", 'subtests_and_refRange.log')
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=log_file_path, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO
)


path_to_json_files = os.path.join(BASE_DIR/"from_parameters")

json_files = [pos_json for pos_json in os.listdir(path_to_json_files) if pos_json.endswith('.json')]

# fetch env variables
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

try: 
    subTests_and_refRange = []
    login_response = session.post(login_url, data=payload)
    
    if login_response.url == login_success_url:
        logger.info(f"Login was successful. This was the login response URL: {login_response.url}")
    
        for json_file in json_files:
            json_file_path = os.path.join(path_to_json_files, json_file)
            
            with open(json_file_path, 'r') as file:
                data = json.load(file)
                records = data.get("testnames", [])
                logger.info(f"Processing file: {json_file} with {len(records)} records.")
                
                for record in records:
                    test_id = record.get("id")
                    response = session.get(f"{protected_url}testresult/showall/{test_id}?test_id={test_id}")
                    
                    if response.status_code == 200:
                        logger.info(f"Fetched data for TestID[{test_id}] from {protected_url}testresult/showall/{test_id}?test_id={test_id}")
                        data = response.json()
                    
                        if not data:
                            logger.warning(f"No data found for TestID[{test_id}]")
                            continue
                        test_results = data.get("testResults", [])
                        
                        # if isinstance(test_results, list) and test_results:
                        #     ref_range = test_results[0].get("refRange", [])
                        #     logger.info(f"Retrieved refRange for TestID[{test_id}]: {ref_range}")   
                        record["testResults"] = test_results
                        subTests_and_refRange.append(record)
                    
                with open((os.path.join(BASE_DIR/"from_parameters/subTests_and_refRange", json_file)), 'w') as file:
                    json.dump(
                        subTests_and_refRange,
                        file,
                        indent=4
                    )
    else:
        logger.error(f"Login failed. Please check your credentials and try again. This was the succes url: {login_response.url}")    
            
except Exception as e:
    logger.exception(f"An error occurred during the scraping process:")