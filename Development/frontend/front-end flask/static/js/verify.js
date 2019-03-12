if (typeof web3 !== 'undefined') {
    web3 = new Web3(web3.currentProvider);
} else {
    // set the provider you want from Web3.providers
    web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
}

// test_Address = '0x4a7d06a50563a988f49129e6eb96f071c6947e8c'
// var ABI = [
// 	{
// 		"constant": false,
// 		"inputs": [
// 			{
// 				"name": "v",
// 				"type": "uint256"
// 			}
// 		],
// 		"name": "deposit",
// 		"outputs": [],
// 		"payable": false,
// 		"stateMutability": "nonpayable",
// 		"type": "function"
// 	},
// 	{
// 		"anonymous": false,
// 		"inputs": [
// 			{
// 				"indexed": false,
// 				"name": "_value",
// 				"type": "uint256"
// 			}
// 		],
// 		"name": "Deposit",
// 		"type": "event"
// 	}
// ]
// web3.eth.defaultAccount = web3.eth.accounts[0]
// var testContract = web3.eth.contract(ABI)
// var test = testContract.at(test_Address)

// var watcher = test.Deposit({}, {fromBlock: 0, toBlock: 'latest'});

// watcher.watch(function(error,result){
//     if (!error){
//         console.log(result)
//     }
//     else{
//         console.log(error)
//     }
// })

// test.deposit(10, function(error, result){
//     console.log(result)
// })

// var events = test.allEvents({fromBlock: 0, toBLock: 'latest'});
//     events.get(function(error, logs){
//         if (!error){
//             console.log("event logs")
//             console.log(logs)
//         }
//         else{
//             console.log(error)
//         }
//     })



loadProofJson()

function verifyProof(proof){
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

    unFormattedContractAddress = document.getElementById("contractAddress").innerHTML
    CAStartIndex = unFormattedContractAddress.indexOf('0')
    contractAddress = unFormattedContractAddress.substring(CAStartIndex, CAStartIndex+42)

    var verifier = verifierContract.at(contractAddress)
    // var verifier = verifierContract.at("0x1593694907d9f7e8f6237e3c829fe28d750953a8")
    
    console.log(verifier)
    
    var instructorEvent = verifier.Verified({}, {fromBlock: 0, toBlock: 'latest'});
    // var instructorEvent = verifierContract.once("Verified", function(error, result){
    //     if (!error){
    //         console.log(result)
    //     }
    //     else{
    //         console.log(error)
    //     }
    // })

    instructorEvent.watch(function(error,result){
        if (!error){
            console.log(result)
            blockNumber = result["blockNumber"]
            txHash = result["transactionHash"]
            web3.eth.getBlockNumber(function (error, result) {
                console.log(result)
                console.log(blockNumber)
                if (result==blockNumber && txHash==document.getElementById("verificationTxHash").innerHTML){
                    document.getElementById("verificationStatus").innerHTML = "Verified"
                }
            })
        }
        else{
            console.log(error)
        }
    })
    
    // var events = verifier.allEvents({fromBlock: 0, toBLock: 'latest'});
    // events.get(function(error, logs){
    //     if (!error){
    //         console.log(logs)
    //     }
    //     else{
    //         console.log(error)
    //     }
    // })
    
    A = proof["proof"]["A"]
    A_p = proof["proof"]["A_p"]
    B = proof["proof"]["B"]
    B_p = proof["proof"]["B_p"]
    C = proof["proof"]["C"]
    C_p = proof["proof"]["C_p"]
    H = proof["proof"]["H"]
    K = proof["proof"]["K"]
    witness = proof["input"]

    console.log(witness);

    for (var i =0 ; i<witness.length; i++){
        // witness[i] = parseInt(witness[i], 10)
        witness[i] = BigNumber(witness[i])
    }
    console.log(witness)

    verifier.verifyTx(A, A_p, B, B_p, C, C_p, H, K, witness, function(error, result){
    // verifierContract.verifyTx().call(A, A_p, B, B_p, C, C_p, H, K, witness, function(error, result){
        if(!error){
            web3.eth.getTransactionReceipt(result, function(error, result){
                if(!error){
                    document.getElementById("verificationTxHash").innerHTML = result["transactionHash"]
                    console.log(result)
                    
                }
                else{
                    console.log(error)
                }
            })
        }
        else{
            console.error(error)
        }
    })


}


function loadProofJson(callback){
    var api = 'http://localhost:8000/proofJson';
    const xhr = new XMLHttpRequest();

    xhr.responseType = 'json';
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            proof = this.response
            console.log(proof)
            verifyProof(proof)
            // connectMetamask(res, callback)
        }
        return this.response
    }
    xhr.open('GET', api, true);
    xhr.send();
}



