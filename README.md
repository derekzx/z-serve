# ZKP of age

Goal: To find the age of a person passes a certain value without him revealing his actual age

### Actors:
1. Government: The government will act as the endorsing authority within this protocol which both prover and verifier can trust. 

2. Prover: The prover wants to convince the verifier that he knows of his birthday address that it is above a certain age

3. Verifier: Wants to have a convincing answer as to whether the prover knows of his birthday address and is above a certain age

### Components:
1. Government Smart Contract: Stores data in the mapping publickey -> birthdayHash and these key-value pairs are publicly accessible

2. Verification Smart Contract: Verifies that the prover has the correct proof.

3. Zokrates: Zokrates will be hosted on an Amazon EC2 instance with all the commands available to call via API. The DSL for this use case will be the following:
```
def function(private s, private birthday, public pubKey, public birthdayHash, public currentTime):
assert bdayHash == H(s, pubKey, bday)
assert bday + 18_years > currentTime
```

### Protocol:
#### Setup Phase
1. Government endorses the government smart contract which will contain mappings of all publicKeys -> birthdayHash
2. Government randomly creates a secret s which it passes to the Prover through a secure off-chain channel
3. Government generates birthdayHash of the Prover using H(s, pubKey, bDay) -> {0, 1}256 and stores it in the mapping
4. Prover generates his own birthdayHash using H(s, pubKey, bDay) -> {0, 1}256 and verifies it against the mapping contained within the government smart contract

#### Use Phase
1. Verifier creates a verification contract with Zokrates which require the prover to prove that he possesses a birth date of more than 18 years
2. Verifier deploys the verification contract on the network while revealing the DSL to all provers
3. A prover will use the DSL to generate the contract from Zokrates to ensure that the compiled bytecode is similar to the contract deployed
4. The prover will generate proof by calling the appropriate functions in Zokrates
5. The prover will send the proof to the verification contract
6. If a verifier sees a success event emitted by the verification contract, he can be convinced that the prover which sent the corresponding proof is more than 18 years old

## Folder directory
```

├── Development                 # Folder that contains different servers and docker images to be deployed
│   ├── docker-flask            # Docker image for compilation server
│   ├── frontend                # Front end servers
│   │   ├── compilation-server  # Node server to compile smart contract
│   │   └── front-end flask     # Flask server to handle user-interface and everything else
│   └── solidity                # Hard coded smart contracts templates (eg. Gov contract)
├── vyper                       # Preliminary (hardcoded) files for vyper verifier contract
├── instructions                # Instructions to run files
└── README.md
```

## Requirements

### Necessary
1. Node.js
2. Python 3
3. Metamask extension

### Optional
1. Docker
2. Amazon-cli

## Instructions
1. (If required) Startup local testnet using command below. If using own wallet remember to change the address of the gov smart contract

> testrpc -m "kingdom route frog cannon arena hard brown able south iron puzzle divorce" 

or

> testrpc --account='0xB49CDB28449AE9FBEDF7AF720EFF22ABCAB3CA8AC830375B4D0D5916914F81D8, 10000000000000000000'

2. Deploy gov smart contract manually (eg. [Remix](https://remix.ethereum.org))

3. Run `node app.js` within `./Development/frontend/compilation server` to start up the compilation folder

4. Run `python3 App.py` (or any other command that you bound Py3 PATH to) within `./Development/frontend/front-end flask` to start up the front-end flask server

5. Access localhost:8000 on your browser to see it for yourself!

6. Desired birthday `01/01/2000` representing 1 Jan 2000 and secret `1`

## To-do
1. Creating another API to allow the use of other birth-dates

### Notes
To end testrpc
> fuser -k -n tcp 8545
