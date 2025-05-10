from web3 import Web3

# Connect to Ethereum Mainnet RPC
ETH_RPC = "https://cloudflare-eth.com"  # Free public Ethereum RPC
RAW_ADDRESS = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"  # Replace this

# Init Web3
web3 = Web3(Web3.HTTPProvider(ETH_RPC))
ADDRESS = web3.to_checksum_address(RAW_ADDRESS)

if not web3.is_connected():
    print("❌ Could not connect to Ethereum Mainnet.")
else:
    balance_wei = web3.eth.get_balance(ADDRESS)
    balance_eth = web3.from_wei(balance_wei, "ether")
    print(f"✅ ETH balance for {ADDRESS}: {balance_eth} ETH")
