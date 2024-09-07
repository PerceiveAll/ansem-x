import requests
import pandas as pd
from datetime import datetime

BINANCE_API_KEY = '-' #enter binance API here and remove the -
BINANCE_BASE_URL = 'https://api.binance.com/api/v3/'

HEADERS = {
    'X-MBX-APIKEY': BINANCE_API_KEY
}

def fetch_top_200_altcoins():
    """Fetch top 200 altcoins by volume from Binance and separate those with both BTC and ETH pairs."""
    url = f"{BINANCE_BASE_URL}ticker/24hr"
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, list):
            # Filter symbols that have both BTC and ETH pairs
            btc_pairs = set([item['symbol'].replace('BTC', '') for item in data if item['symbol'].endswith('BTC')])
            eth_pairs = set([item['symbol'].replace('ETH', '') for item in data if item['symbol'].endswith('ETH')])
            
            # Find common symbols with both BTC and ETH pairs
            both_pairs = btc_pairs.intersection(eth_pairs)
            only_btc_pairs = btc_pairs.difference(both_pairs)  # BTC pairs but no ETH pair
            only_eth_pairs = eth_pairs.difference(both_pairs)  # ETH pairs but no BTC pair

            print(f"Altcoins with both BTC and ETH pairs: {len(both_pairs)}")
            print(f"Altcoins with only BTC pairs: {len(only_btc_pairs)}")
            print(f"Altcoins with only ETH pairs: {len(only_eth_pairs)}")

            return {
                'both_pairs': list(both_pairs),
                'only_btc_pairs': only_btc_pairs,
                'only_eth_pairs': only_eth_pairs
            }
        else:
            print("Unexpected response format from Binance API.")
            return None
    except requests.exceptions.RequestException as err:
        print(f"Error fetching altcoins: {err}")
        return None

def fetch_historical_data(symbol, start_date, end_date):
    """Fetch historical kline (candlestick) data for a given symbol and date range."""
    url = f"{BINANCE_BASE_URL}klines"
    start_time = int(pd.Timestamp(start_date).timestamp() * 1000)
    end_time = int(pd.Timestamp(end_date).timestamp() * 1000)
    
    params = {
        'symbol': symbol,
        'interval': '1d',  # Daily candles
        'startTime': start_time,
        'endTime': end_time,
        'limit': 1000  # Maximum limit
    }
    
    try:
        response = requests.get(url, headers=HEADERS, params=params).json()
        if isinstance(response, list):
            return pd.DataFrame(response, columns=[
                'open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                'taker_buy_quote_asset_volume', 'ignore'
            ])
        else:
            print(f"Error fetching historical data for {symbol}: {response}")
            return None
    except requests.exceptions.RequestException as err:
        print(f"Error fetching historical data for {symbol}: {err}")
        return None

def fetch_current_price(symbol):
    """Fetch the latest price for a given symbol."""
    url = f"{BINANCE_BASE_URL}ticker/price"
    params = {
        'symbol': symbol
    }
    try:
        response = requests.get(url, headers=HEADERS, params=params).json()
        return float(response['price']) if 'price' in response else None
    except requests.exceptions.RequestException as err:
        print(f"Error fetching current price for {symbol}: {err}")
        return None

def calculate_roi(start_price, end_price):
    """Calculate the Return on Investment (ROI)."""
    return ((end_price - start_price) / start_price) * 100 if start_price != 0 else None

def process_pair(symbol, start_date, end_date, pair_type):
    """Process historical data and calculate ROI for a given symbol's BTC or ETH pair."""
    pair = symbol + pair_type  # Append 'BTC' or 'ETH'
    
    # Fetch historical data for the pair
    historical_data = fetch_historical_data(pair, start_date, end_date)

    if historical_data is not None:
        historical_data['timestamp'] = pd.to_datetime(historical_data['open_time'], unit='ms')
        july_5_price = historical_data.loc[(historical_data['timestamp'] >= start_date)].head(1)['low'].values
        august_5_price = historical_data.loc[(historical_data['timestamp'] <= end_date)].tail(1)['low'].values

        print(f"Processing {pair}: July 5 Price: {july_5_price}, August 5 Price: {august_5_price}")

        if len(july_5_price) > 0 and len(august_5_price) > 0:
            july_5_price = float(july_5_price[0])
            august_5_price = float(august_5_price[0])

            # Fetch today's price
            today_price = fetch_current_price(pair)
            print(f"Today's price for {pair}: {today_price}")

            if today_price is not None:
                # Calculate ROI
                roi_august = calculate_roi(july_5_price, august_5_price)
                roi_today = calculate_roi(august_5_price, today_price)
                
                print(f"ROI for {pair}: ROI from July to August: {roi_august}, ROI today: {roi_today}")
                
                return {
                    'symbol': symbol,
                    'pair_type': pair_type,  # 'BTC' or 'ETH'
                    'july_5_price': july_5_price,
                    'august_5_price': august_5_price,
                    'today_price': today_price,
                    'roi_august': roi_august,
                    'roi_today': roi_today
                }
    else:
        print(f"Could not fetch historical data for {pair}.")
    return None

