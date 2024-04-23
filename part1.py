import os
import requests
import json
import sys
import sqlite3

def fetch_bitcoin_price():
    # Define the URL to fetch Bitcoin price data
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    try:
        # Make a GET request to fetch Bitcoin price data
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response into a Python dictionary
            data = response.json()
            # Extract relevant information from the response
            time_updated = data['time']['updated']
            bitcoin_price_usd = data['bpi']['USD']['rate']
            # Print the extracted information
            print("Time Updated:", time_updated)
            print("Bitcoin Price (USD):", bitcoin_price_usd)
        else:
            # Print an error message if the request was unsuccessful
            print("Failed to retrieve Bitcoin price. Status code:", response.status_code)
    except requests.RequestException as e:
        # Handle exceptions if there's an error making the request
        print("Error making request:", e)

def get_transactions(endpoint, start_block, end_block):
    url = endpoint
    headers = {
        'Content-Type': 'application/json',
    }

    transactions = []
    for block_num in range(start_block, end_block + 1):
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getBlockByNumber",
            "params": [hex(block_num), True],
            "id": 1
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            data = response.json()
            if 'result' in data and data['result'] is not None:
                transactions.extend(data['result']['transactions'])

    return transactions

def persist_to_sqlite(transactions, db_file):
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        
        # Create table if not exists
        c.execute('''CREATE TABLE IF NOT EXISTS transactions
                     (hash TEXT PRIMARY KEY, blockHash TEXT, blockNumber TEXT, sender TEXT, receiver TEXT, value TEXT)''')
        
        # Insert transactions into the table
        for tx in transactions:
            c.execute('''INSERT OR IGNORE INTO transactions VALUES (?, ?, ?, ?, ?, ?)''', 
                      (tx['hash'], tx['blockHash'], tx['blockNumber'], tx['from'], tx['to'], tx['value']))
        
        # Commit changes
        conn.commit()
    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        # Close the database connection
        if conn:
            conn.close()

# Example usage:
# persist_to_sqlite(transactions, 'ethereum_transactions.db')

if __name__ == "__main__":
    # Check if the correct number of command-line arguments are provided
    if len(sys.argv) != 4:
        print("Usage: python part1.py <JSON-RPC endpoint> <SQLite file> <block range>")
        sys.exit(1)
    # Parse command-line arguments
    endpoint = sys.argv[1]
    db_file = sys.argv[2]
    block_range = sys.argv[3].split('-')
    start_block = int(block_range[0])
    end_block = int(block_range[1])
    # Fetch Bitcoin price information
    fetch_bitcoin_price()
    # Retrieve Ethereum transactions and persist them to SQLite database
    transactions = get_transactions(endpoint, start_block, end_block)
    persist_to_sqlite(transactions, db_file)
