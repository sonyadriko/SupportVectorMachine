import pandas as pd

def load_data(file_path):
    """Helper function to load data from CSV"""
    try:
        df = pd.read_csv(file_path, header=0)
        return df
    except Exception as e:
        raise Exception(f"Error loading data from {file_path}: {str(e)}")
