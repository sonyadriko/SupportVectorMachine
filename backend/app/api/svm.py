from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from app.services.svm_service import train_and_evaluate

# Define Namespace for SVM API
svm_ns = Namespace('svm', description='Train and evaluate an SVM model with a confusion matrix')

# Request Model (Input)
svm_request_model = svm_ns.model('SVMRequest', {
    'test_size': fields.Float(required=False, description="Test data proportion (default: 0.2)", example=0.2),
    'gamma': fields.Float(required=False, description="Gamma value for SVM (default: 'scale')", example=0.1),
    'lambda': fields.Float(required=False, description="Regularization parameter C (default: 1.0)", example=1.0),
    'complexity': fields.Float(required=False, description="Coef0 parameter for SVM kernel (default: 0.0)", example=0.0)
})

# Response Model (Output)
svm_response_model = svm_ns.model('SVMResponse', {
    'accuracy': fields.Float(description='Accuracy of the SVM model'),
    'confusion_matrix': fields.List(fields.List(fields.Integer), description="2D list representing confusion matrix"),
    'tn': fields.Integer(description='True Negative count'),
    'fp': fields.Integer(description='False Positive count'),
    'fn': fields.Integer(description='False Negative count'),
    'tp': fields.Integer(description='True Positive count'),
    'classification_report': fields.String(description='Classification report as string'),
    'precision': fields.Float(description='Precision score of the model'),
    'f1_score': fields.Float(description='F1 score of the model'),
    'recall': fields.Float(description='Recall score of the model'),
    'total_data': fields.Integer(description='Total number of data points used for testing')
})

# Define SVMResource (Endpoint for SVM Training and Prediction)
@svm_ns.route('/')
class SVMResource(Resource):
    @svm_ns.doc('Train and Evaluate SVM Model')
    @svm_ns.expect(svm_request_model)  # Define expected input
    @svm_ns.response(200, 'Success', svm_response_model)
    @svm_ns.response(400, 'Bad Request')
    @svm_ns.response(500, 'Internal Server Error')
    def post(self):
        """Train and evaluate SVM model, and return evaluation results."""
        
        try:
            # Get request data as JSON
            data = request.get_json()

            # Validate and get parameters
            test_size = data.get('test_size', 0.2)
            gamma = data.get('gamma', 0.1)  # Default to 0.1 instead of 'scale' for consistency
            C = data.get('lambda', 1.0)
            coef0 = data.get('complexity', 0.0)

            # Call the SVMService for processing
            result = train_and_evaluate(test_size, gamma, C, coef0)

            return result, 200  # Return JSON response with status 200

        except Exception as e:
            svm_ns.logger.error(f"Error processing SVM request: {str(e)}")
            return {"error": f"Error processing SVM request: {str(e)}"}, 500
