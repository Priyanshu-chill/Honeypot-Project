# Base image
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    file \
    libimage-exiftool-perl \
    xxd \
    binutils \
    ssdeep \
    yara \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install \
    pefile \
    yara-python \
    requests

# Create non-root user
RUN useradd -m analyzer

WORKDIR /analysis

RUN mkdir -p /analysis/samples /analysis/reports

COPY analyzer.py /analysis/analyzer.py
COPY vt_lookup.py /analysis/vt_lookup.py
COPY rules /analysis/rules

# Give ownership to non-root user
RUN chown -R analyzer:analyzer /analysis

USER analyzer

CMD ["python3","/analysis/analyzer.py"]
