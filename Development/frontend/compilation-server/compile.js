var path = require('path');
var fs = require('fs');
var Web3 = require('web3')
solc = require('solc');
var async = require('async');

console.log("imported modules")

/**
 * Function takes in file location and reads it
 * 
 * @param {string} smartContractLocation    File path of raw smart contract
 * @returns {JSON} updatedSource            JSON with smart contract and required parameters included
 */
exports.readSmartContract = async function(smartContractLocation, cb){
    var filePath = path.resolve(__dirname, smartContractLocation);
    const source = fs.readFileSync(filePath, 'UTF-8');
    updatedSource = JSON.stringify({
        language: 'Solidity',
        sources: {
        'Verification': {
            content: source,
            }
        },
        settings: {
            outputSelection: {
                '*': {
                    '*': [ '*' ]
                }
            }
        }
        }
        )
    console.log("returning updated source")
    return updatedSource
}

/**
 *  Function compiles smart contract
 *  Compiler version currently used: 0.4.21+commit.dfe3193c.Emscripten.clang
 *  NOTE: Line that is retrieving file within solc.js - var solcV047 = solc.useVersion("v0.4.7.commit.822622cf"); 
 * 
 *  @param {JSON} smartContract                 Raw smart contract with required parameters
 *  @param {string} output_location             Output file of smart contract
 *  @returns {JSON} compiledContract            JSON of compiled contract
 */
exports.compileSmartContract = async function(smartContract, output_location, cb){
    var compiledContract

    // Loads previous solc compiler
    solc.loadRemoteVersion("v0.4.21+commit.dfe3193c", async function(err, solc){
        if(err) console.error(err);
        else {
            
            // Compiles contract
            compiledContract = JSON.parse(solc.compile(smartContract));
            if(compiledContract.errors) {
                compiledContract.errors.forEach(err => console.log(err.formattedMessage));
            }
            jsonData = JSON.stringify(compiledContract);
            
            fs.writeFileSync(output_location + "/compiledContract.json", jsonData, function(err) {
                if (err) console.error(err);
            });
            console.log("Contract compiled successfully" + compiledContract)     
        }
    });
    return compiledContract 
}

/**
 *  This function can be used to test that the compiled contract are similar in both flask and node servers
 * 
 *  @param {string} compiledContractLocation    File path of compiled contract
 *  @returns {string} source                    Compiled contract
 */
exports.jsonSmartContract = async function(compiledContractLocation, cb) {
    var filePath = path.resolve(__dirname, compiledContractLocation);
    const source = fs.readFileSync(filePath, 'UTF-8');
    return source
}