import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from fastapi import FastAPI
import tensorflow as tf
import numpy as np

app = FastAPI()
tokenizer = tf.keras.preprocessing.text.Tokenizer(filters='\t\n', char_level=True)

@app.get("/")
async def root():
    return {"message": "Hello World"}
    
def detect(url):
    url_label = url
    tokenizer.fit_on_texts(url)
    url = tokenizer.texts_to_sequences([url])
    url = tf.keras.preprocessing.sequence.pad_sequences(url, maxlen=500)
    model = tf.keras.models.load_model('api_rnn/model.keras')
    probs = model.predict(url)
    percent_label = f'{np.max(probs):.2%}'
    preds_label = 'good' if probs > 0.5 else 'bad'
    return {'url':url_label,'probs': str(percent_label), 'preds': preds_label}

@app.post("/detect")
def create_items(url: str):
    pred = detect(url)
    return pred

