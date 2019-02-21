"""
Shared helper functions
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

def format_df(df_in, dtype_map):
    df = df_in.copy()
    for col, col_type in dtype_map.items():
        if col_type == 'datetime':
            df[col] = pd.to_datetime(df[col])
        else:
            df[col] = df[col].astype(col_type)
    return df


def soup_scraper(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    headers = {'User-Agent': user_agent}
    request = requests.get(url, timeout=5, headers=headers)
    soup = BeautifulSoup(request.text, 'lxml')

    return soup

