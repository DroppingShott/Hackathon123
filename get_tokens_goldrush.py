import requests

ADDRESS = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
CHAIN_ID = "1"  # Ethereum mainnet
API_KEY = "cqt_rQCcgrJbk6Cqkd9CDcXrDQRQGcyq"

def fetch_tokens(address):
    url = f"https://api.covalenthq.com/v1/{CHAIN_ID}/address/{address}/balances_v2/?key={API_KEY}"
    response = requests.get(url)

    try:
        data = response.json()
    except Exception as e:
        print("❌ Could not parse JSON.")
        print(response.status_code, response.text)
        return []

    if "data" not in data or "items" not in data["data"]:
        print("❌ Unexpected data structure.")
        return []

    tokens = []
    for item in data["data"]["items"]:
        decimals = item.get("contract_decimals")
        if decimals is None or decimals == 0:
            continue  # skip tokens with missing or invalid decimals

        try:
            balance = float(item["balance"]) / (10 ** decimals)
        except (ValueError, ZeroDivisionError):
            continue

        if balance > 0:
            tokens.append({
                "symbol": item.get("contract_ticker_symbol", "UNKNOWN"),
                "balance": round(balance, 4)
            })

    return tokens

# Run
tokens = fetch_tokens(ADDRESS)
print(f"\n✅ Tokens held by {ADDRESS}:\n")
if not tokens:
    print("No tokens with balance > 0.")
else:
    for t in tokens:
        print(f"• {t['symbol']}: {t['balance']}")