def process_symbol(symbol, start_date, end_date):
    """Process historical data and calculate ROI for both BTC and ETH pairs for a given symbol."""
    result_btc = process_pair(symbol, start_date, end_date, 'BTC')
    result_eth = process_pair(symbol, start_date, end_date, 'ETH')

    if result_btc and result_eth:
        # Check if both BTC and ETH pairs are making higher lows
        if result_btc['august_5_price'] > result_btc['july_5_price'] and result_eth['august_5_price'] > result_eth['july_5_price']:
            print(f"{symbol} made higher lows on both BTC and ETH pairs.")
            return {
                'symbol': symbol,
                'btc_july_5_price': result_btc['july_5_price'],
                'btc_august_5_price': result_btc['august_5_price'],
                'btc_today_price': result_btc['today_price'],
                'btc_roi_august': result_btc['roi_august'],
                'btc_roi_today': result_btc['roi_today'],
                'eth_july_5_price': result_eth['july_5_price'],
                'eth_august_5_price': result_eth['august_5_price'],
                'eth_today_price': result_eth['today_price'],
                'eth_roi_august': result_eth['roi_august'],
                'eth_roi_today': result_eth['roi_today']
            }
    return None

def process_single_pair(symbol, start_date, end_date, pair_type):
    """Process historical data and check higher lows for a single pair (BTC or ETH)."""
    result = process_pair(symbol, start_date, end_date, pair_type)

    if result and result['august_5_price'] > result['july_5_price']:
        print(f"{symbol} made higher lows on {pair_type} pair.")
        return result
    return None

def main():
    altcoin_data = fetch_top_200_altcoins()
    if not altcoin_data:
        print("No altcoin data fetched.")
        return

    both_pairs_data = []
    one_pair_data = []

    # Start and end dates for analysis
    start_date = '2024-07-05'
    end_date = '2024-08-05'

    # Process coins with both BTC and ETH pairs
    for symbol in altcoin_data['both_pairs']:
        print(f"Processing {symbol}...")
        result = process_symbol(symbol, start_date, end_date)
        
        if result:
            both_pairs_data.append(result)

    # Process coins with only BTC pairs
    for symbol in altcoin_data['only_btc_pairs']:
        print(f"Processing {symbol} with only BTC pair...")
        result_btc = process_single_pair(symbol, start_date, end_date, 'BTC')
        if result_btc:
            one_pair_data.append(result_btc)

    # Process coins with only ETH pairs
    for symbol in altcoin_data['only_eth_pairs']:
        print(f"Processing {symbol} with only ETH pair...")
        result_eth = process_single_pair(symbol, start_date, end_date, 'ETH')
        if result_eth:
            one_pair_data.append(result_eth)

    # Create DataFrame for coins with both pairs
    both_pairs_df = pd.DataFrame(both_pairs_data)
    print(f"Coins with both pairs processed: {len(both_pairs_df)}")

    # Save top 20 coins with both BTC and ETH pairs by ROI
    if not both_pairs_df.empty:
        top_20_coins = both_pairs_df.sort_values(by='btc_roi_august', ascending=False).head(20)
        print(f"Saving top 20 coins with both BTC and ETH pairs making higher lows.")
        top_20_coins.to_csv('binance_api.csv', index=False)
        print("CSV file saved as 'binance_api.csv'.")
    else:
        print("No coins with higher lows for both BTC and ETH pairs were found.")

    # Create DataFrame for coins with only one pair
    one_pair_df = pd.DataFrame(one_pair_data)
    print(f"Coins with only one pair processed: {len(one_pair_df)}")

    # Save coins with only one pair
    if not one_pair_df.empty:
        one_pair_df.to_csv('only_one_pair.csv', index=False)
        print("CSV file saved as 'only_one_pair.csv'.")
    else:
        print("No coins with higher lows for single pairs were found.")

if __name__ == "__main__":
    main()
