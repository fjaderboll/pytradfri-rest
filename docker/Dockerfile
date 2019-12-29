FROM ubuntu:bionic

COPY setup.sh /tmp
RUN /tmp/setup.sh && rm /tmp/setup.sh

COPY rest.py /root
EXPOSE 80
ENTRYPOINT exec /root/rest.py
