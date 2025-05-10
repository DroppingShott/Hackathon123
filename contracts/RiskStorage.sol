// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.28;

contract RiskStorage {
    address public owner;
    string public encryptedWallet;

    constructor() {
        owner = msg.sender;
    }

    function storeEncryptedWallet(string memory _encryptedWallet) public {
        encryptedWallet = _encryptedWallet;
    }

    function getEncryptedWallet() public view returns (string memory) {
        return encryptedWallet;
    }
}
