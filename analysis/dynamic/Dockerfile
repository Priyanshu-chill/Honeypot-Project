FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    strace \
    ltrace \
    tcpdump \
    inotify-tools \
    net-tools \
    iputils-ping \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m analyzer

WORKDIR /analysis

RUN mkdir -p /analysis/samples \
             /analysis/reports \
             /analysis/pcap

RUN chown -R analyzer:analyzer /analysis

USER analyzer

CMD ["python3","--version"]
