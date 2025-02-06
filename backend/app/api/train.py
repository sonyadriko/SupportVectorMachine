from flask import jsonify
from flask_restx import Namespace, Resource, fields
from app.services.svm_service import train_sequential_svm

# Swagger API setup
train_ns = Namespace('train', description='Operations related to Sequential SVM model training')
# Define model input and output
training_response = train_ns.model('TrainingResponse', {
    'message': fields.String(description='Status pesan pelatihan model'),
})

@train_ns.route('/')
class TrainSVM(Resource):
    @train_ns.doc('train_svm')
    @train_ns.response(200, 'Pelatihan Model SVM berhasil', training_response)
    @train_ns.response(500, 'Terjadi kesalahan saat pelatihan')
    def post(self):
        """
        Melatih model Sequential SVM dengan dataset tweet dan menyimpan model, scaler, serta tf-idf vectorizer.
        """
        try:
            # Melatih model Sequential SVM
            result = train_sequential_svm()
            return ({"message": result}), 200
        except Exception as e:
            print(f"Error during training: {str(e)}")
            return ({"error": "Pelatihan model gagal", "message": str(e)}), 500
