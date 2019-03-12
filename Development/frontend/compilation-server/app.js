console.log('Server-side code running');

const express = require('express');
const app = express();
var bodyParser = require('body-parser');
var fs = require("fs")
const compile = require('./compile.js')

// app.use(express.bodyParser());

// serve files from the public directory
app.use(express.static('./'));
app.use(bodyParser.json());


// start the express web server listening on 8001
app.listen(8001, () => {
  console.log('listening on 8001');
});

// serve the homepage
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

// serve the compilation
app.post('/compile', async (req, res) => {
  // console.log(req.body);
  verifierContract = req.body.verifierContract

  fs.writeFile("./contracts/verifier.sol", verifierContract, async function(err, data) {
    if (err) console.log(err);

    console.log("Successfully wrote verifier contract to file");

    // Reads raw .sol file and converts it into desired json format for compiler
    let verifierSource = await compile.readSmartContract("./contracts/verifier.sol");
    console.log("Smart Contract is " + verifierSource.substring(0,500))

    // Compiles smart contract
    let smartContract = await compile.compileSmartContract(verifierSource, "./contracts");

    // fs.readFile('./contracts/compiledContract.json', async function(err, data) {
    //   if (err) console.log(err)
    //   compiledContract = JSON.parse(data)
    //   console.log("hi")
    //   res.send(compiledContract)
    // });
  });


  // var timeout
  // TODO: Do while loop to prevent race conditions
  // Set timeout because of global variable in solc, unable to wrap in a promise/async await successfully
  console.log("reaching timeout")
  var timer = setInterval(function() {
    if (fs.existsSync('./contracts/compiledContract.json')) {
      console.log("reading file to return")
      fs.readFile('./contracts/compiledContract.json', function(err, data) {
        if (err) console.log(err)
        compiledContract = JSON.parse(data)
        console.log("returning now")
        res.send(compiledContract)
        fs.unlink("./contracts/compiledContract.json", function(err, res){
          if (err) console.log(err)
          console.log("Deleting compiled contract")
        });
        clearInterval(timer);
      });
    } else {
      console.log("waiting for compilation")
      // clearTimeout(timeout)
    }
    // console.log("Compiled Contract is" + smartContract);
    // let json = compile.jsonSmartContract("./contracts/verifier.sol");
    // console.log("Read file is" + json);
    // compile.jsonSmartContract("compiledContract.json").then(function(json) {
    //   console.log("Read file is" + json.substring(0,30));
    // }, function(err) {
    //   console.log(err);
    // });

  }, 1000)
  // clearTimeout(timeout)
  // console.log("Compiled Contract is " + smartContract)
  // res.send(data)



  // compile.deploySmartContract("verifier.sol", function(err, res){
  //   console.log("hi")  
  //   if (err) {
  //     console.log('Error' + err)
  //   } else {
  //     console.log("Hi")
  //   }
  // })
  
});
