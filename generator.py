import requests
import tiktoken
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://router.huggingface.co/v1/chat/completions"
HF_TOKEN = os.getenv("HF_API_KEY")
MODEL = "Qwen/Qwen3-235B-A22B-Instruct-2507:fireworks-ai"
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
}

SYSTEM_PROMPT_BASE = "Kamu adalah AI yang menjawab pertanyaan berdasarkan chat WhatsApp berikut. Jawab sebagai {lawan}, dengan gaya {lawan}, berdasarkan histori chat."

# Helper to count tokens
encoding = tiktoken.get_encoding('cl100k_base')
def count_tokens(text):
    return len(encoding.encode(text))

def build_prompt(contexts, question, peran, lawan, max_tokens=2000):
    system_prompt = SYSTEM_PROMPT_BASE.format(lawan=lawan)
    context_str = "\n".join([
        f"[{c['timestamp']}] {c['sender']}: {c['message']}" for c in contexts
    ])
    prompt = f"{system_prompt}\n\nChat Histori:\n{context_str}\n\nPertanyaan dari {peran}: {question}\nJawaban sebagai {lawan}:"
    # Truncate if too long
    while count_tokens(prompt) > max_tokens and contexts:
        contexts = contexts[1:]
        context_str = "\n".join([
            f"[{c['timestamp']}] {c['sender']}: {c['message']}" for c in contexts
        ])
        prompt = f"{system_prompt}\n\nChat Histori:\n{context_str}\n\nPertanyaan dari {peran}: {question}\nJawaban sebagai {lawan}:"
    return prompt

def ask_huggingface(prompt, system_prompt=None, model=MODEL):
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt if system_prompt else ""},
            {"role": "user", "content": prompt}
        ],
        "model": model
    }
    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"].strip()
