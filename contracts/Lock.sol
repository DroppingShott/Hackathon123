// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract AlertStorage {
    mapping(address => mapping(string => string)) public alerts;

    event AlertRaised(address indexed user, string token, string message);

    function storeAlert(address user, string calldata token, string calldata message) public {
        alerts[user][token] = message;
        emit AlertRaised(user, token, message);
    }

    function getAlert(address user, string calldata token) public view returns (string memory) {
        return alerts[user][token];
    }
}
