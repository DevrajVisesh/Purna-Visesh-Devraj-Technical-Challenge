# Purna Visesh Devraj Technical Challenge

# Ethereum Transaction Analysis

This project comprises two parts:

Part 1: A Python script to retrieve Ethereum transactions within a given block range and persist them to a SQLite database.
Part 2: Another Python script to query the populated database for the block that had the largest volume of ether transferred within a specific time frame.


# Part 1: Ethereum Transaction Retrieval

Dependencies:

Python 3.x
requests library
SQLite3

# Usage

To run the script, use the following command format:

python part1.py <JSON-RPC endpoint> <SQLite file> <block range>

- <JSON-RPC endpoint>: The JSON-RPC endpoint to call an Ethereum client.
- <SQLite file>: The path to the SQLite database file to write the transactions to.
- <block range>: The range of Ethereum blocks to retrieve transactions from, specified as <start>-<end>.

Example: python part1.py https://rpc.example.com ethereum_transactions.db 100-200

# Part 2: Ethereum Transaction Analysis

Dependencies:

Python 3.x
SQLite3

# Usage

To run the script, use the following command format:

python part2.py <SQLite file> <start_time> <end_time> <output_file>

- <SQLite file>: The path to the SQLite database file containing the transactions.
- <start_time>: The start time of the time frame to analyze (format: "YYYY-MM-DD HH:MM:SS").
- <end_time>: The end time of the time frame to analyze (format: "YYYY-MM-DD HH:MM:SS").
- <output_file>: The path to the output file to write the analysis results to.

Example: python part2.py ethereum_transactions.db "2024-01-01 00:00:00" "2024-01-01 00:30:00" output.txt

Additional Notes:

- Ensure that you have proper permissions to write to the SQLite file and that the JSON-RPC endpoint is accessible.
- The scripts provide error handling for common issues such as incorrect command-line arguments or failed API requests.


