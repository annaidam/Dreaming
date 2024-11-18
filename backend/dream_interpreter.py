import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the dataset
dataset_path = "dataset.csv"  # Adjust the path if needed
dreams_data = pd.read_csv(dataset_path)

# Extract dream symbols and interpretations
dream_symbols = dreams_data["Dream Symbol"].tolist()
dream_interpretations = dreams_data["Interpretation"].tolist()

# New input example
user_input = input("Enter your dream description: ")

# Step 1: Preprocess and Vectorize the text using TF-IDF
vectorizer = TfidfVectorizer(stop_words="english")
all_text = dream_interpretations + [user_input]
tfidf_matrix = vectorizer.fit_transform(all_text)

# Step 2: Calculate similarity between user input and interpretations
user_vector = tfidf_matrix[-1]  # User input vector
interpretation_vectors = tfidf_matrix[:-1]  # Pre-existing interpretations

# Compute cosine similarity
similarities = cosine_similarity(user_vector, interpretation_vectors).flatten()

# Step 3: Find the closest match
closest_idx = np.argmax(similarities)
predicted_symbol = dream_symbols[closest_idx]
predicted_interpretation = dream_interpretations[closest_idx]

# Display the results
print(f"\nDream Symbol: {predicted_symbol}")
print(f"Interpretation: {predicted_interpretation}")
