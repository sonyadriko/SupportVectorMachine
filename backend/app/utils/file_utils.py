import os

def save_model(model, file_path):
    """Menyimpan model ke file"""
    folder = os.path.dirname(file_path)
    if not os.path.exists(folder):
        os.makedirs(folder)  # Membuat folder jika belum ada
    with open(file_path, 'wb') as file:
        pickle.dump(model, file)
