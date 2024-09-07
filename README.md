# Altcoin Analysis Script

## Overview
This Python script fetches the top 200 altcoins by trading volume on Binance, checks if they're making **higher lows** on both BTC and ETH trading pairs (or only one pair if that's all they have), calculates the **Return on Investment (ROI)**, and outputs the results into CSV files. It’s designed to help crypto traders and analysts quickly identify potential altcoins that are performing well against BTC and ETH over a specific time period.

### What It Does
1. Fetches the top 200 altcoins by volume from Binance.
2. Analyzes their **BTC and ETH pairs** to check for **higher lows** between **July 5, 2024** and **August 5, 2024**.
3. Calculates the **ROI** from July 5 to August 5, as well as from August 5 to the current date.
4. Outputs two CSV files:
   - **`binance_api.csv`**: Contains the top 20 altcoins with both BTC and ETH pairs making higher lows.
   - **`only_one_pair.csv`**: Contains altcoins that have only one pair (BTC or ETH) but are still making higher lows.

## Features
- **Historical Price Analysis**: The script fetches historical candlestick data to identify higher lows between two specific dates.
- **Return on Investment Calculation**: It calculates the ROI over two periods: July 5 to August 5 and August 5 to the present day.
- **CSV Export**: Outputs results to CSV files for easy analysis and sharing.

## Requirements
You will need the following installed:
- Python 3.x
- The following Python libraries:
  - `requests`
  - `pandas`
 
  ## Setup Instructions
## 1. Get Your Binance API Key
You will need a Binance API key to run this script. You can create an API key by signing into your Binance account and navigating to the API Management section.

## 2. Clone This Repository
Clone the repository to your local machine:

git clone https://github.com/YourUsername/altcoin-analysis.git
cd altcoin-analysis

## 3. Update the Binance API Key
Replace the placeholder Binance API key in the script with your actual key. Open the altcoin_analysis.py file and find this line:

BINANCE_API_KEY = 'your-binance-api-key-here'

Replace 'your-binance-api-key-here' with your real Binance API key.

## 4. Run the Script
After setting up the dependencies and API key, you can run the script:

python altcoin_analysis.py

## 5. View the Results
- ** The script will create two CSV files:
   - ** binance_api.csv: Contains the top 20 altcoins with both BTC and ETH pairs making higher lows.
   - ** only_one_pair.csv: Contains altcoins with only one pair (either BTC or ETH) but still making higher lows.

## How the Script Works
1. Fetch Top 200 Altcoins: The script uses Binance’s API to retrieve the top 200 altcoins by volume. It then separates them into three categories:

- ** Altcoins that have both BTC and ETH pairs.
- ** Altcoins that have only a BTC pair.
- ** Altcoins that have only an ETH pair.
2. Check for Higher Lows: For each altcoin, the script checks whether the low price on August 5, 2024 is higher than the low price on July 5, 2024. This is done for both the BTC and ETH pairs.

## 3. ROI Calculation:

- ** The script calculates two ROIs:
   - ** ROI from July 5 to August 5.
   - ** ROI from August 5 to today’s price.
- ** These calculations help identify the best-performing altcoins over this period.

4. CSV Output:

- ** The results are saved in two CSV files:
   - ** binance_api.csv: Top 20 altcoins where both BTC and ETH pairs are making higher lows.
   - ** only_one_pair.csv: Altcoins that have only a BTC or ETH pair but are still making higher lows.

## Example Output
The CSV files will contain the following columns for each altcoin:

- ** symbol: The altcoin symbol.
- ** july_5_price: The low price on July 5, 2024, for the pair (BTC/ETH).
- ** august_5_price: The low price on August 5, 2024, for the pair (BTC/ETH).
- ** today_price: The current price for the pair (BTC/ETH).
- ** roi_august: The ROI from July 5 to August 5.
- ** roi_today: The ROI from August 5 to the current date.

## Notes
- ** Binance Rate Limits: Binance has rate limits for API requests, so the script includes pauses to comply with these limits.
- ** Error Handling: If any API request fails, the script will print an error message and skip that coin.

## Future Improvements
- ** Adding more detailed logging for errors and performance analysis.
- ** Allowing for customizable date ranges and pairs.
- ** Enhancing performance with asynchronous requests.

You can install these libraries using pip:
```bash
pip install requests pandas

