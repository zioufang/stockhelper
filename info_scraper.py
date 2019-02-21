"""
Scraping the web for different things:

get_div_df(code): get the dividend dataframe from web
get_delist_df(year): get the delist history from web
get_company_list_df(): get the latest company list in ASX
"""

import requests
import re
from bs4 import BeautifulSoup
from itertools import compress
import pandas as pd
import io

# local lib
import utils

def web_table_to_df(url, row_regex, cols):
    """
    url: url to scrap
    row_regex: the regex pattern to get the revelant rows
    cols: column names for the dataframe
    returns: dataframe
    """
    soup = utils.soup_scraper(url)
    
    # find all tr element
    all_tr = soup.findAll('tr')
    wanted_bool = [True if i else False for i in list(map(row_regex.search, map(str,all_tr)))]
    wanted_tr = list(compress(all_tr, wanted_bool))
    
    if len(wanted_tr) > 0:
        # fetch the table into a list of lists and convert to a df
        data = [[c.getText() for c in tr.findAll('td')] for tr in wanted_tr]
        df = pd.DataFrame(data, columns=cols)
    else:
        df = pd.DataFrame()
        
    return df


def get_div_df(code):
    url = f'http://www.sharedividends.com.au/{code}+dividend+history'
    # dates in the dividend rows have dd-MMM-yyyy (e.g. 26-Nov-1986) format
    row_regex = re.compile(r'<td>[0-9]{2}-[A-Z][a-z]{2}-[0-9]{4}<')
    cols = ['ex_date', 'amount', 'franked', 'franking_credit', 'book_close', 'date_payable']

    df = web_table_to_df(url, row_regex, cols)
    
    if not df.empty:
        df['code'] = code
        df['date_payable'] = df['date_payable'].str.replace('\r','')

        dtype_map = {
            'ex_date': 'datetime',
            'amount': 'float64',
            'franking_credit': 'float64',
            'book_close': 'datetime',
            'date_payable': 'datetime'
        }
        df = utils.format_df(df, dtype_map)
    
    return df


def get_delist_df(year):
    url = f'https://www.asx.com.au/prices/asx-code-and-company-name-changes-{year}.htm'
    # dates in the delist rows have dd MMM (e.g. 26 Nov) format
    row_regex = re.compile(r'<td>[0-9]{2} [A-Z][a-z]{2}<')
    cols = ['as_of', 'old_code', 'old_name', 'new_code', 'new_name']

    df = web_table_to_df(url, row_regex, cols)
    
    if not df.empty:
        df['delist_date'] = df['as_of'] + ' ' + str(year)
        df.drop(columns = ['as_of'], inplace=True)

        dtype_map = {
            'delist_date': 'datetime'
        }
        df = utils.format_df(df, dtype_map)

    return df


def get_company_list_df():
    url = 'https://www.asx.com.au/asx/research/ASXListedCompanies.csv'
    content = requests.get(url).content
    df = pd.read_csv(io.StringIO(content.decode('utf-8')), skiprows=1, header=None, names=['company_name', 'code', 'gics_group'])
    return df
