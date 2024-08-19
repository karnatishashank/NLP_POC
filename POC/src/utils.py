import os
from werkzeug.utils import secure_filename

def save_uploaded_file(file, upload_folder):
    if file and file.filename:
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return file_path
    return None