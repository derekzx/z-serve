var path = require('path');
var fs = require('fs');
var Web3 = require('web3')
solc = require('solc');
var async = require('async');

console.log("imported modules")

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

// Below lists the preferred version of the compiler that we are using
// version:0.4.21+commit.dfe3193c.Emscripten.clang
// var solcV047 = solc.useVersion("v0.4.7.commit.822622cf"); 
// soljson-v0.4.21+commit.dfe3193c.js

exports.compileSmartContract = async function(smartContract, output_location, cb){
    var compiledContract
    solc.loadRemoteVersion("v0.4.21+commit.dfe3193c", async function(err, solc){
        if(err) {
            console.log(err);
        } else {
            compiledContract = JSON.parse(solc.compile(smartContract));
            // console.log("output is" + JSON.stringify(compiledContract));
            if(compiledContract.errors) {
                compiledContract.errors.forEach(err => console.log(err.formattedMessage));
            }
            jsonData = JSON.stringify(compiledContract);
            fs.writeFileSync(output_location + "/compiledContract.json", jsonData, function(err) {
                if (err) {
                    console.log(err);
                }
            });
            console.log(compiledContract)
            console.log("Contract compiled successfully" + compiledContract)     
        }
    });
    return compiledContract 
}

exports.jsonSmartContract = async function(compiledContractLocation, cb) {
    var filePath = path.resolve(__dirname, compiledContractLocation);
    console.log("file path is " + filePath)
    const source = fs.readFileSync(filePath, 'UTF-8');
    return source
}


        // VerifierContract = compiledContract["contracts"]["Verification"]["Verifier"];
        // VerifierABI = compiledContract["contracts"]["Verification"]["Verifier"]["abi"];
        // VerifierBytecode = compiledContract["contracts"]["Verification"]["Verifier"]["evm"]["bytecode"]["object"];
        // let provider = new Web3.providers.HttpProvider("http://localhost:8545");
        // const web3 = new Web3(provider);
        // let Verifier = new web3.eth.Contract(VerifierABI);

        // // console.log("hi")

        // // console.log(Verifier);
        // //remove ""
        // VerifierBytecode = "0x" + JSON.stringify(VerifierBytecode).substr(1).slice(0, -1)
        // // console.log(VerifierBytecode)
        // // Verifier.deploy({
        // //     data: VerifierBytecode
        // // })
        // // .send({
        // //     from: "0x4690fe8ec04967fa12f9ed8550d65ef6f6f23784",
        // //     gas: 2800000
        // // })
        // // .then((newContractInstance) => {
        // //     address = newContractInstance.options.address;
        // //     console.log(newContractInstance.options.address) // instance with the new contract address
        // //     return address;
        // // });
        // Verifier.deploy({
        //         data: VerifierBytecode
        //     })
        //     .send({
        //         from: "0x4690fe8ec04967fa12f9ed8550d65ef6f6f23784",
        //         gas: 2800000
        //     })
        //     .then((newContractInstance) => {
        //         address = newContractInstance.options.address;
        //         console.log(newContractInstance.options.address) // instance with the new contract address
        //         document.getElementById("address").textContent=address;
        //         return address;
                
        //     });
            
        
