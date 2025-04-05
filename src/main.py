from fastapi import FastAPI

app = FastAPI()

@app.get("/query")
async def read_query(word: str = "default_word"):
    # In a real application, you would look up the word in a dictionary here.
    return {"word": word, "definition": f"Definition for {word}"}