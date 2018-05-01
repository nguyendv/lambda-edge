FROM ubuntu:16.04
RUN apt update && apt upgrade -y
RUN apt install wget apt-transport-https -y
RUN wget -O - https://deb.openalpr.com/openalpr.gpg.key | apt-key add -
#RUN echo "deb http://deb.openalpr.com/master/ xenial main" > /etc/apt/sources.list.d/openalpr.list
RUN apt update
RUN apt install git openalpr openalpr-daemon openalpr-utils libopenalpr-dev -y
RUN git clone https://github.com/openalpr/openalpr
RUN apt install python3 -y
WORKDIR openalpr/src/bindings/python
RUN python3 setup.py install
WORKDIR ~
ENTRYPOINT ["tail", "-f", "/dev/null"]

