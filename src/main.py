from fastapi import FastAPI, HTTPException
# Import the database functions
from populate_db import get_db_connection, query_word 
import json # Import json for potential pretty printing or manipulation if needed later

app = FastAPI()

@app.get("/query")
async def read_query(word: str):
    """Queries the database for the provided word and returns its data."""
    conn = None # Initialize conn to None
    try:
        conn = get_db_connection()
        if conn is None:
            # If connection fails, raise an internal server error
            raise HTTPException(status_code=500, detail="Database connection failed")

        # Query the database for the word
        word_data = query_word(conn, word.lower()) # Assuming words are stored lowercase

        if word_data:
            # If found, return the data (already in JSON format from DB)
            return word_data
        else:
            # If not found, raise a 404 error
            raise HTTPException(status_code=404, detail=f"Word '{word}' not found")

    except HTTPException as http_exc:
        # Re-raise HTTPExceptions directly
        raise http_exc
    except Exception as e:
        # Catch any other unexpected errors during query or connection
        print(f"An unexpected error occurred in /query endpoint: {e}") # Log the error server-side
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        # Ensure the connection is always closed
        if conn:
            conn.close()

# Optional: Add a root endpoint for basic info
@app.get("/")
async def root():
    return {"message": "Welcome to the Dictionary API. Use /query?word=your_word to search."}