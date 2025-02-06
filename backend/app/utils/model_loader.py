import pickle
import os

MODEL_PATH = 'data/models/'  # Path ke folder model

def load_model():
    """Load model, scaler, and tfidf vectorizer from .pkl files."""
    model, scaler, tfidf_vectorizer = None, None, None
    try:
        with open(os.path.join(MODEL_PATH, 'model.pkl'), 'rb') as model_file, \
             open(os.path.join(MODEL_PATH, 'scaler.pkl'), 'rb') as scaler_file, \
             open(os.path.join(MODEL_PATH, 'tfidf_vectorizer.pkl'), 'rb') as tfidf_file:
            model = pickle.load(model_file)
            scaler = pickle.load(scaler_file)
            tfidf_vectorizer = pickle.load(tfidf_file)
            print("Model, scaler, and tfidf_vectorizer loaded successfully.")
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
    
    return model, scaler, tfidf_vectorizer
