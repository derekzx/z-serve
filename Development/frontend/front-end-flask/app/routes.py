from app import app
from flask import request, json, jsonify, render_template, flash, redirect, send_from_directory
import requests
from app.Forms import generateForm, deployForm, verifyForm
import os
import subprocess
import time, datetime
import contextlib

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

# Landing page
@app.route('/index')
@app.route('/')
def index():
    # return "hello"
    user = {'username': 'Derek'}
    return render_template('index.html', title='Home', user=user)


# Page to generate smart contract by hitting Zokrates docker container
@app.route('/generate', methods=['GET', 'POST'])  
def generate():
    form = generateForm()

    # Placeholder for user
    user = {'username': 'Derek'}

    # Only returns compile page once form is filled and submitted
    if form.validate_on_submit():
        flash('Login requested for user {}, birthday={}'.format(
            form.pubKey.data, form.birthday.data))

        # Converts to public key to bytes, pads it to 256b and splits it into 2 128b inputs
        # Reason: Zokrates uses signed 128b (same amount of bits as unsigned 256b)
        pubKey = format(int(form.pubKey.data, 16), '0>128b')
        while(len(pubKey) < 256):
            pubKey = '0' + pubKey
        
        pubKeyFirst = int(pubKey[:128], 2)
        pubKeySecond = int(pubKey[128:], 2)

        # Converts birthday hash in the same way as public key
        birthdayHash = format(int(form.birthdayHash.data, 16), '0>128b')
        while(len(birthdayHash) < 256):
            birthdayHash = '0' + birthdayHash
        
        birthdayHashFirst = int(birthdayHash[:128], 2)
        birthdayHashSecond = int(birthdayHash[128:], 2)     

        # Currently running in Singapore (+8 GMT). Change as needed
        timeZoneDifference = 28800 
        birthdayUnix = int(time.mktime(datetime.datetime.strptime(form.birthday.data, "%d/%m/%Y").timetuple())) + timeZoneDifference

        secret = form.secret.data

        json_generate = {
            "currentTime"       : int(time.time()),
            "pubKeyFirst"       : pubKeyFirst,
            "pubKeySecond"      : pubKeySecond,
            "birthdayUnix"      : birthdayUnix,
            "secret"            : int(secret),
            "birthdayHashFirst" : birthdayHashFirst,
            "birthdayHashSecond": birthdayHashSecond
        }

        # Create Smart Contract with Zokrates docker container
        res = requests.post('http://18.136.198.116/generate', json=json_generate)
        json_res = res.json()
        contract = json_res["contract"]

        # Formats json proof for pretty print
        json_proof = json.dumps(json_res["proof"], sort_keys = True, indent = 4, separators = (',', ': '))

        # Save smart contract file
        smart_contract_file = open("./contracts/verifier.sol", "w")
        smart_contract_file.write(contract)
        smart_contract_file.close()

        # Save proof contract file
        proof_file = open("./contracts/proof.json", "w")
        proof_file.write(json.dumps(json_res))
        proof_file.close()
        return render_template('compile_start.html', user=user, proof=json_proof)

    return render_template('generate.html', title='Sign In', form=form)

@app.route('/compile', methods=['GET'])  
def compile():
    placeholder = {'username': 'DerekC'}

    verifierContractLocation = os.path.join(SITE_ROOT, "../contracts", "verifier.sol")
    verifierContractFile = open(verifierContractLocation, "r")
    verifierContract = verifierContractFile.read()

    verifierContract_json = {
        "verifierContract" : verifierContract
    }
    # print(verifierContract_json)

    # Calls node js compiler
    res = requests.post('http://127.0.0.1:8001/compile', json=verifierContract_json)
    
    # Save compiled contract file
    compiled_contract_file = open("./contracts/compiledContract.json", "w")
    compiled_contract_file.write(json.dumps(res.json()))
    compiled_contract_file.close()

    # print("request response is: " + res.text)
    return render_template('compile_finish.html', user=placeholder)

# Deploys contract
@app.route('/deploy', methods=['GET', 'POST'])  
def deploy():
    form = deployForm()

    placeholder = {'username': 'DerekC'}
    if form.validate_on_submit():
        verificationForm = verifyForm()
        flash('Your contract has been deployed')

        return render_template('verify.html', user=placeholder, txHash=form.txHash.data, contractAddress=form.contractAddress.data, form=verificationForm)
    
    return render_template('deploy.html', user=placeholder, form=form)

# Returns compiled smart contract in json form
@app.route('/scJson', methods=['GET'])  
def scJson():
    json_url = os.path.join(SITE_ROOT, "../contracts", "compiledContract.json")
    data = json.load(open(json_url))

    # Deletes file after sending
    with contextlib.suppress(FileNotFoundError):
        os.remove(json_url)

    return jsonify(data)

# Returns proof in json form
@app.route('/proofJson', methods=['GET'])  
def proofJson():
    json_url = os.path.join(SITE_ROOT, "../contracts", "proof.json")
    proof = json.load(open(json_url))
    
    # Deletes file after sending
    with contextlib.suppress(FileNotFoundError):
        os.remove(json_url) 

    # Converts to string to avoid over-flow problems in json
    witness_str = []
    for i in proof["input"]:
        witness_str.append(str(i))
    proof["input"] = witness_str
    
    return jsonify(proof)

# Favicons
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(SITE_ROOT, "../static"),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')