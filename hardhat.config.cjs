require("dotenv").config(); // this must be at the top
require("@nomicfoundation/hardhat-toolbox");
require("@oasisprotocol/sapphire-hardhat");

module.exports = {
  solidity: "0.8.28",
  networks: {
    sapphireTestnet: {
      url: "https://testnet.sapphire.oasis.dev",
      accounts: [process.env.PRIVATE_KEY],
      chainId: 23295,
    },
  },
};
