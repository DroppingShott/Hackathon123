// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract WalletSubmit {
    event WalletSubmitted(bytes encryptedWallet);

    function submitWallet(bytes calldata encryptedWallet) external {
        emit WalletSubmitted(encryptedWallet);
    }
}
