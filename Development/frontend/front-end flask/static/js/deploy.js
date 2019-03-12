
// var web3 = new Web3();
// web3.setProvider(new web3.providers.HttpProvider("http://localhost:8545"));

// loadFile();

// function loadFile() {

// }

loadSCJson(callback)

function loadSCJson(callback){
    var api = 'http://localhost:8000/scJson';
    const xhr = new XMLHttpRequest();

    xhr.responseType = 'json';
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            res = this.response
            bytecode_data = this.response["contracts"]["Verification"]["Verifier"]["evm"]["bytecode"]["object"]
            // console.log(res)
            // console.log(bytecode_data)
            connectMetamask(bytecode_data, callback)
        }
        return this.response
    }
    xhr.open('GET', api, true);
    xhr.send();
}



function connectMetamask(bytecode_data, callback){
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
                // You also should verify the user is on the correct network:
                // if (ethereum.networkVersion !== desiredNetwork) {
                //   alert('This application requires the main network, please switch it in your MetaMask UI.')
            
                // We plan to provide an API to make this request in the near future.
                // https://github.com/MetaMask/metamask-extension/issues/3663
                // }
                const account = accounts[0]
                deployContract(account, bytecode_data, callback)
            })
    } 
}

function deployContract(account, bytecode_data, callback) {
    console.log(account)
    const method = 'eth_sendTransaction'
    const parameters = [{
        from: account,
        gas: "0x2DC6C0",  // 3,000,000 gas
        gasPrice: "0x9184e72a000" , // Lots
        data: bytecode_data
        // sample hello world data for debugging
        // data: "6060604052341561000c57fe5b5b6101598061001c6000396000f30060606040526000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063cfae32171461003b575bfe5b341561004357fe5b61004b6100d4565b604051808060200182810382528381815181526020019150805190602001908083836000831461009a575b80518252602083111561009a57602082019150602081019050602083039250610076565b505050905090810190601f1680156100c65780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b6100dc610119565b604060405190810160405280600381526020017f486921000000000000000000000000000000000000000000000000000000000081525090505b90565b6020604051908101604052806000815250905600a165627a7a72305820ed71008611bb64338581c5758f96e31ac3b0c57e1d8de028b72f0b8173ff93a10029"
    }]
    const from = account

    // Now putting it all together into an RPC request:
    const payload = {
        method: method,
        params: parameters,
        from: from,
    }

    // Methods that require user authorization like this one will prompt a user interaction.
    // Other methods (like reading from the blockchain) may not.
    ethereum.sendAsync(payload, function (err, response) {
        console.log("Attempting to send transaction")
        const rejected = 'User denied transaction signature.'
        if (response.error && response.error.message.includes(rejected)) {
            console.log(`Permission Error`)
        }
    
        if (err) {
            console.log('There was an issue, please try again.')
        }
    
        if (response.result) {
            // If there is a response.result, the call was successful.
            // In the case of this method, it is a transaction hash.
            const txHash = response.result
            console.log('Contract Deployed at ' + txHash)
            document.getElementById("txHash").value = txHash;
            pollForCompletion(account, txHash, callback)
        }
        })
}

function pollForCompletion (account, txHash, callback) {
    let calledBack = false
  
    // Normal ethereum blocks are approximately every 15 seconds.
    // Here we'll poll every 2 seconds.
    // Checks for contract address
    const checkInterval = setInterval(function () {
  
      const notYet = 'response has no error or result'
      ethereum.sendAsync({
        method: 'eth_getTransactionReceipt',
        params: [ txHash ],
      }, function (err, response) {
        if (calledBack) return
        if (err || response.error) {
          if (err.message.includes(notYet)) {
            return 'transaction is not yet mined'
          }
  
          callback(err || response.error)
        }
  
        // We have successfully verified the mined transaction.
        // Mind you, we should do this server side, with our own blockchain connection.
        // Client side we are trusting the user's connection to the blockchain.
        const txReceipt = response.result
        console.log(txReceipt)
        clearInterval(checkInterval)
        calledBack = true
        // getContractAddress(account, txHash, callback)
        document.getElementById("contractAddress").value = txReceipt["contractAddress"];
        callback(null, txReceipt)
      })
    }, 2000)
}


function callback(err, message) {
    if (err == undefined){
        console.log("callback has been reached. Deployment successful.")
        document.getElementById("deployStatus").innerHTML = "Deployment Complete";
        

    }
    else {
        console.log(err)
    }
}