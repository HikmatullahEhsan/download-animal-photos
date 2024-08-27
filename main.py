import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

# Constants
BASE_URL = 'https://unsplash.com/s/photos/animals'
IMAGE_DIR = 'animal_images'
NUM_IMAGES = 50

# Ensure the directory exists
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def get_image_urls(url, num_images):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all image tags and extract the URLs
    image_tags = soup.find_all('img', {'srcset': True})
    image_urls = [img['srcset'].split(',')[0].split(' ')[0] for img in image_tags if 'srcset' in img.attrs]
    
    return image_urls[:num_images]

def download_image(url, filename):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            image = Image.open(BytesIO(response.content))
            image.save(filename)
            print(f"Downloaded and saved {filename}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")
    else:
        print(f"Failed to retrieve image from {url}")

def main():
    image_urls = get_image_urls(BASE_URL, NUM_IMAGES)
    for i, url in enumerate(image_urls):
        filename = os.path.join(IMAGE_DIR, f'animal_image_{i+1}.jpg')
        download_image(url, filename)

if __name__ == "__main__":
    main()
