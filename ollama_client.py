import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"


import requests
import base64

OLLAMA_URL = "http://localhost:11434"


def chat_llm(messages, model="llama3.1:8b", tools=None, stream=False):
    payload = {"model": model, "messages": messages, "stream": stream}
    if tools:
        payload["tools"] = tools
    try:
        r = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=120)
        print("Status:", r.status_code)
        print("Response:", r.text[:500])
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Ollama request failed: {e}\nPayload: {payload}")


def vision_qa(image_bytes, prompt="What is this?", model="llava"):
    import base64, requests
    b64 = base64.b64encode(image_bytes).decode()

    msgs = [{
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image", "image": b64}
        ]
    }]

    payload = {"model": model, "messages": msgs}

    try:
        r = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=120)
        print("Status:", r.status_code)
        print("Response:", r.text[:500])  # show first 500 chars
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Ollama vision request failed: {e}\nPayload: {payload}")
