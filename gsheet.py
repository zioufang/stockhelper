"""
Dealing with Google Sheets API
"""

import os.path
import pandas as pd
import numpy as np
from datetime import datetime
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# local lib
import utils
import config

CLIENT_JSON = os.path.join(config.HOME_FOLDER, 'cred.json')
TOKEN_FILE = os.path.join(config.HOME_FOLDER, 'token.pickle')
SCOPE = 'https://www.googleapis.com/auth/spreadsheets'

FOREVER_DATE = pd.to_datetime('2222-02-02')


def get_creds():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_JSON, SCOPE)
            creds = flow.run_local_server()

        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return creds


def spreadsheet_to_df(spreadsheet_id, spreadsheet_range):
    creds = get_creds()
    service = build('sheets', 'v4', credentials = creds)
    sheet = service.spreadsheets()
    res = sheet.values().get(spreadsheetId=spreadsheet_id,
                  range=spreadsheet_range).execute()
    df = pd.DataFrame(res.get('values')[1:], columns=res.get('values')[0])
    return df


#def get_stock_holding_df