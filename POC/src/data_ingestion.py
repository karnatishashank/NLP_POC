import cv2
import pytesseract
from PIL import Image
import PyPDF2

def process_input(file_path):
    if isinstance(file_path, str):
        # This is a text input
        return file_path
    elif file_path.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        # Process image input
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
    elif file_path.filename.lower().endswith('.pdf'):
        # Process PDF input
        pdf_reader = PyPDF2.PdfReader(file_path)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    elif file_path.filename.lower().endswith('.txt'):
        # Process text file
        text = file_path.read().decode('utf-8')
    else:
        text = "Unsupported file type"
    
    return text