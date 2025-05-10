// contracts/RiskSubmit.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract RiskSubmit {
    event WalletSubmitted(address indexed sender, string walletAddress);

    function submitWallet(string calldata walletAddress) public {
        emit WalletSubmitted(msg.sender, walletAddress);
    }
}
