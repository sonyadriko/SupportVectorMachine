import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from app.utils.model_loader import load_model

model, scaler, tfidf_vectorizer = load_model()

class PredictService:
    
    @staticmethod
    def preprocess_text(text):
        """Melakukan preprocessing terhadap teks input"""
        # Logika preprocessing seperti case folding, tokenization, stopword removal, dll
        processed_text = text.lower()  # Contoh, mengubah teks menjadi huruf kecil
        return processed_text

    @staticmethod
    def vectorize_and_standardize(text):
        """Melakukan vektorisasi dan standarisasi teks"""
        vectorized_text = tfidf_vectorizer.transform([text]).toarray()
        standardized_text = scaler.transform(vectorized_text)
        return standardized_text

    @staticmethod
    def predict_sentiment(standardized_text):
        """Melakukan prediksi sentimen dan mengembalikan matriks kernel"""
        prediction = model.predict(standardized_text).tolist()
        kernel_matrix = model.decision_function(standardized_text).tolist()
        return prediction, kernel_matrix
