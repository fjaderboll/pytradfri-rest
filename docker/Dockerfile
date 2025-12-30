ARG imageName=python:3.14-trixie
FROM $imageName

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

COPY requirements.txt docker/install-coap-client.sh docker/libcoap-4.1.2.zip /tmp/
RUN pip3 install -r /tmp/requirements.txt && rm /tmp/requirements.txt
RUN /tmp/install-coap-client.sh && rm /tmp/install-coap-client.sh /tmp/libcoap-4.1.2.zip

COPY rest /root/rest
COPY create-crypt-key.sh /root/
RUN /root/create-crypt-key.sh && rm -fr /root/create-crypt-key.sh `find /root/rest -type d -name __pycache__`

EXPOSE 80
ENTRYPOINT ["exec", "/root/rest/rest.py"]
