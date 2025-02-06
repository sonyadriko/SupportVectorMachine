import pandas as pd
import re
import string
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import logging

logger = logging.getLogger(__name__)

class TextPreprocessor:
    def __init__(self, tweet_data_path, stopwords_path, normalization_path):
        self.tweet_data_path = tweet_data_path
        self.stopwords_path = stopwords_path
        self.normalization_path = normalization_path

        self.df = pd.read_csv(self.tweet_data_path)
        logger.info(f"Loaded dataset from {self.tweet_data_path}")

        # Load stopwords
        self.stopwords = set(stopwords.words('indonesian'))
        self.load_additional_stopwords()

        # Load normalization dictionary
        self.normalization_dict = self.load_normalization_dict()

        # Initialize Stemmer
        factory = StemmerFactory()
        self.stemmer = factory.create_stemmer()

    def load_additional_stopwords(self):
        """Load additional stopwords from a file"""
        if os.path.exists(self.stopwords_path):
            with open(self.stopwords_path, "r") as file:
                additional_stopwords = file.read().splitlines()
            self.stopwords.update(additional_stopwords)
            logger.info(f"Loaded {len(additional_stopwords)} additional stopwords.")

    def load_normalization_dict(self):
        """Load the normalization dictionary from file"""
        normalization_dict = {}
        if os.path.exists(self.normalization_path):
            with open(self.normalization_path, 'r') as file:
                for line in file:
                    if ':' in line:
                        parts = line.strip().split(': ')
                        if len(parts) == 2:
                            normalization_dict[parts[0]] = parts[1]
            logger.info(f"Loaded normalization dictionary with {len(normalization_dict)} entries.")
        return normalization_dict

    def clean_text(self, text):
        """Clean the tweet text"""
        text = text.lower()
        text = re.sub(r"\\t|\\n|\\u|\\", " ", text)
        text = re.sub(r"([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)", " ", text)
        text = re.sub(r"[.!&,/@#$%^*\-]+", " ", text)
        text = re.sub(r"\d+", "", text)
        text = text.translate(str.maketrans("", "", string.punctuation))
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def preprocess(self):
        """Run preprocessing pipeline"""
        # Case Folding
        self.df['caseFolding'] = self.df['rawContent'].str.lower()
        logger.info("Applied case folding")

        # Cleaning
        self.df['cleaning'] = self.df['caseFolding'].apply(self.clean_text)
        logger.info("Applied text cleaning")

        # Tokenizing
        self.df['tokenizing'] = self.df['cleaning'].apply(word_tokenize)
        logger.info("Tokenized the text")

        # Stopword Removal
        self.df['stopword'] = self.df['tokenizing'].apply(
            lambda tokens: [word for word in tokens if word not in self.stopwords]
        )
        logger.info("Removed stopwords")

        # Normalization
        self.df['normalized'] = self.df['stopword'].apply(
            lambda tokens: [self.normalization_dict.get(word, word) for word in tokens]
        )
        logger.info("Applied normalization")

        # Stemming
        self.df['stemmed'] = self.df['normalized'].apply(
            lambda tokens: [self.stemmer.stem(word) for word in tokens]
        )
        logger.info("Applied stemming")

        # Save processed data
        processed_file_path = "data/Text_Preprocessing.csv"
        self.df.to_csv(processed_file_path, index=False)
        logger.info(f"Saved preprocessed data to {processed_file_path}")

        return processed_file_path
