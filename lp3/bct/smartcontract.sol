// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Contract = a program that lives on the blockchain and holds data + functions.
contract Banking {

    // ---------------- STATE VARIABLES ----------------
    // A mapping works like a dictionary / hash map: key => value.
    // address = a wallet/account address on Ethereum.

    // Stores the balance of every user (in wei; 1 Ether = 10^18 wei).
    // "public" auto-creates a getter so you can check any address's balance.
    mapping(address => uint) public user_account;

    // Stores whether a user has created an account (true / false).
    mapping(address => bool) public user_exists;

    // ---------------- CREATE ACCOUNT ----------------
    // "payable" means this function can receive Ether along with the call.
    // The Ether sent (msg.value) becomes the opening balance (can be 0).
    function create_account() public payable returns (string memory) {

        // require(condition, message): if the condition is false, the whole
        // transaction is cancelled and the message is shown as the error.
        require(user_exists[msg.sender] == false, "Account already created");

        // msg.sender = address of the person calling the function.
        // msg.value  = amount of Ether (in wei) sent with the call.
        user_account[msg.sender] = msg.value;
        user_exists[msg.sender] = true;

        return "Account created";
    }

    // ---------------- DEPOSIT MONEY ----------------
    // The user sends Ether along with this call and it is added to their balance.
    function deposit() public payable returns (string memory) {

        require(user_exists[msg.sender] == true, "Account not created");
        require(msg.value > 0, "Value for deposit is Zero");

        // Add the deposited amount to the existing balance.
        user_account[msg.sender] = user_account[msg.sender] + msg.value;

        return "Deposited Successfully";
    }

    // ---------------- WITHDRAW MONEY ----------------
    // "amount" is given in wei. The Ether is sent from the contract
    // back to the user's wallet.
    function withdraw(uint amount) public returns (string memory) {

        require(user_exists[msg.sender] == true, "Account not created");
        require(amount > 0, "Amount should be more than zero");
        // >= so the user can withdraw their entire balance.
        require(user_account[msg.sender] >= amount, "Insufficient Balance");

        // IMPORTANT: reduce the balance FIRST, then send the Ether.
        // This is a safety practice that prevents re-entrancy attacks.
        user_account[msg.sender] = user_account[msg.sender] - amount;

        // call{value: amount}("") sends Ether to the user's wallet.
        // It returns true/false in "success". This is the recommended
        // replacement for the deprecated transfer().
        (bool success, ) = payable(msg.sender).call{value: amount}("");
        require(success, "Withdrawal failed");

        return "Withdrawal Successful";
    }

    // ---------------- SHOW BALANCE ----------------
    // "view" = only reads data, changes nothing, so it costs no gas
    // when called directly from Remix.
    function user_balance() public view returns (uint) {
        return user_account[msg.sender];
    }

    // ---------------- CHECK IF ACCOUNT EXISTS ----------------
    function account_exist() public view returns (bool) {
        return user_exists[msg.sender];
    }

    // ---------------- TRANSFER TO ANOTHER BANK USER ----------------
    // Moves money from one customer's balance to another customer's
    // balance inside the bank. No Ether leaves the contract.
    function transfer(address userAddress, uint amount) public returns (string memory) {

        require(user_exists[msg.sender] == true, "Account is not created");
        require(user_exists[userAddress] == true, "Transfer account does not exist");
        require(amount > 0, "Amount should be more than zero");
        require(user_account[msg.sender] >= amount, "Insufficient balance in Bank account");

        user_account[msg.sender] = user_account[msg.sender] - amount;
        user_account[userAddress] = user_account[userAddress] + amount;

        return "Transfer Successful";
    }

    // ---------------- SEND TO ANY WALLET ----------------
    // Sends Ether from the user's bank balance to any outside wallet address.
    function send_amt(address payable toAddress, uint256 amount) public returns (string memory) {

        require(user_exists[msg.sender] == true, "Account is not created");
        require(amount > 0, "Amount should be more than zero");
        require(user_account[msg.sender] >= amount, "Insufficient balance in Bank account");

        // Reduce balance first, then send (same safety rule as withdraw).
        user_account[msg.sender] = user_account[msg.sender] - amount;

        (bool success, ) = toAddress.call{value: amount}("");
        require(success, "Transfer failed");

        return "Transfer Success";
    }
}