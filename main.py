import argparse
from price_tracker import track_crypto_prices, track_etf_prices
from price_tracker import track_etf_prices
from config import crypto_symbols, cell_mapping, etf_symbols

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Track cryptocurrency and ETF prices.")
    parser.add_argument("--interval", type=int, default=0, help="Interval in seconds between price checks. Use 0 to disable it.")
    args = parser.parse_args()
    
    # 每隔 interval 秒查詢一次
    track_crypto_prices(crypto_symbols, cell_mapping, args.interval)
    #track_etf_prices(etf_symbols, cell_mapping, args.interval)