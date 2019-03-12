const path = require('path');
const fs = require('fs');
const solc = require('solc');
const filePath = path.resolve(__dirname, 'hello.sol');
const source = fs.readFileSync(filePath, 'UTF-8');
console.log(source);
updatedSource = JSON.stringify({
    language: 'Solidity',
    sources: {
      'Hello': {
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
    })
// module.exports = solc.compile(source, 1).contracts[':Hello'];
// console.log(updatedSource)

// console.log(solc.compile(updatedSource)
const compiledContract = JSON.parse(solc.compile(updatedSource));
console.log("output is" + compiledContract)
if(compiledContract.errors) {
    compiledContract.errors.forEach(err => console.log(err.formattedMessage));
}

const contract = compiledContract.contracts['Hello'].HelloWorld;

const abi = contract.abi;

console.log(abi)

// console.log(JSON.stringify(compiledContract))
    // const contracts = output.contracts['Hello'].Hello;  
    // console.log(contracts);
    // for (let contractName in contracts) {
    //     const contract = contracts[contractName];
    //     fs.writeFileSync(path.resolve(buildPath, `${contractName}.json`), JSON.stringify(contract.abi, null, 2), 'utf8');
    // }



// var input = {
// 	language: 'Solidity',
// 	sources: {
// 		'hello.sol': {
// 			content: 'contract C { function f() public { } }'
// 		}
// 	},
// 	settings: {
// 		outputSelection: {
// 			'*': {
// 				'*': [ '*' ]
// 			}
// 		}
// 	}
// }

// var output = JSON.parse(solc.compile(JSON.stringify(input)))

// for (var contractName in output.contracts['test.sol']) {
// 	console.log(contractName + ': ' + output.contracts['test.sol'][contractName].evm.bytecode.object)
// }