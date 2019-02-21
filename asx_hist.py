"""
Getting ASX historical data from https://www.asxhistoricaldata.com/:

latest_zip_to_df(): read the latest zip to df directly from 
local_folder_to_df(zip_folder_path): read historical stock data from the manually downloaded zip files in a folder
"""

import zipfile
import os
import pandas as pd 
import io
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup

# local lib
import config
import utils

def get_latest_zip():
    url = 'https://www.asxhistoricaldata.com'
    soup = utils.soup_scraper(url)

    # get the latest zip url from website
    zip_url = soup.find('div', {'id': 'downloads'}).findAll('a', href=True)[0]['href']

    z = urlopen(zip_url).read()
    return io.BytesIO(z)


def zip_to_df(zip_file):
    """
    zipfile: can be the abs local path of a zip file or the BytesIO of a zip url 
    """
    with zipfile.ZipFile(zip_file) as zf:
        txt_files = [text_file.filename for text_file in zf.infolist() if text_file.filename.lower().find('.txt') > 0]
        read_txt = lambda file: pd.read_csv(zf.open(file), 
            header=None, names = ['code', 'date', 'open', 'high', 'low', 'close', 'volume'])
        df = pd.concat(list(map(read_txt, txt_files)))
    
    return df


def latest_zip_to_df():
    zip_file = get_latest_zip()
    return zip_to_df(zip_file)


def local_folder_to_df(zip_folder_path):
    """
    zip_folder: all zip files in the folder will be read to df
    """
    zips = os.listdir(zip_folder_path)
    zips_paths = [os.path.join(zip_folder_path, z) for z in zips]

    df = pd.concat([zip_to_df(p) for p in zips_paths])
    
    return df

