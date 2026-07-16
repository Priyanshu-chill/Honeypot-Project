FROM ubuntu:22.04

LABEL maintainer="Priyanshu-chill"

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    wget \
    net-tools \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m appuser

WORKDIR /app

COPY test_script.py .

RUN chown -R appuser:appuser /app

USER appuser

CMD ["python3","test_script.py"]
