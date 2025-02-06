from flask import Blueprint
from flask_restx import Api

# Create Blueprint
api_bp = Blueprint('api', __name__)
api = Api(
    api_bp,
    version='1.0',
    title='Sentiment Analysis API',
    description='API for sentiment analysis using KNN method',
    doc='/swagger'  # Swagger aktif di /api/swagger
)

# Import namespaces
from .data_training import data_training_ns
from .preprocessing import preprocessing_ns
from .tfidf import tfidf_ns
from .predict import predict_ns
from .train import train_ns
from .svm import svm_ns

# Add namespaces
api.add_namespace(data_training_ns, path='/data_training')
api.add_namespace(preprocessing_ns, path='/preprocessing')
api.add_namespace(tfidf_ns, path='/tfidf')
api.add_namespace(predict_ns, path='/predict')
api.add_namespace(train_ns, path='/train')
api.add_namespace(svm_ns, path='/svm')