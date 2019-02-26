from app import app
from flask import request, json, jsonify
import os
import subprocess
import time

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/index2')
def index2():
    return "Hello, World!"

@app.route('/shell', methods=['POST'])  
def shell():
    data = request.get_json()
    data_in = data.get("input")
    subprocess.call(["chmod", "u+x", "test.sh"])
    # p1 = subprocess.Popen(["./test.sh", data_in], stdout=subprocess.PIPE)
    script = subprocess.Popen(["./test.sh"])

    # subprocess.call(["mkdir", "my_directory"])
    # p1 = subprocess.Popen(["pwd"], stdout=subprocess.PIPE)
    # pwd = p1.communicate()

    # print(pwd)

    # time.sleep(10)
    script.wait()


    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    proof_file = os.path.join(BASE_DIR, '../code/proof.json')
    contract_file = os.path.join(BASE_DIR, '../code/verifier.sol')

    proof = json.load(open(proof_file))
    contract = open(contract_file).read()
    proof["contract"] = contract

    return jsonify(proof)

