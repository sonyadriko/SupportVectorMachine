import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import os
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, precision_score, f1_score, recall_score
from app.utils.data_loader import load_data
from sklearn.preprocessing import LabelEncoder

MODEL_PATH = 'data/models/'  # Path ke folder model

def initialize_model():
    """Initialize and return the SVM model."""
    return SVC(kernel='linear', probability=True)

def train_sequential_svm():
    """Train the Sequential SVM model and save it to files."""
    # Membaca dataset
    df = pd.read_csv("data/data_tweet.csv", header=0)
    
    # Menentukan fitur (X) dan label (y)
    X = df['rawContent'].values  # Kolom 'rawContent' berisi teks
    y = df['label'].values

    # Mengubah teks menjadi format yang sesuai untuk model menggunakan TF-IDF
    tfidf_vectorizer = TfidfVectorizer()
    X_tfidf = tfidf_vectorizer.fit_transform(X)
    
    # Menstandarisasi fitur
    scaler = StandardScaler(with_mean=False)
    X_scaled = scaler.fit_transform(X_tfidf)

    # Menginisialisasi dan melatih model
    model = initialize_model()
    model.fit(X_scaled, y)
    
    # Membuat direktori untuk menyimpan model jika belum ada
    os.makedirs(MODEL_PATH, exist_ok=True)

    # Menyimpan model, scaler, dan TF-IDF vectorizer
    with open(os.path.join(MODEL_PATH, 'model.pkl'), 'wb') as model_file, \
         open(os.path.join(MODEL_PATH, 'scaler.pkl'), 'wb') as scaler_file, \
         open(os.path.join(MODEL_PATH, 'tfidf_vectorizer.pkl'), 'wb') as tfidf_file:
        pickle.dump(model, model_file)
        pickle.dump(scaler, scaler_file)
        pickle.dump(tfidf_vectorizer, tfidf_file)

    return "Pelatihan Sequential SVM berhasil"

def train_and_evaluate(test_size, gamma, C, coef0):
        try:
            # Load the dataset
            df = load_data("data/pelabelan.csv")
            total_data = df.shape[0]
            
            # Encode labels
            label_encoder = LabelEncoder()
            df['label'] = label_encoder.fit_transform(df['label'])
            
            # Prepare features and labels
            X = df.drop(columns=['status', 'label'])
            y = df['label']
            
            XNum = X.astype(np.float64)
            yNum = y.astype(np.float64)

            # Check if there's more than one class
            if len(np.unique(yNum)) <= 1:
                return {"error": "Number of classes must be greater than 1"}

            # Split the dataset
            X_train, X_test, y_train, y_test = train_test_split(XNum, yNum, test_size=test_size, random_state=42)

            # Initialize the SVM model
            svm_model = SVC(kernel='poly', gamma=gamma, C=C, coef0=coef0)
            svm_model.fit(X_train, y_train)

            # Predict on the test set
            y_pred = svm_model.predict(X_test)

            # Compute confusion matrix and classification report
            cm = confusion_matrix(y_test, y_pred)
            classification_rep = classification_report(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)

            # Extract TN, FP, FN, TP
            tn, fp, fn, tp = cm.ravel() if cm.shape == (2, 2) else (0, 0, 0, 0)

            # Calculate accuracy
            accuracy = np.mean(y_pred == y_test)

            return {
                "accuracy": accuracy,
                "confusion_matrix": cm.tolist(),
                "tn": int(tn),
                "fp": int(fp),
                "fn": int(fn),
                "tp": int(tp),
                "classification_report": classification_rep,
                "precision": precision,
                "f1_score": f1,
                "recall": recall,
                "total_data": total_data * test_size
            }

        except Exception as e:
            raise Exception(f"Error in training or evaluating the model: {str(e)}")
