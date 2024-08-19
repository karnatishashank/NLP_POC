from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
import spacy

def setup_nlp_pipeline():
    # Use a more general NER model
    ner_model_name = "dslim/bert-base-NER"
    ner_tokenizer = AutoTokenizer.from_pretrained(ner_model_name)
    ner_model = AutoModelForTokenClassification.from_pretrained(ner_model_name)
    ner_pipeline = pipeline("ner", model=ner_model, tokenizer=ner_tokenizer, aggregation_strategy="simple")
    
    # Use a general-purpose sentiment analysis model
    sentiment_pipeline = pipeline("sentiment-analysis")
    
    # Load spaCy model for additional text analysis
    nlp = spacy.load("en_core_web_sm")
    
    return ner_pipeline, sentiment_pipeline, nlp

def extract_entities(text, ner_pipe, nlp):
    # Get named entities from the NER pipeline
    ner_entities = ner_pipe(text)
    
    # Standardize NER entities
    standardized_ner = [{"entity_type": e.get('entity_group', 'UNKNOWN'), "word": e['word']} for e in ner_entities]
    
    # Use spaCy for additional entity recognition and noun phrase extraction
    doc = nlp(text)
    
    # Extract noun phrases
    noun_phrases = [{"entity_type": "NOUN_PHRASE", "word": chunk.text} for chunk in doc.noun_chunks]
    
    # Combine NER entities and noun phrases
    all_entities = standardized_ner + noun_phrases
    
    return all_entities

def analyze_sentiment(text, sentiment_pipe):
    result = sentiment_pipe(text)[0]
    return result['label'], result['score']

def analyze_text_structure(text, nlp):
    doc = nlp(text)
    
    # Analyze sentence structure
    sentences = [sent.text for sent in doc.sents]
    
    # Get key words (excluding stop words and punctuation)
    keywords = [token.text for token in doc if not token.is_stop and not token.is_punct]
    
    return {
        "sentence_count": len(sentences),
        "word_count": len(doc),
        "keywords": keywords[:10]  # Return top 10 keywords
    }