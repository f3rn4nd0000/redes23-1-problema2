FROM ubuntu:20.04

RUN apt-get -y update && apt-get -y install python3 python3-pip
RUN mkdir /home/app

EXPOSE 1883

COPY . /home/app
WORKDIR /home/app
RUN python3 -m pip install -r requirements.txt
CMD ["/bin/bash"]
# Dockerfile do dispositivo udp
