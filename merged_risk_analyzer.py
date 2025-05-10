# Merged CryptoPanic Risk Analyzer
# ================================

# === From cryptopanic_fetcher.ipynb ===

#!/usr/bin/env python
# coding: utf-8

# In[21]:


import json
import requests
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any
from dotenv import load_dotenv
import os

API_PATH = "/Users/akramchakrouni/eth-wallet-risk-analysis/sentiment_analysis/config/api_keys.env"
KEY_NAME = "CRYPTO_PANIC_API_KEY"

BASE_URL = "https://cryptopanic.com/api/v1/posts/"

MAX_PER_ASSET = 5
DAYS_BACK = 7

def load_symbols_from_token_list(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    tokens = data.get("tokens", [])
    symbols = list({token["symbol"] for token in tokens if "symbol" in token})
    return symbols

def load_api_key(api_path: str, key_name: str) -> str:
    """Load API key from environment file"""
    load_dotenv(api_path)
    api_key = os.getenv(key_name)
    if not api_key:
        raise ValueError(f"Missing {key_name} in environment")
    return api_key

def save_json(data: object, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_recent_articles(symbol: str, filter_type: str) -> List[Dict[str, Any]]:

    api_key = load_api_key(API_PATH, KEY_NAME)

    params = {
        "auth_token": CRYPTO_PANIC_API_KEY,
        "currencies": symbol,
        "filter": filter_type
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        print(f"[{symbol}] Error {response.status_code} with filter={filter_type}")
        return []

    cutoff = datetime.utcnow() - timedelta(days=DAYS_BACK)
    results = []
    for post in response.json().get("results", []):
        try:
            pub_time = datetime.strptime(post["published_at"], "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)
        except Exception:
            continue
        if pub_time >= cutoff:
            results.append({
                "text": post["title"],
                "source": post["url"],
                "published_at": pub_time.isoformat()
            })
        if len(results) >= MAX_PER_ASSET:
            break
    return results

def fetch_news_for_symbols(symbols: List[str]) -> List[Dict[str, Any]]:
    output_data = []
    cutoff = (datetime.utcnow() - timedelta(days=DAYS_BACK)).isoformat()

    for symbol in symbols:
        articles = get_recent_articles(symbol, filter_type="hot")
        if not articles:
            print(f"[{symbol}] Fallback to filter=new")
            articles = get_recent_articles(symbol, filter_type="new")

        if articles:
            output_data.append({
                "asset_name": symbol,
                "status": "analyzed",
                "texts": articles
            })
        else:
            output_data.append({
                "asset_name": symbol,
                "status": "no_recent_data",
                "texts": [],
                "risk_level": None,
                "reason": f"No qualifying articles found after {cutoff}",
                "priority": None
            })

        time.sleep(1)

    return output_data


# In[22]:


ASSET_FILE_PATH = "/Users/akramchakrouni/eth-wallet-risk-analysis/sentiment_analysis/input/assets_input.json"
OUTPUT_PATH = "/Users/akramchakrouni/eth-wallet-risk-analysis/sentiment_analysis/output/cp_output.json"

if __name__ == "__main__":
    symbols = load_symbols_from_token_list(ASSET_FILE_PATH)
    print(f"🔍 Detected symbols: {symbols}")
    asset_data = fetch_news_for_symbols(symbols)
    save_json(asset_data, OUTPUT_PATH)
    print(f"✅ Output saved to {OUTPUT_PATH}")



# === From inference.ipynb ===

#!/usr/bin/env python
# coding: utf-8

# In[52]:


import os
import json
from openai import OpenAI
from dotenv import load_dotenv

API_PATH=r"/Users/akramchakrouni/eth-wallet-risk-analysis/sentiment_analysis/config/api_keys.env"
KEY_NAME="NVIDIA_API_KEY"

SYSTEM_PROMPT_PATH=r"/Users/akramchakrouni/eth-wallet-risk-analysis/sentiment_analysis/config/system_prompt.txt"

MODEL_BASE_URL="https://integrate.api.nvidia.com/v1"
MODEL_TYPE="nvidia/llama-3.3-nemotron-super-49b-v1"

def load_api_key(api_path: str, key_name: str) -> str:
    """Load API key from environment file"""
    load_dotenv(api_path)
    api_key = os.getenv(key_name)
    if not api_key:
        raise ValueError(f"Missing {key_name} in environment")
    return api_key

def load_system_prompt(system_prompt_path: str) -> str:
    """Load system prompt from file"""
    with open(system_prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def load_crypto_panic_input_data(file_path: str) -> Dict[str, Any]:
    """Load and parse assets input data from file"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def run_sentiment_inference(asset_json_path: str) -> dict:
    """
    Run sentiment risk analysis on a given JSON file of asset data using NVIDIA's LLM API.

    Args:
        asset_json_path (str): Path to the JSON file with asset names and associated text data.

    Returns:
        dict: Parsed JSON result from the LLM containing risk assessments.
    """

    # Load API key
    api_key = load_api_key(API_PATH, KEY_NAME)
    
    # Load system prompt
    system_prompt = load_system_prompt(SYSTEM_PROMPT_PATH)

    # Load asset data
    user_input = user_input = json.dumps(load_crypto_panic_input_data(asset_json_path))

    # Initialize OpenAI client
    client = OpenAI(
        base_url=MODEL_BASE_URL,
        api_key=api_key
    )

    # Create chat completion
    completion = client.chat.completions.create(
        model=MODEL_TYPE,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.6,
        top_p=0.95,
        max_tokens=4096,
        frequency_penalty=0,
        presence_penalty=0,
        stream=True
    )

    # Stream and capture response
    output = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content
        if content is not None:
            print(content, end="")
            output += content

    # Parse and return JSON
    try:
        result_json = json.loads(output)
        return result_json
    except json.JSONDecodeError as e:
        raise RuntimeError("Failed to parse LLM output as JSON.") from e


# In[53]:


if __name__ == "__main__":
    result = run_sentiment_inference("/Users/akramchakrouni/eth-wallet-risk-analysis/sentiment_analysis/output/cp_output.json")
    with open("/Users/akramchakrouni/eth-wallet-risk-analysis/sentiment_analysis/output/sen_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

