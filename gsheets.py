import os
import pygsheets
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read environment variables
credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
spreadsheet_url = os.getenv('GOOGLE_SHEETS_URL')

# Initialize Google Sheets API
gc = pygsheets.authorize(service_file=credentials_path)
print("Google Sheets API 初始化成功。{}",credentials_path )

# Open Google Sheets and specify the worksheet name
spreadsheet = gc.open_by_url(spreadsheet_url)

# Select the worksheets
crypto_worksheet = spreadsheet.worksheet_by_title('Const')
etf_worksheet = spreadsheet.worksheet_by_title('BondsETF')

def update_google_sheet(worksheet, symbols, prices, timestamp, cell_mapping):
    """
    將價格寫入 Google Sheets 的特定儲存格。
    
    :param symbols: 加密貨幣符號的列表或元組
    :param prices: 加密貨幣價格字典
    :param timestamp: 查詢時間戳
    :param cell_mapping: 符號與儲存格的對應關係字典，例如 {"BTC": "A2", "ETH": "B2"}
    """
    # 更新時間戳至第一行
    worksheet.update_value("A1", f"Last Updated: {timestamp}")
    
    for symbol in symbols:
        cell = cell_mapping.get(symbol.upper())  # 找到對應的儲存格
        if cell:
            price = prices.get(symbol.upper())
            if price is not None:
                worksheet.update_value(cell, f"{price:.2f}")  # 更新價格
            else:
                worksheet.update_value(cell, "N/A")  # 如果無法獲取價格，填入 N/A
        else:
            print(f"符號 {symbol} 沒有對應的儲存格，跳過更新。")