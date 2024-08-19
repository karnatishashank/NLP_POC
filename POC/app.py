import os
from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
from src.data_ingestion import process_input
from src.nlp_processing import setup_nlp_pipeline, extract_entities, analyze_sentiment, analyze_text_structure
from src.multimodal_integration import setup_multimodal_model, analyze_multimodal
from src.clinical_decision_support import generate_clinical_summary

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for flash messages

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set up models
ner_pipe, sentiment_pipe, nlp = setup_nlp_pipeline()
multimodal_model, multimodal_processor = setup_multimodal_model()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text_input = request.form.get('text_input')
        file = request.files.get('file')
        
        if not text_input and not file:
            flash('Please provide either text input or a file.')
            return render_template('index.html')
        
        if text_input:
            text = process_input(text_input)
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            text = process_input(file)
        else:
            flash('Invalid file type')
            return render_template('index.html')
        
        # Analyze
        entities = extract_entities(text, ner_pipe, nlp) if text else []
        sentiment = analyze_sentiment(text, sentiment_pipe) if text else ('NEUTRAL', 0.5)
        text_structure = analyze_text_structure(text, nlp) if text else {}
        
        multimodal_result = None
        if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            try:
                multimodal_result = analyze_multimodal(file_path, text, multimodal_model, multimodal_processor)
            except Exception as e:
                flash(f'Error in multimodal analysis: {str(e)}')
        
        # Generate summary
        summary = generate_clinical_summary(entities, sentiment, text_structure, multimodal_result)
        
        return render_template('result.html', summary=summary, original_text=text[:500] + "..." if len(text) > 500 else text)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)