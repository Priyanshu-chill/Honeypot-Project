# Base image — start from Ubuntu
FROM ubuntu:22.04

# Who made this
LABEL maintainer="Priyanshu-chill"

# Update and install tools
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    wget \
    net-tools \
    iputils-ping

# Create a working directory inside container
WORKDIR /app

# Copy a file from your VM into container
COPY test_script.py .

# Default command when container starts
CMD ["python3", "test_script.py"]