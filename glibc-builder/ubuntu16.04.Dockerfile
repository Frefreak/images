FROM ubuntu:16.04

RUN apt-get update && apt-get install -y software-properties-common curl
RUN add-apt-repository -y ppa:jblgf0/python && apt-get update
RUN apt-get install -y gcc make gawk bison python3.7 bear
RUN curl https://bootstrap.pypa.io/get-pip.py | python3.7
RUN pip3 install requests beautifulsoup4
