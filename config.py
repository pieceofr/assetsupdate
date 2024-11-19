import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 儲存加密貨幣符號的元組
crypto_symbols = ("SOL", "PYTH", "ETH", "MATIC", "BTC", "JUP", "JTO", "SUI", "CRO")

# 儲存 ETF 符號的元組
etf_symbols = ("00679B.TW", "00687B.TW", "00712.TW", "00751B.TW", "00857B.TW", "00933B.TW", "00937B.TW")


# 定義符號與儲存格的對應
cell_mapping = {
    "SOL": "B6",
    "PYTH": "B7",
    "ETH": "B8",
    "MATIC": "B9",
    "BTC": "B10",
    "JUP": "B11",
    "JTO": "B12",
    "SUI": "B13",
    "CRO": "B14",
    "00679B.TW": "B6",
    "00687B.TW": "B7",
    "00712.TW": "B8",
    "00751B.TW": "B9",
    "00857B.TW": "B10",
    "00933B.TW": "B11",
    "00937B.TW": "B12",
}

# 讀取 cmc_key 從環境變量
cmc_key = os.getenv('CMC_KEY')
cmc_quotes_base = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
# Google Sheets Config
assets_analysis_url='https://docs.google.com/spreadsheets/d/1rj6Oc18TlnMpedoVlJHGnmPDa5zct7d1S1xDS7DUQQU/'
    
