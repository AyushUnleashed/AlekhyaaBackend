import os
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

# Function to extract PRID from the URL
def extract_prid_from_url(url):
    parsed_url = urlparse(url)
    query_parameters = parse_qs(parsed_url.query)
    if 'PRID' in query_parameters:
        return query_parameters['PRID'][0]
    else:
        return None

# Function to create a folder for images
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

# Function to download and save an image
def save_image(image_url, folder_name):
    response = requests.get(image_url)
    if response.status_code == 200:
        # Generate a random image name
        random_image_name = str(random.randint(1, 10000)) + '.jpg'
        image_path = os.path.join(folder_name, random_image_name)
        with open(image_path, 'wb') as image_file:
            image_file.write(response.content)
        print(f'Saved: {image_path}')
    else:
        print(f'Failed to download image: {image_url}')

# Main function
def scrape_images_from_website(url):
    prid = extract_prid_from_url(url)
    if prid:
        folder_name = f'PRID_{prid}'
        create_folder(folder_name)

        # Send an HTTP GET request to the URL
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all image tags in the HTML
            img_tags = soup.find_all('img')

            # Extract the image URLs and save them
            if len(img_tags) == 0:
                print('No images found on the page.')
            else:
                for img_tag in img_tags:
                    img_url = img_tag.get('src')
                    if img_url:
                        save_image(img_url, folder_name)
        else:
            print(f'Failed to fetch URL: {url}')
    else:
        print('PRID not found in the URL.')

if __name__ == "__main__":
    input_url = "https://pib.gov.in/PressReleseDetail.aspx?PRID=1959030"
    scrape_images_from_website(input_url)
