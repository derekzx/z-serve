from app import app
from flask import request, json, jsonify
import os
import subprocess
import time

# Returns simple message to guide users
@app.route('/')
@app.route('/index')
def index():
    return "Please use /generate endpoint to generate smart contract and proof"

# API endpoint to generate smart contract
@app.route('/generate', methods=['POST'])  
def generate():
    data = request.get_json()

    # Gives right to bash script just in case
    subprocess.call(["chmod", "u+x", "generateSC.sh"])

    # Formats input and uses it as an input for bash script
    # Format: currenttime, pubkeyfirst, pubkeysecond, digest1, digest2, birthday, secret
    currentTime = data["currentTime"]
    pubKeyFirst = data["pubKeyFirst"]
    pubKeySecond = data["pubKeySecond"]
    birthdayHashFirst = data["birthdayHashFirst"]
    birthdayHashSecond = data["birthdayHashSecond"]
    birthday = data["birthdayUnix"]
    secret = data["secret"]

    str_input = "{0} ".format(currentTime) + "{0} ".format(pubKeyFirst) + "{0} ".format(pubKeySecond) + "{0} ".format(birthdayHashFirst) + "{0} ".format(birthdayHashSecond) + "{0} ".format(birthday) + "{0}".format(secret) 

    script = subprocess.Popen(["./generateSC.sh"], stdin=subprocess.PIPE)
    bytes_input = bytes(str_input, 'ascii')
    result = script.communicate(bytes_input)

    # Waits for zokrates finish generating contract and proof
    script.wait()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    proof_file = os.path.join(BASE_DIR, '../code/proof.json')
    contract_file = os.path.join(BASE_DIR, '../code/verifier.sol')

    proof = json.load(open(proof_file))
    contract = open(contract_file).read()
    proof["contract"] = contract

    os.remove(proof_file)
    os.remove(contract_file)

    return jsonify(proof)

