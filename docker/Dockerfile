FROM ubuntu:bionic

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get update && apt-get install -y python3-pip
COPY tmp/requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt && rm /tmp/requirements.txt

COPY install-coap-client.sh /tmp
RUN /tmp/install-coap-client.sh && rm /tmp/install-coap-client.sh

COPY tmp/rest /root/rest
EXPOSE 80
ENTRYPOINT exec /root/rest/rest.py
