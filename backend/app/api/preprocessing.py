from flask_restx import Namespace, Resource, fields
from flask import send_from_directory, jsonify
import os
import pandas as pd
from app.services.text_preprocessing import TextPreprocessor

# Define Namespace
preprocessing_ns = Namespace('preprocessing', description='API for text preprocessing')

# Model output untuk response sukses
preprocessing_response = preprocessing_ns.model('PreprocessingResponse', {
    'message': fields.String(description='Status pesan'),
    'file': fields.String(description='Path file hasil preprocessing')
})

# Model output untuk response membaca file
read_file_response = preprocessing_ns.model('ReadFileResponse', {
    'status': fields.String(description='Status'),
    'data': fields.Raw(description='Data dari file preprocessing dalam format JSON')
})

# Endpoint untuk Preprocessing
@preprocessing_ns.route('/')
class PreprocessingResource(Resource):
    @preprocessing_ns.response(200, 'Success', preprocessing_response)
    @preprocessing_ns.response(500, 'Internal Server Error')
    def get(self):
        """Perform preprocessing on tweet data"""
        try:
            # Path file yang dibutuhkan untuk preprocessing
            tweet_data_path = "data/data_tweet.csv"
            stopwords_path = "data/stopwords.txt"
            normalization_path = "data/normalisasi.txt"

            # Inisialisasi Preprocessor
            preprocessor = TextPreprocessor(tweet_data_path, stopwords_path, normalization_path)

            # Menjalankan proses preprocessing
            processed_file = preprocessor.preprocess()

            return {
                "message": "Preprocessing berhasil",
                "file": processed_file
            }, 200

        except Exception as e:
            return {"message": f"Error: {str(e)}"}, 500

# Endpoint untuk membaca file hasil preprocessing
@preprocessing_ns.route('/read_preprocessing')
class ReadPreprocessingResource(Resource):
    @preprocessing_ns.response(200, 'Success', read_file_response)
    @preprocessing_ns.response(404, 'File Not Found')
    @preprocessing_ns.response(500, 'Internal Server Error')
    def get(self):
        """Membaca hasil preprocessing dari file Text_Preprocessing.csv"""
        try:
            # Path ke file hasil preprocessing
            file_path = "data/Text_Preprocessing.csv"
            
            # Cek apakah file ada
            if not os.path.exists(file_path):
                return {"status": "Error", "message": "File tidak ditemukan"}, 404

            # Membaca data dari file CSV
            data = pd.read_csv(file_path)

            # Mengonversi dataframe ke format JSON
            data_json = data.to_dict(orient='records')

            return {
                "status": "Success",
                "data": data_json
            }, 200

        except Exception as e:
            return {"status": "Error", "message": str(e)}, 500
