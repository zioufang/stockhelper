import gsheet
import web_scraper
import utils

# stock_trade Google Sheet
ss_id = '1h6p2-m8KfBqub9qJT8lxHX3se68o3TYSpuYEjJ3QFsY'
ss_range = 'Sheet1!A:G'

df_ss = gsheet.spreadsheet_to_df(ss_id, ss_range)