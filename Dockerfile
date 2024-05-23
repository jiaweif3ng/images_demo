FROM tangwan/python-firefox-driver

RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list && \
    sed -i s@/security.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list && \
    apt-get clean && \
    apt-get update && \
    apt install -y vim && \
    apt-get install -y wget

WORKDIR /home/csmn
ADD firefox-115.10.0esr.tar.bz2 .
WORKDIR /usr/local/bin
ADD geckodriver-v0.34.0-linux64.tar.gz .

WORKDIR /home/demo

ADD requirements.txt .
ADD config.py .
ADD jiucai_api.py .
ADD jiucai.py .
ADD server_jiucai.py .
ADD requirements.txt .

RUN pip install -r requirements.txt