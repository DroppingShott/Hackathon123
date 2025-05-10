// generate-keys.js
import crypto from "crypto";

const key = crypto.randomBytes(32).toString("hex"); // 256-bit
const iv = crypto.randomBytes(16).toString("hex"); // 128-bit

console.log("🔑 WALLET_SECRET_KEY =", key);
console.log("🧊 WALLET_IV =", iv);
