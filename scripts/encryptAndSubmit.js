import { ethers } from "ethers";
import * as sapphire from "@oasisprotocol/sapphire-paratime";
import dotenv from "dotenv";
dotenv.config();

const CONTRACT_ADDRESS = " 0xcE0A7768828B1fB0b347891E45b52e4577F3db7A";
const ABI = [
  "function submitWallet(bytes encryptedWallet) external",
  "event WalletSubmitted(bytes encryptedWallet)"
];

const provider = sapphire.wrap(new ethers.JsonRpcProvider(process.env.SAPPHIRE_RPC));
const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);
const contract = new ethers.Contract(CONTRACT_ADDRESS, ABI, wallet);

const walletToEncrypt = process.argv[2];
if (!walletToEncrypt) throw new Error("Provide wallet address to encrypt.");

(async () => {
  const encrypted = sapphire.utils.encrypt(walletToEncrypt);
  const tx = await contract.submitWallet(encrypted);
  await tx.wait();
  console.log("🔐 Encrypted & submitted!");
})();
