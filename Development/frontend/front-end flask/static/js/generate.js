if (typeof web3 !== 'undefined') {
    web3 = new Web3(web3.currentProvider);
} else {
    web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
}

loadPubKey();


/**
 *  Requests user to log in to metamask and approve connection with webapp
 */
function loadPubKey(){
    if (typeof window.ethereum === 'undefined') {
        alert('Looks like you need a Dapp browser to get started.')
        alert('Consider installing MetaMask!')
    } else {
        ethereum.enable()
        // User reject request
        .catch(function (reason) {
        if (reason === 'User rejected provider access') {
        } else {
            console.log(reason)
            alert('There was an issue signing you in.')
        }
        })
        .then(function (accounts) {

            // Uncomment following block in the future to verify network user is on
            // Copy block into other .js files located in ./static/js if required
            // Might have API in the future. Check resolution of metamask github
            // https://github.com/MetaMask/metamask-extension/issues/3663

            /*
            var desiredNetwork = 1
            // 1:Main Network ; 3:Ropsten ; 4:Rinkleby ; 42:Kovan
            if (ethereum.networkVersion !== desiredNetwork) {
               alert('This application requires the main network, please switch it in your MetaMask UI.')
            }
            */
            
            const account = accounts[0]
            document.getElementById("pubKey").value=account;
            loadBirthdayHash()
        })
    } 
}

/**
 *  Loads birthday hash of the account currently associated with Metamask wallet
 * 
 *  TODO: Automate deployment of government contract
 */
function loadBirthdayHash(){
    // Government contract is currently manually deployed through remix
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
        if (error) console.error(error)
        document.getElementById("birthdayHash").value=result;
        })
}