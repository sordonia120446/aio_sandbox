FROM python:3.7

RUN apt-get update && \
        apt-get install -y \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        pkg-config

ADD . /app
WORKDIR /app
RUN pip install -r /app/requirements.txt

CMD [ "python", "/app/server.py" ]
