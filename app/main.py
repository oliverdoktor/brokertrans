"""Main FastAPI application."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import gradio as gr
from app.models import TranslationRequest, TranslationResponse
from app.services.translator import translator_service
from app.ui.gradio_interface import create_gradio_interface
from app.config import settings

app = FastAPI(
    title="Neural Machine Translator",
    description="API for neural machine translation",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/translate/", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """
    Translate text to the specified target language.
    """
    
    try:
        translated_text = translator_service.translate(
            request.text,
            request.target_language
        )
        
        return TranslationResponse(
            translated_text=translated_text,
            target_language=settings.SUPPORTED_LANGUAGES[request.target_language]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete("/unload_model/")
async def unload_model():
    """
    Unload the translation model from memory.
    """
    translator_service.unload_model()
    return {"message": "Model unloaded successfully."}

@app.post("/load_model/")
async def load_model():
    """
    Load the translation model into memory.
    """
    translator_service.load_model()
    return {"message": "Model loaded successfully."}

# Create and mount Gradio interface
gradio_interface = create_gradio_interface()
app = gr.mount_gradio_app(app, gradio_interface, path="")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)