import json
import os
import sys # Add sys import for command-line arguments
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import Json

load_dotenv()

def get_db_connection():
    """Establishes a connection to the PostgreSQL database using DATABASE_URL."""
    database_url = os.getenv('DB_URL')
    if not database_url:
        print("Error: DATABASE_URL environment variable not set.")
        print("Please set the DATABASE_URL environment variable with your PostgreSQL connection string.")
        print("Example: postgresql://user:password@host:port/dbname")
        return None
    try:
        conn = psycopg2.connect(database_url)
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error connecting to the database using DATABASE_URL: {e}")
        print("Please ensure the DATABASE_URL is correct and the database is running.")
        return None

def create_table(conn):
    """Creates the words table if it doesn't exist."""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS words (
                word TEXT PRIMARY KEY,
                data JSONB
            );
        """)
    conn.commit()
    print("Table 'words' checked/created successfully.")

def populate_data(conn, data_file='dictionary_cache.json'):
    """Populates the words table from the JSON file."""
    try:
        with open(data_file, 'r') as f:
            word_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Data file '{data_file}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{data_file}'.")
        return

    total_words = len(word_data)
    print(f"Found {total_words} words in {data_file}.")

    insert_sql = """
        INSERT INTO words (word, data)
        VALUES (%s, %s)
        ON CONFLICT (word) DO UPDATE SET
            data = EXCLUDED.data;
    """

    with conn.cursor() as cur:
        for i, entry in enumerate(word_data):
            try:
                word = entry.get('word')
                if not word:
                    print(f"Skipping entry {i+1}/{total_words}: Missing 'word' key.")
                    continue

                # Use psycopg2.extras.Json to handle JSONB insertion correctly
                cur.execute(insert_sql, (word, Json(entry)))

                if (i + 1) % 100 == 0 or (i + 1) == total_words:
                    print(f"Processed {i + 1}/{total_words} words...")

            except Exception as e:
                print(f"Error processing entry for word '{entry.get('word', 'N/A')}': {e}")
                conn.rollback() # Rollback the specific problematic transaction part if needed
                # Decide if you want to continue or stop on error
                # continue

    conn.commit()
    print("Data population complete.")

def query_word(conn, word_to_find):
    """Queries the database for a specific word and returns its data."""
    select_sql = "SELECT data FROM words WHERE word = %s;"
    word_data = None
    with conn.cursor() as cur:
        try:
            cur.execute(select_sql, (word_to_find,))
            result = cur.fetchone()
            if result:
                word_data = result[0] # The data is in the first column
        except Exception as e:
            print(f"Error querying for word '{word_to_find}': {e}")
    return word_data

if __name__ == "__main__":
    # Check if a word is provided as a command-line argument
    if len(sys.argv) > 1:
        word_to_search = sys.argv[1]
        print(f"Attempting to query for word: '{word_to_search}'")
        conn = get_db_connection()
        if conn:
            try:
                # Query for the specific word
                retrieved_data = query_word(conn, word_to_search)
                if retrieved_data:
                    print("\n--- Found Word Data ---")
                    # Pretty print the JSON data
                    print(json.dumps(retrieved_data, indent=2))
                    print("-----------------------")
                else:
                    print(f"Word '{word_to_search}' not found in the database.")

            except Exception as e:
                print(f"An unexpected error occurred during query: {e}")
            finally:
                conn.close()
                print("Database connection closed.")
    else:
        # Default behavior: If no argument, maybe run population (or just print help)
        print("Usage: python src/populate_db.py <word_to_query>")
        print("To populate the database (run only if needed):")
        print("  Set POPULATE_DB=true environment variable and run: python src/populate_db.py")

        # Optional: Add logic to run population based on an env var
        if os.getenv("POPULATE_DB", "false").lower() == "true":
            print("\nPOPULATE_DB environment variable set to true. Running population...")
            conn = get_db_connection()
            if conn:
                try:
                    create_table(conn)
                    populate_data(conn)
                except Exception as e:
                    print(f"An unexpected error occurred during population: {e}")
                finally:
                    conn.close()
                    print("Database connection closed after population.")
