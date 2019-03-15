if (typeof web3 !== 'undefined') {
    web3 = new Web3(web3.currentProvider);
} else {
    web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
}

loadProofJson();

/**
 * Creates a HTTP request which hits local Flask server to retrieve ./contracts/proof.json
 * Calls verifyProof() using retrieved proof
 */
function loadProofJson(){
    var api = 'http://localhost:8000/proofJson';
    const xhr = new XMLHttpRequest();

    xhr.responseType = 'json';
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            proof = this.response
            verifyProof(proof)
        }
        return this.response
    }
    xhr.open('GET', api, true);
    xhr.send();
}


/**
 * Verfies proof by sending proof.json to the verifier contract and listening for the fired "Verified" event
 *  
 * @param {JSON} proof 
 * 
 */
function verifyProof(proof){

    // ABI for verifier contract
    var ABI = [{
            "constant": false,
            "inputs": [
                {
                    "name": "a",
                    "type": "uint256[2]"
                },
                {
                    "name": "a_p",
                    "type": "uint256[2]"
                },
                {
                    "name": "b",
                    "type": "uint256[2][2]"
                },
                {
                    "name": "b_p",
                    "type": "uint256[2]"
                },
                {
                    "name": "c",
                    "type": "uint256[2]"
                },
                {
                    "name": "c_p",
                    "type": "uint256[2]"
                },
                {
                    "name": "h",
                    "type": "uint256[2]"
                },
                {
                    "name": "k",
                    "type": "uint256[2]"
                },
                {
                    "name": "input",
                    "type": "uint256[6]"
                }
            ],
            "name": "verifyTx",
            "outputs": [
                {
                    "name": "r",
                    "type": "bool"
                }
            ],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "anonymous": false,
            "inputs": [
                {
                    "indexed": false,
                    "name": "s",
                    "type": "string"
                }
            ],
            "name": "Verified",
            "type": "event"
        }]
    
    web3.eth.defaultAccount = web3.eth.accounts[0]
    var verifierContract= web3.eth.contract(ABI)

    // Minor formatting to remove whitespaces
    unFormattedContractAddress = document.getElementById("contractAddress").innerHTML
    CAStartIndex = unFormattedContractAddress.indexOf('0')
    contractAddress = unFormattedContractAddress.substring(CAStartIndex, CAStartIndex+42)

    var verifier = verifierContract.at(contractAddress)
    
    // Event listener for verifier contract. All events that are fired by the verifier contract are constantly monitored
    var instructorEvent = verifier.Verified({}, {fromBlock: 0, toBlock: 'latest'});

    instructorEvent.watch(function(error,result){
        if (error) console.error(error)
        else {
            blockNumber = result["blockNumber"]
            txHash = result["transactionHash"]
            web3.eth.getBlockNumber(function (error, result) {
                if (error) console.error(error)
                // This condition ensures that our webapp will only recognize the latest 'Verified' event
                if (result==blockNumber && txHash==document.getElementById("verificationTxHash").innerHTML){
                    document.getElementById("verificationStatus").innerHTML = "Verified"
                }
            })
        }
    })
    
    A = proof["proof"]["A"]
    A_p = proof["proof"]["A_p"]
    B = proof["proof"]["B"]
    B_p = proof["proof"]["B_p"]
    C = proof["proof"]["C"]
    C_p = proof["proof"]["C_p"]
    H = proof["proof"]["H"]
    K = proof["proof"]["K"]
    witness = proof["input"]

    // Converts witness to a BigNumber (256bits) since JS only allows max of 53 bits
    for (var i =0 ; i<witness.length; i++){
        witness[i] = BigNumber(witness[i])
    }

    verifier.verifyTx(A, A_p, B, B_p, C, C_p, H, K, witness, function(error, result){
        if (error) console.error(error)
        web3.eth.getTransactionReceipt(result, function(error, result){
            if (error) console.error(error)
            document.getElementById("verificationTxHash").innerHTML = result["transactionHash"]
            console.log(result)           
        })
    })
}