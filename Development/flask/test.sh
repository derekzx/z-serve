#!/bin/bash          

cd ZoKrates
# docker run -v $PWD/code:/home/zokrates/ZoKrates/target/debug/code -ti zokrates_tutorial /bin/bash
#creates bash shell in container
# docker run -v /home/derek/Desktop/FYP/Development/flask/ZoKrates/code:/home/zokrates/ZoKrates/target/debug/code -i zokrates bash <<'EOF'
echo "Starting docker"
# docker build -t zokrates .
docker run -v /home/ec2-user/code:/home/zokrates/ZoKrates/code -i zokrates bash <<'EOF'


./zokrates compile -i ZoKrates/code/prime.code

./zokrates compute-witness -a 1 1 1 1 4 2 2

./zokrates setup && ./zokrates export-verifier

./zokrates generate-proof
cp verifier.sol /home/zokrates/ZoKrates/code


cp proof.json /home/zokrates/ZoKrates/code
exit
EOF


