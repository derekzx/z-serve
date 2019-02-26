#!/bin/bash          

cd ZoKrates
# docker run -v $PWD/code:/home/zokrates/ZoKrates/target/debug/code -ti zokrates_tutorial /bin/bash
#creates bash shell in container
docker run -v /home/derek/Desktop/FYP/Development/flask/code:/home/zokrates/ZoKrates/target/debug/code -i zokrates_tutorial bash <<'EOF'

echo hello
exit
EOF


