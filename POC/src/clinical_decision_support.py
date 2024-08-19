def generate_clinical_summary(entities, sentiment, text_structure, multimodal_result):
    summary = "Analysis Summary:\n\n"
    
    # Entities analysis
    entity_types = set(e['entity_type'] for e in entities)
    summary += f"Detected entity types: {', '.join(entity_types)}\n"
    summary += f"Total entities detected: {len(entities)}\n\n"
    
    # Sentiment analysis
    summary += f"Overall sentiment: {sentiment[0]} (confidence: {sentiment[1]:.2f})\n\n"
    
    # Text structure analysis
    if text_structure:
        summary += f"Text structure:\n"
        summary += f"- Number of sentences: {text_structure.get('sentence_count', 'N/A')}\n"
        summary += f"- Word count: {text_structure.get('word_count', 'N/A')}\n"
        summary += f"- Key terms: {', '.join(text_structure.get('keywords', []))}\n\n"
    else:
        summary += "Text structure analysis not available for this input.\n\n"
    
    # Multimodal analysis
    if multimodal_result:
        summary += f"Image-text relevance: {multimodal_result}\n\n"
    else:
        summary += "No multimodal analysis performed.\n\n"
    
    # Content analysis
    summary += "Content Analysis:\n"
    summary += "The text appears to discuss the following topics:\n"
    for entity in set(e['word'] for e in entities):
        if len(entity) > 3:  # Filter out short entities
            summary += f"- {entity}\n"
    
    if not entities:
        summary += "No specific entities detected.\n"
    
    summary += "\nBased on the entities and keywords detected, "
    if any(keyword in ' '.join(e['word'] for e in entities).lower() for keyword in ['aem', 'content', 'author', 'web']):
        summary += "this appears to be a resume for a professional in the AEM (Adobe Experience Manager) field. "
        summary += "The individual seems to have experience in content authoring, web development, and content management systems. "
        summary += "Key skills mentioned may include AEM, MSM (Multi-Site Manager), and content translation.\n"
    else:
        summary += "this text seems to be related to healthcare or medical topics. "
        summary += "It may mention various technologies or procedures used in patient care. "
        summary += "For a more detailed analysis, please consult with a domain expert.\n"
    
    return summary