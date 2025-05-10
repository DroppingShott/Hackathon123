import { ethers } from "ethers";
import * as sapphire from "@oasisprotocol/sapphire-paratime";
import dotenv from "dotenv";
dotenv.config();

const CONTRACT_ADDRESS = " 0xcE0A7768828B1fB0b347891E45b52e4577F3db7A";
const ABI = [
  "event WalletSubmitted(bytes encryptedWallet)"
];

const provider = sapphire.wrap(new ethers.JsonRpcProvider(process.env.SAPPHIRE_RPC));
const contract = new ethers.Contract(CONTRACT_ADDRESS, ABI, provider);

(async () => {
  const events = await contract.queryFilter("WalletSubmitted");
  const latest = events[events.length - 1];
  const decrypted = sapphire.utils.decrypt(latest.args.encryptedWallet);
  console.log("🔓 Decrypted wallet:", decrypted);
})();
