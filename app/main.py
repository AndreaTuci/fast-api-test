from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentiment_analysis import analyze_sentiment
import spacy
from transformers import pipeline
from utils import *
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification


class TextToAnalyze(BaseModel):
    text: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/analyze/")
async def analyze(text_to_analyze: TextToAnalyze):
    try:
        sentiment_result = analyze_sentiment(text_to_analyze.text)
        print_rich_info(sentiment_result)
        return {"sentiment": sentiment_result}
    except Exception as e:
        print_exception()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze-with-spacy/")
async def analyze_with_spacy(text_to_analyze: TextToAnalyze):
    try:
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text_to_analyze.text)
        print_rich_info(doc)
        return {"response": "success"}
    except Exception as e:
        print_exception()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-with-transformers/")
async def analyze_with_transformers(text_to_analyze: TextToAnalyze):
    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
    model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

    try:
        inputs = tokenizer(text_to_analyze.text, return_tensors="pt", padding=True, truncation=True)
        outputs = model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=-1)
        predicted_label_id = torch.argmax(probabilities).item()
        predicted_label = model.config.id2label.get(predicted_label_id, "Unknown Label")
        print_rich_info(predicted_label)
        return predicted_label
    except Exception as e:
        print_exception()
        raise HTTPException(status_code=500, detail=str(e))
