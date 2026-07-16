# Base image
FROM ubuntu:22.04

# Avoid interactive prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Install static analysis tools
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    file \
    libimage-exiftool-perl \
    xxd \
    binutils \
    ssdeep \
    yara

# Install Python libraries
RUN pip3 install \
    pefile \
    yara-python \
    requests

# Create working directory
WORKDIR /analysis

# Create folders for input and output
RUN mkdir -p /analysis/samples /analysis/reports

# Copy analyzer script
COPY analyzer.py /analysis/analyzer.py
COPY vt_lookup.py /analysis/vt_lookup.py

COPY rules /analysis/rules

# Default command
CMD ["python3",  "/analysis/analyzer.py"]
