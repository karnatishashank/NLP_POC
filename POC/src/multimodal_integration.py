from transformers import CLIPProcessor, CLIPModel
from PIL import Image

def setup_multimodal_model():
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    return model, processor

def analyze_multimodal(image_path, text, model, processor):
    image = Image.open(image_path)
    inputs = processor(text=[text], images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)
    return probs.detach().numpy()