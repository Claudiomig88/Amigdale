import requests
import time
import os
from typing import Optional
from src.pipeline.state import VideoProductionState
from src.config import Config
from src.utils.helpers import wait_for_leonardo_generation, download_file, analyze_script_for_scenes, clean_filename

def images_agent(state: VideoProductionState) -> dict:
    script = state.get('script', '')
    topic = state.get('topic') or 'untitled'
    
    scene_prompts = analyze_script_for_scenes(script, Config.NUM_IMAGES_PER_VIDEO)
    
    headers = {
        'authorization': f'Bearer {Config.LEONARDO_API_KEY}',
        'content-type': 'application/json'
    }
    
    image_paths = []
    topic_clean = clean_filename(topic)
    
    style_reference_id = upload_style_reference_if_exists(headers)
    
    for i, scene_prompt in enumerate(scene_prompts):
        payload = {
            "height": 576,
            "width": 1024,
            "modelId": Config.LEONARDO_MODEL_ID,
            "prompt": f"{scene_prompt}, cinematic, historical, professional",
            "photoReal": True,
            "alchemy": True,
            "num_images": 1,
            "public": False
        }
        
        if style_reference_id:
            payload["controlnets"] = [{
                "initImageId": style_reference_id,
                "preprocessorId": 67,
                "strengthType": "High"
            }]
        
        try:
            response = requests.post(
                "https://cloud.leonardo.ai/api/rest/v1/generations",
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                print(f"Leonardo API error: {response.text}")
                continue
            
            gen_id = response.json()['sdGenerationJob']['generationId']
            
            api_key = Config.LEONARDO_API_KEY or ""
            image_urls = wait_for_leonardo_generation(gen_id, api_key)
            
            if image_urls:
                local_path = os.path.join(Config.IMAGES_DIR, f"{topic_clean}_{i}.jpg")
                download_file(image_urls[0], local_path)
                image_paths.append(local_path)
            
            time.sleep(2)
            
        except Exception as e:
            print(f"Error generating image {i}: {e}")
            continue
    
    if len(image_paths) < 10:
        raise ValueError(f"Failed to generate enough images. Only got {len(image_paths)}/25")
    
    return {"images": image_paths}

def upload_style_reference_if_exists(headers: dict) -> Optional[str]:
    style_image_path = None

    default_path = os.path.join(Config.ASSETS_DIR, "style_reference.jpg")
    if os.path.exists(default_path):
        style_image_path = default_path
    else:
        for ext in ['.jpg', '.jpeg', '.png']:
            path = f"data/style_reference_image{ext}"
            if os.path.exists(path):
                style_image_path = path
                break

    if not style_image_path:
        return None
    
    with open(style_image_path, 'rb') as f:
        files = {'file': f}
        upload_response = requests.post(
            "https://cloud.leonardo.ai/api/rest/v1/init-image",
            headers={'authorization': headers['authorization']},
            files=files
        )
    
    if upload_response.status_code == 200:
        return upload_response.json().get('uploadInitImage', {}).get('id')
    
    return None
