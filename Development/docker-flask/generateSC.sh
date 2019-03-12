#!/bin/bash          
echo "Reading inputs"

# Input string for verifier
read inputs

cd ZoKrates
# Creates bash shell in container
echo "Starting ZoKrates docker"
# docker build -t zokrates .
# docker run -v /home/derek/Desktop/FYP/Development/flask/ZoKrates/code:/home/zokrates/ZoKrates/target/debug/code -i zokrates bash <<'EOF'
docker run -v /home/ec2-user/code:/home/zokrates/ZoKrates/code -i zokrates bash <<EOF

./zokrates compile -i ZoKrates/code/bdayVerify.code

./zokrates compute-witness -a $inputs

./zokrates setup

./zokrates export-verifier

./zokrates generate-proof

cp verifier.sol /home/zokrates/ZoKrates/code

cp proof.json /home/zokrates/ZoKrates/code

EOF


