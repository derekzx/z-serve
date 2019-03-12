pragma solidity >=0.4.22 <0.6.0;

contract govSC {
    mapping(address => bytes32) public birthdayHashes;
    address owner;

    constructor() public{
        birthdayHashes[0x2A00CDf2032007133f21e794dd832DB2692D9426] = 0x19E154992DDED7F825098D336696AC7DE950CC59FAF7EE42E907D5EA6A38C29A;
        owner = msg.sender;
        
    }
    
    function setHash(address checkedPerson, bytes32 birthdayHash) public {
        if (msg.sender == owner)
            birthdayHashes[checkedPerson] = birthdayHash;
    }

    function getHash(address checkedPerson) public view returns (bytes32) {
        return birthdayHashes[checkedPerson];
    }
}