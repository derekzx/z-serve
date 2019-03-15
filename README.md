# FYP birthday as ZKP

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

2. Deploy gov smart contract

3. Run `node app.js` within `./Development/frontend/compilation server` to start up the compilation folder

4. Run `python3 App.py` (or any other command that you bound Py3 PATH to) within `./Development/frontend/front-end flask` to start up the front-end flask server

5. Access localhost:8000 on your browser to see it for yourself!

6. Desired birthday `01/01/2000` representing 1 Jan 2000 and secret `1`

### Notes
To end testrpc
> fuser -k -n tcp 8545
