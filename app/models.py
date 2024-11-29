"""Pydantic models for request/response validation."""
from pydantic import BaseModel, Field

class TranslationRequest(BaseModel):
    """Translation request model."""
    text: str = Field(..., min_length=1, max_length=5000)
    target_language: str = Field(..., min_length=2, max_length=2)

class TranslationResponse(BaseModel):
    """Translation response model."""
    translated_text: str
    target_language: str