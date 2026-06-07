from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: List[str]

POSITIVE = {
    "love", "great", "excellent", "amazing", "awesome",
    "happy", "good", "fantastic", "wonderful", "best"
}

NEGATIVE = {
    "hate", "terrible", "awful", "bad", "worst",
    "sad", "angry", "horrible", "poor", "disappointed"
}

@app.get("/")
def root():
    return {"status": "ok"}

from textblob import TextBlob

@app.post("/sentiment")
def sentiment(req: SentimentRequest):
    results = []

    for sentence in req.sentences:
        polarity = TextBlob(sentence).sentiment.polarity

        if polarity > 0.1:
            sentiment = "happy"
        elif polarity < -0.1:
            sentiment = "sad"
        else:
            sentiment = "neutral"

        results.append({
            "sentence": sentence,
            "sentiment": sentiment
        })

    return {"results": results}