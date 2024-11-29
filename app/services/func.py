import torch
import re

import subprocess
def get_device_with_most_memory():
    # Check if CUDA is available
    if not torch.cuda.is_available():
        raise NotImplementedError("CUDA is not available on this system.")
    
    # Get the number of available GPUs
    device_count = torch.cuda.device_count()
    
    # Check memory for each GPU using nvidia-smi
    available_memory = []
    for device_id in range(device_count):
        # Use nvidia-smi to get memory info
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=memory.free', '--format=csv,nounits,noheader'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"Failed to run nvidia-smi: {result.stderr}, please specify GPU in config.py")
        
        # Parse the output
        free_memory = int(result.stdout.split('\n')[device_id])
        available_memory.append((device_id, free_memory))

    # Select GPU with most available memory
    device_id, _ = max(available_memory, key=lambda x: x[1])
    return f"cuda:{device_id}"

def extract_placeholders(text):
    # Find placeholders in the text marked by []
    placeholders = re.findall(r'\[(.*?)\]', text)
    # Replace placeholders with unique tokens
    processed_text = re.sub(r'\[(.*?)\]', lambda x: f'[PLaC3H0LD3R{placeholders.index(x.group(1))}]', text)
    return processed_text, placeholders

def restore_placeholders(text, placeholders):
    for idx, placeholder in enumerate(placeholders):
        text = text.replace(f'[PLaC3H0LD3R{idx}]', f'[{placeholder}]')
    return text

def prepare_text(text, target_language):
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove leading and trailing spaces
    text = text.strip()
    # remove newlines
    text = text.replace('\n', ' ')
    # remove multiple spaces
    text = re.sub(' +', ' ', text)
    text = f"<2{target_language}> {text}"
    return text