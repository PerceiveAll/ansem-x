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

You can install these libraries using pip:
```bash
pip install requests pandas
