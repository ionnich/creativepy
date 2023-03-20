import requests
import os
from bs4 import BeautifulSoup


# filter for files that contain "tab_urls" in the name
tab_urls = [f for f in os.listdir('.') if 'tab_urls' in f]

with open (tab_urls[0], 'r') as f:
    urls = f.readlines()

# Retrieve the headlines from each URL and save them to a new file
with open('headlines.txt', 'w') as f:
    for url in urls:
        # Remove any trailing whitespace or newline characters from the URL
        url = url.strip()
        # Retrieve the webpage and parse it using BeautifulSoup
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        # Find the headline element and extract its text
        headline = soup.find('h1').get_text()
        # Write the headline to the output file
        f.write(headline + '\n')
