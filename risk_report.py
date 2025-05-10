
import sys
import json
import requests
from cryptopanic_fetcher import fetch_news_for_symbols

CHAIN_ID = "1"
API_KEY = "cqt_rQCcgrJbk6Cqkd9CDcXrDQRQGcyq"

def fetch_tokens(address):
    url = f"https://api.covalenthq.com/v1/{CHAIN_ID}/address/{address}/balances_v2/?key={API_KEY}"
    response = requests.get(url)

    try:
        data = response.json()
    except Exception as e:
        return [], [], {"error": "Failed to parse JSON", "details": str(e)}

    if "data" not in data or "items" not in data["data"]:
        return [], [], {"error": "Unexpected data format"}

    tokens = []
    symbols = []
    for item in data["data"]["items"]:
        try:
            quote = item.get("quote", 0.0)
            symbol = item.get("contract_ticker_symbol", "UNKNOWN")
            if quote and quote > 5:
                symbols.append(symbol)
                tokens.append({
                    "symbol": symbol,
                    "address": item.get("contract_address", "N/A"),
                    "usd_value": round(quote, 2)
                })
        except Exception:
            continue

    return tokens, symbols, None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Wallet address required"}))
        sys.exit(1)

    wallet = sys.argv[1]
    tokens, symbols, error = fetch_tokens(wallet)

    if error:
        print(json.dumps(error))
        sys.exit(1)

    news = fetch_news_for_symbols(symbols)

    result = {
        "address": wallet,
        "tokens": tokens,
        "news": news
    }

    print(json.dumps(result, indent=2))
