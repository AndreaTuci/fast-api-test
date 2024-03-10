from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentiment_analysis import analyze_sentiment

class TextToAnalyze(BaseModel):
    text: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/analyze/")
async def analyze(text_to_analyze: TextToAnalyze):
    sentiment_result = analyze_sentiment(text_to_analyze.text)
    return {"sentiment": sentiment_result}
