import os
import json
import requests

from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
file_path = os.path.join(BASE_DIR, 'parameter_list.json')

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

try:
    login_response = session.post(login_url, data=payload)
    
    if login_response.status_code == 200:
        print("Login successful!", login_response.url)
        
        data_response = session.get(f"{protected_url}parameterlist")
        if data_response.status_code == 200:
            scraped_data = data_response.json()
            
            try:
                with open(file_path, 'w') as file:
                    json.dump(
                        scraped_data,
                        file, 
                        indent=5
                    )
                    print(f"Scraped data from '{protected_url}parameterlist' successfully written into {file_path}")
            
            except Exception as e:
                print("Error writing to file:", e)
                
    else:
        print(f"Login failed. Status Code: {login_response.status_code}")

except Exception as e:
    print("An error occurred during scraping:", e)
        
        