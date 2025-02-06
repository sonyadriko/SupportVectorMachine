import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.preprocessing import normalize
import logging
import os

logger = logging.getLogger(__name__)

class TFIDFCalculator:
    def __init__(self, preprocessed_data_path, tweet_data_path, vector_matrix_path, labeled_data_path):
        self.preprocessed_data_path = preprocessed_data_path
        self.tweet_data_path = tweet_data_path
        self.vector_matrix_path = vector_matrix_path
        self.labeled_data_path = labeled_data_path

        # Load preprocessed data
        self.tweet_data = pd.read_csv(self.preprocessed_data_path, usecols=["stemmed"])
        self.tweet_data.columns = ["stemmed"]
        logger.info(f"Loaded preprocessed data from {self.preprocessed_data_path}")

        # Load original tweet data for labeling
        self.data_tweet = pd.read_csv(self.tweet_data_path)
        logger.info(f"Loaded tweet data from {self.tweet_data_path}")

    def calculate_tfidf(self):
        """Calculate TF-IDF and save the results"""
        # Join token lists into single strings
        self.tweet_data["tweet_join"] = self.tweet_data["stemmed"].apply(lambda x: ' '.join(eval(x)))
        logger.info("Token lists joined into single strings")

        # Initialize CountVectorizer and calculate TF vector
        cvect = CountVectorizer(max_features=50, lowercase=False)
        TF_vector = cvect.fit_transform(self.tweet_data["tweet_join"])
        logger.info("Calculated term frequency (TF) matrix")

        # Initialize TfidfTransformer and calculate TF-IDF matrix
        tfidf_transformer = TfidfTransformer(smooth_idf=False)
        tfidf_matrix = tfidf_transformer.fit_transform(TF_vector)

        # Normalize TF-IDF matrix
        normalized_tfidf_matrix = normalize(tfidf_matrix, norm='l1', axis=1)

        # Create DataFrame for TF-IDF results
        tfidf_df = pd.DataFrame(normalized_tfidf_matrix.toarray(), columns=cvect.get_feature_names_out())
        logger.info("Normalized and created TF-IDF DataFrame")

        # Save TF-IDF matrix to CSV
        tfidf_df.to_csv(self.vector_matrix_path, index=False)
        logger.info(f"Saved TF-IDF matrix to {self.vector_matrix_path}")

        # Label the data
        tfidf_df['status'] = self.data_tweet['status']
        tfidf_df['label'] = self.data_tweet['status'].apply(lambda x: 'negatif' if x in [1, 2] else 'positif')

        # Save labeled data
        tfidf_df.to_csv(self.labeled_data_path, index=False)
        logger.info(f"Saved labeled data to {self.labeled_data_path}")

        return tfidf_df.tail(1).to_dict(orient='records')
