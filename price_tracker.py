import time
import requests
import yfinance as yf
from gsheets import update_google_sheet, crypto_worksheet, etf_worksheet
from config import cmc_quotes_base, cmc_key, crypto_symbols, etf_symbols, cell_mapping

def get_etf_price(symbol):
    stock = yf.Ticker(symbol)
    stock_info = stock.info
    if 'previousClose' in stock_info:
        return stock_info['previousClose']
    else:
        print(f"Key 'previousClose' not found for symbol {symbol}. Available keys: {stock_info.keys()}")
        return None
    
def get_crypto_prices(symbols):
    """
    根據多個加密貨幣符號一次性獲取即時價格。
    
    :param symbols: 加密貨幣的符號元組或列表，例如 ('BTC', 'ETH', 'SOL')
    :return: 包含每個加密貨幣價格的字典或錯誤信息
    """

    symbols_str = ','.join(symbols).upper()
    parameters = {'symbol': symbols_str, 'convert': 'USD'}
    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': cmc_key.strip()}
    
    try:
        response = requests.get(cmc_quotes_base, headers=headers, params=parameters)
        response.raise_for_status()
        data = response.json()
        
        prices = {}
        for symbol in symbols:
            try:
                price = data['data'][symbol.upper()]['quote']['USD']['price']
                prices[symbol.upper()] = price
            except KeyError:
                prices[symbol.upper()] = None  # 無法獲取價格，設為 None
        return prices
    except requests.exceptions.RequestException as e:
        print(f"發生錯誤: {e}")
        return None
    except KeyError:
        print("無法解析數據，請檢查 API 響應。")
        return None

def check_and_update_prices(worksheet, symbols, prices, timestamp, cell_mapping):
    """
    檢查並更新價格到 Google Sheets。
    
    :param worksheet: Google Sheets 的工作表
    :param symbols: 符號的元組或列表
    :param prices: 包含每個符號價格的字典
    :param timestamp: 查詢時間戳
    :param cell_mapping: 符號與儲存格的對應關係字典
    """
    #update_google_sheet(worksheet, symbols, prices, timestamp, cell_mapping)  # 更新 Google Sheets
    for symbol in symbols:
        price = prices.get(symbol.upper())
        if price is not None:
            print(f"{symbol}: ${price:.2f} USD")
            update_google_sheet(worksheet, symbols, prices, timestamp, cell_mapping)
        else:
            print(f"{symbol}: 無法獲取價格")
            update_google_sheet(worksheet, symbols, 0, timestamp, cell_mapping)

def track_crypto_prices(symbols, cell_mapping, interval=0):
    """
    每隔一定時間查詢多個加密貨幣的即時價格並更新到 Google Sheets。
    :param symbols: 加密貨幣符號的元組或列表
    :param cell_mapping: 符號與儲存格的對應關係字典，例如 {"BTC": "A2", "ETH": "B2"}
    :param interval: 查詢間隔時間，單位為秒
    """
    periodical = True
    while periodical:
        print(f"\n=== 查詢時間: {time.strftime('%Y-%m-%d %H:%M:%S')} ===")
        prices = get_crypto_prices(symbols)
        if prices:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            check_and_update_prices(crypto_worksheet, symbols, prices, timestamp, cell_mapping)
            print(f"等待 {interval} 秒後再次查詢...\n")
        if interval == 0:
            periodical = False
        else:
            print(f"等待 {interval} 秒後再次查詢...\n")
            time.sleep(interval)

def track_etf_prices(symbols, cell_mapping, interval=0):
    """
    每隔一定時間查詢多個 ETF 的即時價格並更新到 Google Sheets。
    :param symbols: ETF 符號的元組或列表
    :param cell_mapping: 符號與儲存格的對應關係字典，例如 {"00679B.TW": "A2", "00687B.TW": "B2"}
    :param interval: 查詢間隔時間，單位為秒
    """
    periodical = True
    while periodical:
        print(f"\n=== 查詢時間: {time.strftime('%Y-%m-%d %H:%M:%S')} ===")
        prices = {}
        for symbol in symbols:
            print
            print(f"查詢 {symbol} 的價格...")
            price = get_etf_price(symbol)
            if price is not None:
                prices[symbol.upper()] = price
            else:
                prices[symbol.upper()] = "N/A"
        if prices:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            check_and_update_prices(etf_worksheet, symbols, prices, timestamp, cell_mapping)
        if interval == 0:
            periodical = False
        else:
            print(f"等待 {interval} 秒後再次查詢...\n")
            time.sleep(interval)