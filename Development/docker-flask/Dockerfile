FROM ubuntu:18.10

LABEL maintainer="Derek Chin <github.com/derekzx>"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev bash docker.io python3-pip

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app


ENTRYPOINT [ "python3" ]
EXPOSE 22 5000

CMD [ "App.py" ]
