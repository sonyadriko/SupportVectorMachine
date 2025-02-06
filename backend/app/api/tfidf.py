from flask_restx import Namespace, Resource, fields
from app.services.tfidf_calculator import TFIDFCalculator
import pandas as pd
import os

tfidf_ns = Namespace('tfidf', description='API for TF-IDF calculation')

# Model output
tfidf_response = tfidf_ns.model('TFIDFResponse', {
    'status': fields.String(description='Status penghitungan'),
    'file_vector_matrix': fields.String(description='Path file hasil vector matrix'),
    'file_labeled': fields.String(description='Path file hasil pelabelan'),
    'last_row': fields.Raw(description='Data baris terakhir dengan label')
})

# Model output untuk response membaca file
read_file_response = tfidf_ns.model('ReadFileResponse', {
    'status': fields.String(description='Status'),
    'data': fields.Raw(description='Data dari file tfidf dalam format JSON')
})


@tfidf_ns.route('/')
class TFIDFResource(Resource):
    @tfidf_ns.response(200, 'Success', tfidf_response)
    @tfidf_ns.response(500, 'Internal Server Error')
    def get(self):
        """Hitung TF-IDF dan simpan hasilnya"""
        try:
            # Initialize TFIDFCalculator
            preprocessed_data_path = "data/Text_Preprocessing.csv"
            tweet_data_path = "data/data_tweet.csv"
            vector_matrix_path = "data/hasil_vector_matrix.csv"
            labeled_data_path = "data/pelabelan.csv"
            tfidf_calculator = TFIDFCalculator(preprocessed_data_path, tweet_data_path, vector_matrix_path, labeled_data_path)

            # Run TF-IDF calculation
            last_row_data = tfidf_calculator.calculate_tfidf()

            return {
                "status": "TF-IDF berhasil dihitung",
                "file_vector_matrix": "hasil_vector_matrix.csv",
                "file_labeled": "pelabelan.csv",
                "last_row": last_row_data
            }, 200

        except Exception as e:
            return {"status": "Error", "message": str(e)}, 500

# Endpoint untuk membaca file hasil tfidf
@tfidf_ns.route('/read_tfidf')
class ReadPreprocessingResource(Resource):
    @tfidf_ns.response(200, 'Success', read_file_response)
    @tfidf_ns.response(404, 'File Not Found')
    @tfidf_ns.response(500, 'Internal Server Error')
    def get(self):
        """Membaca hasil preprocessing dari file Text_Preprocessing.csv"""
        try:
            # Path ke file hasil preprocessing
            file_path = "data/pelabelan.csv"
            
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
