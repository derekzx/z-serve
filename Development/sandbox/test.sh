#!/bin/bash          

# cd ZoKrates
# #creates bash shell in container
# echo "Starting docker"
# # docker build -t zokrates .
# # docker run -v /home/derek/Desktop/FYP/Development/flask/ZoKrates/code:/home/zokrates/ZoKrates/target/debug/code -i zokrates bash <<'EOF'
# docker run -v /home/ec2-user/code:/home/zokrates/ZoKrates/code -i zokrates bash <<'EOF'


# ./zokrates compile -i ZoKrates/code/bdayVerify.code

# ./zokrates compute-witness -a $

# ./zokrates setup && ./zokrates export-verifier

# ./zokrates generate-proof
# cp verifier.sol /home/zokrates/ZoKrates/code


# cp proof.json /home/zokrates/ZoKrates/code
# exit
# EOF


read a b c d e

./test1.sh <<EOF
$a $b $c $d $e
EOF
echo $a $b $c $d $e
# echo "hello world"