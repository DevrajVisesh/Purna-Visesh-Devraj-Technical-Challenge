import sys
import sqlite3

def query_largest_volume_block(sqlite_file, start_time, end_time):
    # Connect to the SQLite database
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    # Construct SQL query to retrieve transactions within the specified time range
    sql_query = """
        SELECT blockNumber, SUM(value) AS volume
        FROM transactions
        WHERE blockNumber BETWEEN ? AND ?
        GROUP BY blockNumber
        ORDER BY volume DESC
        LIMIT 1
    """
    # Execute the SQL query with the provided start and end times
    c.execute(sql_query, (start_time, end_time))
    # Fetch the query result
    result = c.fetchone()
    # Display the result
    if result:
        block_number, volume = result
        print(f"Largest volume block within {start_time} and {end_time}:")
        print(f"Block Number: {block_number}")
        print(f"Volume: {volume}")
    else:
        print("No transactions found within the specified time range.")
    # Close the database connection
    conn.close()

if __name__ == "__main__":
    # Check if the correct number of command-line arguments are provided
    if len(sys.argv) != 4:
        print("Usage: python part2.py <SQLite file> <start_time> <end_time>")
        sys.exit(1)
    # Parse command-line arguments
    sqlite_file = sys.argv[1]
    start_time = sys.argv[2]
    end_time = sys.argv[3]
    # Query the largest volume block within the specified time range
    query_largest_volume_block(sqlite_file, start_time, end_time)
