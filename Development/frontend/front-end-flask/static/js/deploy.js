
loadSCJson(callback)

/**
 * Creates a HTTP request which hits local Flask server to retrieve ./contracts/compiledContract.json
 * This function has a callback unlike verify.js because we are using .ethereum not web3
 * 
 * TODO: Update to Web3
 * 
 * @param {*} callback 
 */
function loadSCJson(callback){
    var api = 'http://localhost:8000/scJson';
    const xhr = new XMLHttpRequest();

    xhr.responseType = 'json';
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            res = this.response
            // We only want the bytecode data for verifier contract.
            // Other contracts that are located here include library contracts
            bytecode_data = this.response["contracts"]["Verification"]["Verifier"]["evm"]["bytecode"]["object"]
            connectMetamask(bytecode_data, callback)
        }
        return this.response
    }
    xhr.open('GET', api, true);
    xhr.send();
}


/**
 * Takes in bytecode data for verifier contract and calls deployContract()
 * @param {*} bytecode_data 
 * @param {*} callback 
 */
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
  
            const account = accounts[0]
            deployContract(account, bytecode_data, callback)
        })
    } 
}

/**
 * Deploys contract
 * @param {*} account 
 * @param {*} bytecode_data 
 * @param {*} callback 
 */
function deployContract(account, bytecode_data, callback) {
    console.log(account)
    const method = 'eth_sendTransaction'
    const parameters = [{
        from: account,
        gas: "0x2DC6C0",  // 3,000,000 gas
        gasPrice: "0x9184e72a000" , // Lots
        data: bytecode_data
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
            console.error(`Permission Error`)
        }
    
        if (err) {
            console.error('There was an issue, please try again.')
        }
    
        if (response.result) {
            // If there is a response.result, the call was successful.
            // In the case of this method, it is a transaction hash.
            const txHash = response.result
            document.getElementById("txHash").value = txHash;
            pollForCompletion(txHash, callback)
        }
    })
}

/**
 * Contract is not immediately deployed. Waits for transaction to be mined.
 * Polling once every 2 seconds to check address of deployed contract
 * NOTE: Normal ethereum blocks are mined every ~15s
 * 
 * TODO: Check manually on server side as well
 * @param {*} txHash 
 * @param {*} callback 
 */
function pollForCompletion (txHash, callback) {
    let calledBack = false
  
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
        const txReceipt = response.result
        clearInterval(checkInterval)
        calledBack = true
        document.getElementById("contractAddress").value = txReceipt["contractAddress"];
        callback(null, txReceipt)
      })
    }, 2000)
}

/**
 * Final callback function reached when deployment is successful
 * @param {*} err 
 * @param {*} message 
 */
function callback(err, message) {
    if (err) console.error(err)
    console.log("callback has been reached. Deployment successful.")
    document.getElementById("deployStatus").innerHTML = "Deployment Complete";
    
}