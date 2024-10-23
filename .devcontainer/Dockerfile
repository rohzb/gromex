FROM mcr.microsoft.com/devcontainers/base:ubuntu as base

# Update packages and install python 3.11
RUN apt-get update \
    && apt-get upgrade -y 

RUN apt-get install -y \
        host \
        vim \
        mc \
        telnet \
        bash-completion

FROM base as python
RUN apt-get install -y \
    python3 \
    python3-pip \
    python3-venv
