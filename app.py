from flask import Flask, render_template
import csv
import requests

app = Flask(__name__)

# CoinGecko API URL
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

# Load portfolio from CSV
def load_portfolio(csv_file):
    portfolio = []
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            portfolio.append({
                'ticker': row['Ticker'],
                'balance': float(row['Balance']),
                'cost': float(row['Cost'])
            })
    return portfolio

# Get prices from CoinGecko API
def get_crypto_prices(tickers):
    try:
        ids = ','.join(tickers)
        response = requests.get(COINGECKO_API_URL, params={'ids': ids, 'vs_currencies': 'usd', 'include_24hr_change': 'true'})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from CoinGecko API: {e}")
        return {}

@app.route('/')
def index():
    portfolio_data = load_portfolio('portfolio.csv')
    tickers = [item['ticker'] for item in portfolio_data]
    prices = get_crypto_prices(tickers)
    
    total_value = 0
    for item in portfolio_data:
        ticker = item['ticker']
        if ticker in prices:
            item['price'] = prices[ticker]['usd']
            item['value'] = item['balance'] * item['price']
            item['change_1h'] = prices[ticker].get('usd_1h_change', 'N/A')
            item['change_24h'] = prices[ticker].get('usd_24h_change', 'N/A')
            total_value += item['value']
        else:
            item['price'] = item['value'] = item['change_1h'] = item['change_24h'] = 'N/A'

        # Format change percentages to two decimal places and add '%' sign if they are not 'N/A'
        if item['change_1h'] != 'N/A':
            item['change_1h'] = f"{item['change_1h']:.2f}%"
        if item['change_24h'] != 'N/A':
            item['change_24h'] = f"{item['change_24h']:.2f}%"

    return render_template('index.html', portfolio=portfolio_data, total_value=total_value)

if __name__ == '__main__':
    app.run(debug=True)
