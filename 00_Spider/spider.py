import requests
import argparse
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

EXT = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
HEADER = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0'}


def is_valid_url(url):
    try:
        repsonse = requests.head(url, timeout=3)
        return repsonse.status_code == 200
    except requests.exceptions.RequestException as e:
        return False

def download_image( image_url, path_to_save):
    filename = os.path.basename(image_url)
    save_path = os.path.join(path_to_save, filename)
    try:
        if os.path.exists(save_path):
            raise Exception(f'Image {filename} allready exists in the save directory')
        img_response = requests.get(image_url, headers=HEADER, timeout=5)
        if img_response.status_code != 200:
            raise Exception(f'Failed to fetch image!')
        with open(save_path, 'wb') as file:
            file.write(img_response.content)
            return 1
    except Exception as e:
        print (f'Skipping {filename}: {e}')
        return 0


def resolve_img_url(base_url, path):
    parse = urlparse(path)
    if not parse.netloc:
        return urljoin(base_url, parse.path)
    elif not parse.scheme:
        return 'http://' + parse.netloc + parse.path
    return parse.scheme + '://' + parse.netloc + parse.path

def download_images_from_url(url, soup: BeautifulSoup, args):
    image_tags = soup.find_all('img')
    for image_tag in image_tags:
        image_path = image_tag.get('src')
        ext = os.path.splitext(image_path)[-1]
        if ext.lower() not in EXT:
            continue
        image_url = resolve_img_url(url, image_path)
        download_image(image_url, args.p)

def download_recursive(url, depth, visited, args):
    if depth < 1 or url in visited:
        return
    visited.add(url)
    try:
        response = requests.get(url, headers=HEADER, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        download_images_from_url(url, soup, args)
        for link_tag in soup.find_all('a', href=True):
            link = link_tag.get('href')
            resolved_url = urljoin(url, link)
            parsed_url = urlparse(resolved_url)
            if parsed_url.netloc and parsed_url.netloc in urlparse(url).netloc:
                download_recursive(resolved_url, depth - 1, visited, args)
    except requests.RequestException as e:
        print (f'Error scraping {url}: {e}')


def scrape(args):
    try:
        response = requests.get(url=args.URL, headers=HEADER)
        soup = BeautifulSoup(response.text, 'html.parser')
        if (args.r == False):
            download_images_from_url(args.URL, soup, args)
        else:
            visited = set()
            download_recursive(args.URL, args.l, visited, args)
    except KeyboardInterrupt as e:
        print ("Keyboard Intereput!")

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-r', action='store_true', default=False,help='Recursively downloads the image')
    parser.add_argument('-l', type=int, default=5,help='Maximum depth to download images, 5 default')
    parser.add_argument('-p', type=str, default='./data/',help='Path where to save the images, ./data/ default')
    parser.add_argument('URL', type=str, help='URL to scrape images')
    args = parser.parse_args()

    if (args.p == './data/'):
        curent_dir = os.getcwd()
        data_path = os.path.join(curent_dir, 'data')
        if not (os.path.isdir(data_path)):
            os.mkdir(data_path)
    elif (os.path.isdir(args.p) == False):
        parser.error(f'{args.p} is not a valid path')
    if (args.l < 1):
        parser.error('-l has to have a value grater than 0')
    if not (is_valid_url(args.URL)):
        parser.error(f'{args.URL} is not reachable')
    scrape(args)

if __name__=='__main__':
    main()
