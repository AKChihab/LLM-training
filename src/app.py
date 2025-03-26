#app.py
from fastapi import FastAPI, HTTPException
import asyncio
from src.scripts.chat_crypto_trend import main as chat_main  # import your main logic

app = FastAPI()

@app.get("/")
async def read_root():
    try:
        result = await chat_main()  # Call your asynchronous main function
        return {"result": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    