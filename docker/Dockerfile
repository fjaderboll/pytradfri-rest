FROM ubuntu:bionic

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

COPY setup.sh /tmp
RUN /tmp/setup.sh && rm /tmp/setup.sh

COPY rest.py /root
EXPOSE 80
ENTRYPOINT exec /root/rest.py
