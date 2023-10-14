import requests
from bs4 import BeautifulSoup
import time

def fetch_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        print("Waiting for 10 seconds before parsing the content...")
        time.sleep(10)  # Delay for 10 seconds
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    else:
        return f"Error {response.status_code}: Unable to fetch content from the URL."

url = "https://arxivxplorer.com/?query=LLM"
content = fetch_content(url)
print(content)
