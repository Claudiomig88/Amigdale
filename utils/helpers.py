import requests
import time
import os
from typing import List

def download_file(url: str, output_path: str) -> str:
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    return output_path

def wait_for_leonardo_generation(generation_id: str, api_key: str, timeout: int = 300) -> List[str]:
    headers = {
        'authorization': f'Bearer {api_key}',
        'content-type': 'application/json'
    }
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        response = requests.get(
            f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}",
            headers=headers
        )
        
        data = response.json()
        
        if data.get('generations_by_pk', {}).get('status') == 'COMPLETE':
            images = data['generations_by_pk']['generated_images']
            return [img['url'] for img in images]
        
        time.sleep(5)
    
    raise TimeoutError(f"Leonardo generation {generation_id} timed out")

def analyze_script_for_scenes(script: str, num_scenes: int = 25) -> List[str]:
    sentences = script.replace('\n', ' ').split('. ')
    
    scenes_per_sentence = max(1, num_scenes // len(sentences))
    
    base_prompts = []
    
    for sentence in sentences[:num_scenes]:
        if len(sentence.strip()) > 20:
            prompt = f"Historical scene: {sentence.strip()[:200]}, cinematic lighting, detailed, professional photography"
            base_prompts.append(prompt)
    
    while len(base_prompts) < num_scenes:
        base_prompts.append("Historical scene, cinematic atmosphere, detailed, professional photography")
    
    return base_prompts[:num_scenes]

def clean_filename(filename: str) -> str:
    import re
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'[-\s]+', '_', filename)
    return filename[:100]
