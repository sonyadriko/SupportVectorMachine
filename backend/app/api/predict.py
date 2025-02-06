from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from app.services.predict_service import PredictService
from app.utils.model_loader import load_model

# Define Namespace for Predict API
predict_ns = Namespace('predict', description='API for sentiment prediction')

# Model for request input (expecting 'text')
predict_request = predict_ns.model('PredictRequest', {
    'text': fields.String(description='Input text for sentiment prediction', required=True)
})

# Model for Response (sentiment prediction, kernel matrix, and processed text)
predict_response = predict_ns.model('PredictResponse', {
    'sentimen': fields.List(fields.Integer, description='Sentiment prediction'),
    'kernel_matrix': fields.List(fields.List(fields.Float), description='Kernel matrix from the model'),
    'preprocess_text': fields.String(description='Processed input text')
})

# Load the pre-trained model, scaler, and TF-IDF vectorizer
model, scaler, tfidf_vectorizer = load_model()

# Define PredictResource (Endpoint for Prediction)
@predict_ns.route('/')
class PredictResource(Resource):
    @predict_ns.doc('Sentiment Prediction')
    @predict_ns.expect(predict_request)  # Request expects a 'text' input
    @predict_ns.response(200, 'Success', predict_response)
    @predict_ns.response(400, 'Bad Request')
    @predict_ns.response(500, 'Internal Server Error')
    def post(self):
        """Predict sentiment based on input text"""

        data = request.get_json()

        # Validate input data
        if not data or 'text' not in data:
            return {
                "error": "Invalid data",
                "message": "No text found in the input data."
            }, 400

        try:
            # Preprocess and filter the input text
            processed_text = PredictService.preprocess_text(data['text'])
            print(f"Processed text: {processed_text}")

            # Vectorize and standardize the text
            vectorized_text = PredictService.vectorize_and_standardize(processed_text)

            # Get sentiment prediction and kernel matrix
            prediction, kernel_matrix = PredictService.predict_sentiment(vectorized_text)

            # Return prediction results
            return {
                "sentimen": prediction,
                "kernel_matrix": kernel_matrix,
                "preprocess_text": processed_text
            }, 200

        except Exception as e:
            # Handle any errors that occur during prediction processing
            return {
                "error": "Error in prediction processing",
                "message": str(e)
            }, 500
