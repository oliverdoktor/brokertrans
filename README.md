# Neural Machine Translation Service

A FastAPI-based translation service using the MADLAD-400 3B model for high-quality machine translation.

## Limitations and areas of improvement:
* Currently in POC state
* Housing one model but can be easily expanded to support multiple models
* Inference is done inside backend, more prudent way would be to house the model inference separately and app should comunicate with inference service. - My solution would be Triton.

### Cost and computation time based on language 
Current model is multilingual, the input and output language does not effect computational cost too much. However, it would be much more cost-efficient to utilize smaller, language specific (or language and domain specific) models. In that case computational cost is dependent on a couple of factors:
* Source-target language similarity
    the closer the languages are in terms of grammatic similarity, the lower the cost
* How low/high recourse language is involved
    Low resource language translation can be expensive due to more complex models and lower quality
* Morphoplogical complexity
    More complex langauges need bigger model to produce similar quality (to put it simply)

## System Requirements

### Hardware Requirements
- **GPU**: NVIDIA GPU with at least 20GB VRAM 
- **Storage**: At least 20GB free space for model weights and cache


### Software Requirements
- **CUDA**: CUDA 12.4 or higher
- **Docker**: Docker with NVIDIA Container Toolkit installed

## Installation & Deployment

### 1. Clone the Repository
```bash
git clone <repository-url>
cd trans
```

### 2. Build Docker Image
```bash
docker build -t translator-app -f Dockerfile .
```

### 5. Run the Container, select a folder for HF_HOME which well hold the weights (app will download it at first use)
```bash
docker run --gpus all \
    -v <PATH_TO_YOUR_TORCH_HOME_FOLDER>:/data/torch_home \
    -v <PATH_TO_YOUR_HF_HOME_FOLDER>:/data/hf_home \
    -p 6660:6660 \
    --env-file .env \
    translator-app
```

## Usage
Most input languages are supported, detection is automatic. 
Input the desired text and target language than hit "Translate"
To free up memory from GPU without stopping the service hit the unload button

### API Endpoints

The service exposes the following endpoints:

1. **Translation API**
   - Endpoint: `POST /translate`
   - Request body:
     ```json
     {
       "text": "Hello, how are you?",
       "target_language": "es"
     }
     ```
   - Response:
     ```json
     {
       "translated_text": "Ich gebe dir etwas",
       "target_language": "German"
     }
     ```

2. **Load Model**
   - Endpoint: `POST /load_model`
   - Load the model on GPU

3. **Unload Model**
   - Endpoint: `DELETE /unload_model`
   - Unloads the model from GPU

### Supported Languages
Almost all language is supported, dropdown is limited in the UI for expedience but the API accepts everything.

## Model Information

### MADLAD-400 3B
MADLAD-400 is a powerful machine translation model developed by Google Research. 

**Key Features:**
- 3 billion parameters
- Trained on 400+ languages
- High-quality translations for major language pairs
- Automatic input language detection

**Model Specifications:**
- Model Size: ~11GB on disk
- Runtime Memory: ~21GB VRAM during inference
- Average inference time: 0.5-2 seconds per translation (GPU and text length dependent)
