pragma solidity ^0.8.0;

contract VulnerableContract {
    address private owner;

    constructor() {
        owner = msg.sender;
    }

    function destroyContract(address payable recipient) public {
        require(msg.sender == owner, "Only the contract owner can destroy the contract");
        selfdestruct(recipient);
    }
}