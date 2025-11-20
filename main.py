import os
import requests

from pathlib import Path
from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parent
file_path = os.path.join(BASE_DIR, 'scraped_text_content.txt')

response = requests.get('https://ajnalab.com')

if response:
    print("Status:", response.status_code)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    prettified_html = soup.prettify()
    scraped_text = soup.get_text()
    
    try:
        with open(file_path, 'w') as file:
            file.write(scraped_text)
            print(f"Text from scraped content successfully written into {file_path}")
    except Exception as e:
        print("Error writing to file:", e)

else:
    print(response.status_code)
    print("Failed to fetch anything from the webpage")