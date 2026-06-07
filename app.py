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

@app.post("/sentiment")
def sentiment(req: SentimentRequest):
    results = []

    for sentence in req.sentences:
        text = sentence.lower()

        pos = sum(word in text for word in POSITIVE)
        neg = sum(word in text for word in NEGATIVE)

        if pos > neg:
            label = "happy"
        elif neg > pos:
            label = "sad"
        else:
            label = "neutral"

        results.append({
            "sentence": sentence,
            "sentiment": label
        })

    return {"results": results}