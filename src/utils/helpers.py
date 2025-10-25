import os
import re
import time
from itertools import cycle
from typing import List, Optional

import requests


def download_file(url: str, output_path: str) -> str:
    """Download ``url`` to ``output_path`` ensuring the destination directory exists."""

    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(output_path, "wb") as file_obj:
        for chunk in response.iter_content(chunk_size=8192):
            if not chunk:
                continue
            file_obj.write(chunk)

    return output_path


def wait_for_leonardo_generation(
    generation_id: str,
    api_key: str,
    timeout: int = 300,
) -> List[str]:
    """Poll Leonardo.ai for a generation result until completion or timeout."""

    if timeout <= 0:
        raise TimeoutError(f"Leonardo generation {generation_id} timed out")

    headers = {
        "authorization": f"Bearer {api_key}",
        "content-type": "application/json",
    }

    start_time = time.time()
    poll_interval = min(5.0, max(0.5, timeout / 10.0))
    last_error: Optional[Exception] = None

    while time.time() - start_time < timeout:
        try:
            response = requests.get(
                f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}",
                headers=headers,
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError) as exc:
            last_error = exc
            time.sleep(poll_interval)
            continue

        generation = data.get("generations_by_pk") or {}
        status = generation.get("status")

        if status == "COMPLETE":
            images = generation.get("generated_images") or []
            urls = [img.get("url") for img in images if isinstance(img, dict) and img.get("url")]
            if urls:
                return urls
            raise ValueError("Leonardo API response missing generated image URLs")

        if status in {"FAILED", "ERROR"}:
            raise RuntimeError(
                f"Leonardo generation {generation_id} failed with status {status}"
            )

        time.sleep(poll_interval)

    if last_error:
        raise TimeoutError(
            f"Leonardo generation {generation_id} timed out after repeated errors"
        ) from last_error

    raise TimeoutError(f"Leonardo generation {generation_id} timed out")


def analyze_script_for_scenes(script: str, num_scenes: int = 25) -> List[str]:
    """Return descriptive prompts derived from ``script`` for image generation."""

    if num_scenes <= 0:
        return []

    normalized = re.sub(r"\s+", " ", script).strip()
    prompts: List[str] = []

    if normalized:
        sentences = [
            sentence.strip()
            for sentence in re.split(r"(?<=[.!?])\s+", normalized)
            if sentence.strip()
        ]

        snippets: List[str] = []
        for sentence in sentences:
            words = sentence.split()
            if not words:
                continue

            current: List[str] = []
            for word in words:
                potential_length = len(" ".join(current + [word])) if current else len(word)
                if potential_length > 200 and current:
                    snippets.append(" ".join(current))
                    current = [word]
                else:
                    current.append(word)

            if current:
                snippets.append(" ".join(current))

        # Use snippets derived from the script where possible
        for snippet in snippets:
            prompts.append(
                f"Historical scene: {snippet[:200]}, cinematic lighting, detailed, professional photography"
            )
            if len(prompts) >= num_scenes:
                break

        if snippets and len(prompts) < num_scenes:
            for snippet in cycle(snippets):
                prompts.append(
                    f"Historical scene: {snippet[:200]}, cinematic lighting, detailed, professional photography"
                )
                if len(prompts) >= num_scenes:
                    break

    while len(prompts) < num_scenes:
        prompts.append(
            "Historical scene, cinematic atmosphere, detailed, professional photography"
        )

    return prompts[:num_scenes]


def clean_filename(filename: str) -> str:
    filename = re.sub(r"[^\w\s-]", "", filename)
    filename = re.sub(r"[-\s]+", "_", filename).strip("_")
    return filename[:100]
