if (typeof web3 !== 'undefined') {
    web3 = new Web3(web3.currentProvider);
} else {
    // set the provider you want from Web3.providers
    web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
}

loadPubKey();

function loadBirthdayHash(){
    govContractAddress = '0x796cbcffbd465da13c8646f956545577b84406fc'
    var ABI = [
        {
            "constant": false,
            "inputs": [
                {
                    "name": "checkedPerson",
                    "type": "address"
                },
                {
                    "name": "birthdayHash",
                    "type": "bytes32"
                }
            ],
            "name": "setHash",
            "outputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "constructor"
        },
        {
            "constant": true,
            "inputs": [
                {
                    "name": "",
                    "type": "address"
                }
            ],
            "name": "birthdayHashes",
            "outputs": [
                {
                    "name": "",
                    "type": "bytes32"
                }
            ],
            "payable": false,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": true,
            "inputs": [
                {
                    "name": "checkedPerson",
                    "type": "address"
                }
            ],
            "name": "getHash",
            "outputs": [
                {
                    "name": "",
                    "type": "bytes32"
                }
            ],
            "payable": false,
            "stateMutability": "view",
            "type": "function"
        }
    ]

    web3.eth.defaultAccount = web3.eth.accounts[0]
    var govContract= web3.eth.contract(ABI)
    var gov = govContract.at(govContractAddress)

    gov.getHash(web3.eth.defaultAccount, function(error, result){
        // console.log(result)
        document.getElementById("birthdayHash").value=result;
        })

}

function loadPubKey(){
    if (typeof window.ethereum === 'undefined') {
        alert('Looks like you need a Dapp browser to get started.')
        alert('Consider installing MetaMask!')
    
    } else {
        ethereum.enable()

        //User reject request
        .catch(function (reason) {
        if (reason === 'User rejected provider access') {
        } else {
            console.log(reason)
            alert('There was an issue signing you in.')
        }
        })
        .then(function (accounts) {
            const account = accounts[0]
            document.getElementById("pubKey").value=account;
            loadBirthdayHash()
        })
    } 
}