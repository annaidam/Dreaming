from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

# Initialize FastAPI app
app = FastAPI()

# cors to allow requests from fronten


# Load the dataset
dataset_path = "dataset.csv"  # Adjust the path if needed
dreams_data = pd.read_csv(dataset_path)

# Extract dream symbols and interpretations
dream_symbols = dreams_data["Dream Symbol"].tolist()
dream_interpretations = dreams_data["Interpretation"].tolist()

# Initialize the TF-IDF vectorizer and fit on the dataset
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(dream_interpretations)


# Request model for user input
class DreamRequest(BaseModel):
    description: str


# Endpoint to interpret a dream description
@app.post("/interpret")
async def interpret_dream(request: DreamRequest):
    user_input = request.description

    # Vectorize the user input
    user_vector = vectorizer.transform([user_input])

    # Compute cosine similarity
    similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()

    # Handle no matches
    if not similarities.size or max(similarities) <= 0:
        return {"detail": "No matching dream symbol found."}

    # Find the closest match
    closest_idx = np.argmax(similarities)
    predicted_symbol = dream_symbols[closest_idx]
    predicted_interpretation = dream_interpretations[closest_idx]

    return {"symbol": predicted_symbol, "interpretation": predicted_interpretation}
