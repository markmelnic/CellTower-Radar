
import os, csv, json, shutil, requests, gzip
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

MLS_URL = 'https://location.services.mozilla.com/downloads'

def download():

    # find MLS file link
    page = requests.get(MLS_URL, headers = HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')

    mls_file_link = soup.find_all('ul')[1].find_all('li')[0].find('a')['href']
    file_credentials = soup.find_all('ul')[1].find_all('li')[0].get_text()

    # download MLS file
    print('Downloading MLS file', file_credentials)
    mls_filename = mls_file_link.split('/')[-1]
    with requests.get(mls_file_link, stream=True) as r:
        with open(mls_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    # extract from zip
    with gzip.open(mls_filename, 'rb') as mls_zip_in:
        with open('mls.csv', 'wb') as mls_zip_out:
            shutil.copyfileobj(mls_zip_in, mls_zip_out)

    os.remove(mls_filename)

if __name__ == '__main__':

    download()