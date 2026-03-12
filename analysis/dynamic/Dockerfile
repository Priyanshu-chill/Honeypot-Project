# Base image
FROM ubuntu:22.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install dynamic analysis tools
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
    curl

# Create working directory
WORKDIR /analysis

# Create folders
RUN mkdir -p /analysis/samples /analysis/reports /analysis/pcap

# Default command
CMD ["python3", "--version"]