"""Gradio interface for the translator application."""
import gradio as gr
from app.config import settings
from app.services.translator import translator_service

def create_gradio_interface():
    """Create and configure the Gradio interface."""
    
    def load_model() -> str:
        """Load the translation model."""
        try:
            translator_service.load_model()
            return "Model loaded successfully"
        except Exception as e:
            return f"Error loading model: {str(e)}"
    
    def unload_model() -> str:
        """Unload the translation model."""
        try:
            translator_service.unload_model()
            return "Model unloaded successfully"
        except Exception as e:
            return f"Error unloading model: {str(e)}"
    
    def get_model_status() -> str:
        """Get the current model status."""
        return "Model is loaded" if translator_service.model is not None else "Model is not loaded"
    
    def translate_text(text: str, target_lang: str) -> str:
        """Wrapper function for translation service."""
        if not text.strip():
            return "Please enter some text to translate."
        
        try:
            result = translator_service.translate(text, target_lang)
            return result, get_model_status()
        except Exception as e:
            return f"Translation error: {str(e)}"
    
    # Create the interface
    with gr.Blocks(title="Neural Machine Translator") as interface:
        gr.Markdown("# Neural Machine Translator")
        gr.Markdown("Translate text between multiple languages using neural machine translation.")
        
        # Model control section
        with gr.Row():
            load_btn = gr.Button("Load Model", variant="primary")
            unload_btn = gr.Button("Unload Model", variant="secondary")
            status_text = gr.Textbox(
                label="Model Status",
                value=get_model_status(),
                interactive=False
            )
        
        # Translation section
        with gr.Row():
            input_text = gr.Textbox(
                lines=5,
                placeholder="Enter text to translate...",
                label="Input Text"
            )
            target_lang = gr.Dropdown(
                choices=list(settings.SUPPORTED_LANGUAGES.keys()),
                label="Target Language",
                value="de",
                type="value"
            )
        
        output_text = gr.Textbox(
            label="Translated Text",
            lines=5
        )
        
        # Connect components
        load_btn.click(
            fn=load_model,
            outputs=status_text
        )
        
        unload_btn.click(
            fn=unload_model,
            outputs=status_text
        )
        
        # Set up translation triggers
        input_text.submit(
            fn=translate_text,
            inputs=[input_text, target_lang],
            outputs=[output_text, status_text]
        )
        
        
        # Add a translate button
        translate_btn = gr.Button("Translate", variant="primary")
        translate_btn.click(
            fn=translate_text,
            inputs=[input_text, target_lang],
            outputs=[output_text, status_text]
        )
    
    return interface