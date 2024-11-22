from transformers import pipeline

class NERModel:
    def __init__(self):
        # Load the pre-trained NER model from Hugging Face
        self.ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

    def predict(self, text):
        # Run NER on the input text
        entities = self.ner_pipeline(text)
        return entities
