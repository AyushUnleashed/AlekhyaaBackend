import os
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import re

def send_get_request(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        print(f"An error occurred while sending the GET request: {str(e)}")
        return None

def extract_links_and_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    assets = []
    images = []
    page_text = soup.get_text()

    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            assets.append(href)

    # Remove content after "Read this release in" in the text
    page_text = re.sub(r'Read this release in.*', '', page_text, flags=re.DOTALL)

    # Reduce multiple consecutive blank lines to a single empty line
    page_text = re.sub(r'\n\s*\n', '\n\n', page_text)

    with open('webpage_text.txt', 'w', encoding='utf-8') as text_file:
        text_file.write(page_text)

    # Extract date, time, and department name using regex
    date_time_match = re.search(r'(\d{1,2} [A-Z]+ \d{4} \d{1,2}:\d{2}[APM]+) by ([A-Z\s]+)', page_text)

    date = ''
    time = ''
    department = ''

    if date_time_match:
        date_time = date_time_match.group(1)
        department = date_time_match.group(2)

        # Split date and time
        date_parts = re.split(r'\s+', date_time)
        date = ' '.join(date_parts[:3])
        time = date_parts[3]

    return assets, page_text, date, time, department

def download_images(html_content, base_url):
    image_paths = []

    if not os.path.exists('Scrapped_Images'):
        os.mkdir('Scrapped_Images')

    soup = BeautifulSoup(html_content, 'html.parser')

    ignore_classes = ["fb_b", "twitter_r", "whatsapp_r", "fa-linkedin_r", "log_oo"]
    ignore_image_names = ["facebook.jpg", "email1.png", "linkedin.png", "whatsapp1.png"]

    for img in soup.find_all('img'):
        parent_div = img.find_parent('div', class_=ignore_classes)
        if parent_div:
            continue  # Skip this image if it's inside a div with any of the ignore_classes

        img_url = urljoin(base_url, img.get('src'))
        img_name = os.path.basename(img_url)

        # Check if the image name is in the list of ignore_image_names
        if img_name in ignore_image_names:
            continue  # Skip this image

        # Check if the image name starts with 'ph'
        if img_name.startswith('ph') :
            continue  # Skip this image

        img_path = os.path.join('Scrapped_Images', img_name)

        try:
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                with open(img_path, 'wb') as img_file:
                    img_file.write(img_response.content)
                image_paths.append(img_path)
        except Exception as e:
            print(f"An error occurred while downloading an image: {str(e)}")

    return image_paths


def filter_links(links):
    filtered_links = []

    for link in links:
        # Exclude links starting with specified patterns
        if not link.startswith(('https://pib.gov.in/', 'https://mail.google.com/')):
            # Exclude redundant and social media sharing links
            if link not in filtered_links and not link.startswith(('https://www.linkedin.com/shareArticle',
                                                                   'http://www.facebook.com/share',
                                                                   'https://api.whatsapp.com/send')):
                filtered_links.append(link)

    return filtered_links

def save_links_to_file(links, filename='webpage_links.txt'):
    with open(filename, 'w', encoding='utf-8') as links_file:
        for link in links:
            links_file.write(link + '\n')

def scrape_web_page(url):
    html_content = send_get_request(url)

    if html_content is not None:
        assets, page_text, date, time, department = extract_links_and_text(html_content)
        filtered_links = filter_links(assets)
        save_links_to_file(filtered_links)

        print("Links on the page:")
        for link in filtered_links:
            print(link)

        print("Text from the page has been saved to 'webpage_text.txt'.")
        print(f"Date: {date}")
        print(f"Time: {time}")
        print(f"Department: {department}")
        print("Links have been saved to 'webpage_links.txt'.")

        images = download_images(html_content, url)
        print(f"{len(images)} images have been downloaded and saved in the 'Scrapped_Images' folder.")
    else:
        print('Failed to retrieve the web page.')

if __name__ == "__main__":
    # Example usage:
    url_to_scrape = 'https://pib.gov.in/PressReleasePage.aspx?PRID=1958748'
    scrape_web_page(url_to_scrape)