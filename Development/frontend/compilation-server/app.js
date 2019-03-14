console.log('Server initialised');

const express = require('express');
const app = express();
var bodyParser = require('body-parser');
var fs = require("fs")
const compile = require('./compile.js')

// Serve files from the public directory
app.use(express.static('./'));
app.use(bodyParser.json());

// Start web server listening on port 8001
app.listen(8001, () => {
  console.log('listening on 8001');
});

// Serves homepage (help)
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

// Serves compilation api
app.post('/compile', async (req, res) => {
  verifierContract = req.body.verifierContract

  // Writes verifier contract to file
  fs.writeFile("./contracts/verifier.sol", verifierContract, async function(err, data) {
    if (err) console.error(err);

    console.log("Successfully wrote verifier contract to file");

    // Reads raw .sol file and converts it into desired json format for compiler
    let verifierSource = await compile.readSmartContract("./contracts/verifier.sol");
    console.log("Smart Contract is " + verifierSource.substring(0,500))

    // Compiles smart contract
    let smartContract = await compile.compileSmartContract(verifierSource, "./contracts");

    // NOTE: This block can be used instead to return response once await function for solc is fixed
    /* 
    fs.readFile('./contracts/compiledContract.json', async function(err, data) {
      if (err) console.log(err)
      compiledContract = JSON.parse(data)
      console.log("hi")
      res.send(compiledContract)
    });
    */
  });

  // Set timeout because of global variable in solc, unable to wrap in a promise/async await successfully
  var timer = setInterval(function() {

    // Interval checks will continue until compiled contract is saved to server
    if (fs.existsSync('./contracts/compiledContract.json')) {
      console.log("reading file to return")
      fs.readFile('./contracts/compiledContract.json', function(err, data) {
        if (err) console.log(err)
        compiledContract = JSON.parse(data)
        console.log("returning file now")
        res.send(compiledContract)

        // Deletes both raw and compiled contracts
        fs.unlink("./contracts/compiledContract.json", function(err, res){
          if (err) console.log(err)
          console.log("Deleting compiled contract")
        });
        fs.unlink("./contracts/verifier.sol", function(err, res){
          if (err) console.log(err)
          console.log("Deleting compiled contract")
        });
        clearInterval(timer);
      });
    } else {
      console.log("waiting for compilation")
    }
  }, 1000)  
});
