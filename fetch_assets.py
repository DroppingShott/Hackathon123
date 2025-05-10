import sys
import requests
import json

CHAIN_ID = "1"
API_KEY = "cqt_rQCcgrJbk6Cqkd9CDcXrDQRQGcyq"

def fetch_tokens(address):
    url = f"https://api.covalenthq.com/v1/{CHAIN_ID}/address/{address}/balances_v2/?key={API_KEY}"
    response = requests.get(url)

    try:
        data = response.json()
    except Exception as e:
        return {"error": "Failed to parse JSON", "details": str(e)}

    if "data" not in data or "items" not in data["data"]:
        return {"error": "Unexpected data format"}

    tokens = []
    for item in data["data"]["items"]:
        try:
            quote = item.get("quote", 0.0)
            if quote and quote > 5:
                tokens.append({
                    "symbol": item.get("contract_ticker_symbol", "UNKNOWN"),
                    "address": item.get("contract_address", "N/A"),
                    "usd_value": round(quote, 2)
                })
        except Exception:
            continue

    return {"address": address, "tokens": tokens}

if __name__ == "__main__":
    address = sys.argv[1]
    result = fetch_tokens(address)
    
    # Write result to data.json
    with open("data.json", "w") as f:
        json.dump(result, f, indent=2)

    # Also print to console
    print(json.dumps(result, indent=2))