// 1 is main ethereum network
// desiredNetwork = 8545

// function connectMetamask(proof, callback){
//     if (typeof window.ethereum === 'undefined') {
//         alert('Looks like you need a Dapp browser to get started.')
//         alert('Consider installing MetaMask!')
    
//     } else {
//         ethereum.enable()

//         //User reject request
//             .catch(function (reason) {
//             if (reason === 'User rejected provider access') {
//             } else {
//                 console.log(reason)
//                 alert('There was an issue signing you in.')
//             }
//             })
//             .then(function (accounts) {
//                 // You also should verify the user is on the correct network:
//                 // if (ethereum.networkVersion !== desiredNetwork) {
//                 //   alert('This application requires the main network, please switch it in your MetaMask UI.')
            
//                 // We plan to provide an API to make this request in the near future.
//                 // https://github.com/MetaMask/metamask-extension/issues/3663
//                 // }
//                 const account = accounts[0]
//                 callContract(account, proof, callback)
//             })
//     } 
// }

// function callContract(account, proof, callback) {
//     console.log(account)
//     unFormattedContractAddress = document.getElementById("contractAddress").innerHTML
//     CAStartIndex = unFormattedContractAddress.indexOf('0')
//     contractAddress = unFormattedContractAddress.substring(CAStartIndex, CAStartIndex+42)
//     const method = 'eth_call'
//     const parameters = [{
//         from: account,
//         to: contractAddress,
//         gas: "0x2DC6C0",  // 3,000,000 gas
//         gasPrice: "0x9184e72a000" , // Lots
//         data: "0x1"
//         // sample hello world data for debugging
//         // data: "6060604052341561000c57fe5b5b6101598061001c6000396000f30060606040526000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063cfae32171461003b575bfe5b341561004357fe5b61004b6100d4565b604051808060200182810382528381815181526020019150805190602001908083836000831461009a575b80518252602083111561009a57602082019150602081019050602083039250610076565b505050905090810190601f1680156100c65780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b6100dc610119565b604060405190810160405280600381526020017f486921000000000000000000000000000000000000000000000000000000000081525090505b90565b6020604051908101604052806000815250905600a165627a7a72305820ed71008611bb64338581c5758f96e31ac3b0c57e1d8de028b72f0b8173ff93a10029"
//     }]
//     const from = account

//     // Now putting it all together into an RPC request:
//     const payload = {
//         method: method,
//         params: parameters,
//         from: from,
//     }

//     // Methods that require user authorization like this one will prompt a user interaction.
//     // Other methods (like reading from the blockchain) may not.
//     ethereum.sendAsync(payload, function (err, response) {
//         console.log("Attempting to send transaction")
//         const rejected = 'User denied transaction signature.'
//         if (response.error && response.error.message.includes(rejected)) {
//             console.log(`Permission Error`)
//         }
    
//         if (err) {
//             console.log('There was an issue, please try again.')
//         }
    
//         if (response.result) {
//             // If there is a response.result, the call was successful.
//             // In the case of this method, it is a transaction hash.
//             const txHash = response.result
//             console.log('Contract Deployed at ' + txHash)
//             document.getElementById("txHash").value = txHash;
//             pollForCompletion(account, txHash, callback)
//         }
//         })
// }

// function pollForCompletion (account, txHash, callback) {
//     let calledBack = false
  
//     // Normal ethereum blocks are approximately every 15 seconds.
//     // Here we'll poll every 2 seconds.
//     // Checks for contract address
//     const checkInterval = setInterval(function () {
  
//       const notYet = 'response has no error or result'
//       ethereum.sendAsync({
//         method: 'eth_getTransactionReceipt',
//         params: [ txHash ],
//       }, function (err, response) {
//         if (calledBack) return
//         if (err || response.error) {
//           if (err.message.includes(notYet)) {
//             return 'transaction is not yet mined'
//           }
  
//           callback(err || response.error)
//         }
  
//         // We have successfully verified the mined transaction.
//         // Mind you, we should do this server side, with our own blockchain connection.
//         // Client side we are trusting the user's connection to the blockchain.
//         const txReceipt = response.result
//         console.log(txReceipt)
//         clearInterval(checkInterval)
//         calledBack = true
//         callback(null, txReceipt)
//       })
//     }, 2000)
// }


// function callback(err, message) {
//     if (err == undefined){
//         console.log("callback has been reached. Verificationt successful.")
//         document.getElementById("deployStatus").innerHTML = "Verification Complete";
        

//     }
//     else {
//         console.log(err)
//     }
// }