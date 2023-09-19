import requests
from bs4 import BeautifulSoup

# Define the URL of the web page you want to scrape
url = 'https://pib.gov.in/PressReleasePage.aspx?PRID=1958754'

# Send an HTTP GET request to the URL
response = requests.get(url)
# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find and extract all links on the page
    assets = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            assets.append(href)

    # Extract and save the text from the page to a txt file
    page_text = soup.get_text()
    with open('webpage_text.txt', 'w', encoding='utf-8') as text_file:
        text_file.write(page_text)

    # Print or process the extracted links and text as needed
    print("Links on the page:")
    for link in assets:
        print(link)

    print("Text from the page has been saved to 'webpage_text.txt'.")
else:
    print('Failed to retrieve the web page.')