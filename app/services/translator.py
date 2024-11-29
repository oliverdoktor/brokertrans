"""Translation service implementation."""
from typing import Optional
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from app.config import settings
from app.services.func import get_device_with_most_memory, extract_placeholders, restore_placeholders, prepare_text
import gc

class TranslatorService:
    """Service for handling translation operations."""
    
    def __init__(self):
        """Initialize the translator service."""
        self.model = None
        self.tokenizer = None
        
    def load_model(self) -> None:
        """Load the translation model and tokenizer."""
        if self.model is None:
            if settings.DEVICE == "automatic":
                self.device = get_device_with_most_memory()
            else:
                self.device = settings.DEVICE
            
            self.model = AutoModelForSeq2SeqLM.from_pretrained(settings.MODEL_NAME)
            self.tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_NAME)
            self.model.to(self.device)
    
    def unload_model(self) -> None:
        """Unload the model and free up resources."""
        if self.model is not None:
            self.model.cpu()
            del self.model
            del self.tokenizer
            torch.cuda.empty_cache()
            gc.collect()
            self.model = None
            self.tokenizer = None
    
    def translate(self, text: str, target_lang: str) -> str:
        """
        Translate the input text to the target language.
        
        Args:
            text: Input text to translate
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        self.load_model()
        text, placeholders = extract_placeholders(text)
        text = prepare_text(text, target_lang)
        input_ids = self.tokenizer(text, return_tensors="pt").input_ids.to(self.model.device)
        outputs = self.model.generate(
            input_ids=input_ids,
            max_length=800, # depends on the use case, model is stable on relatively long inputs
        )
        translation = self.tokenizer.decode(outputs[0])
        translation = translation.replace('<pad>', '').replace('<s>', '').replace('</s>', '').replace('<unk> ', '')
        translation = restore_placeholders(translation, placeholders)
        return translation



# Create a singleton instance
translator_service = TranslatorService()