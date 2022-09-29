FROM ubuntu:18.04

RUN apt-get update && apt-get install -y gcc make gawk bison python3 python3-pip bear
RUN pip3 install requests beautifulsoup4
