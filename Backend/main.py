import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tensorflow import keras
from tokenizer import Tokenizer, preprocess_text
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # Set this to True if you want to allow credentials (e.g., cookies)
    allow_methods=["*"],  # You can specify HTTP methods here (e.g., ["GET", "POST"])
    allow_headers=["*"],  # You can specify HTTP headers here
)

tokenizer = Tokenizer()
tokenizer.load('tokenizer.json')
model = keras.models.load_model('model.keras')

def predict_sentiment(sentence: str) -> float:
    """
    Predict the sentiment of the given sentence
    :param sentence: input sentence
    :return: sentiment score
    """
    sentence = preprocess_text(sentence)
    tokens = tokenizer.transform_single(sentence)
    tokens = keras.preprocessing.sequence.pad_sequences([tokens], maxlen=20, padding='post', truncating='post')[0]
    sentiment_score = model.predict(tokens.reshape(1, 20))[0][0]
    sentiment_score = float(sentiment_score)
    return sentiment_score

@app.get("/")
async def root():
    return {"greeting": "Welcome    ", "message": "Go to /predict"}

@app.get('/predict')
async def predict(sentence: str):
    sentiment_score = predict_sentiment(sentence)
    sentiment = 'positive' if sentiment_score > 0.5 else 'negative'
    return {'sentence': sentence, 'sentiment_score': sentiment_score, 'sentiment': sentiment}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Sentiment Analysis API",
        version="1.0.0",
        description="This is a FastAPI application for sentiment analysis.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    from hypercorn.config import Config
    from hypercorn.asyncio import serve

    config = Config.from_str("host=localhost port=8000")
    serve(app, config)