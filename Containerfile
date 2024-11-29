# Setup dependancy versions
ARG DEBIAN_VERSION=12-slim
 
FROM docker.io/library/debian:${DEBIAN_VERSION}
 
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    python3.11 python3-pip python3-venv \
    python3-tk libsqlite3-dev
 
WORKDIR /usr/src/
# setup python virtual environment
ENV VIRTUAL_ENV=.venv
RUN python3 -m venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

RUN pip3 install wheel
# install needed python libraries
COPY requirements.txt .
RUN pip3 install -r requirements.txt && \
    rm requirements.txt
 
# jank way to have the virtual environment activated
ENTRYPOINT . .venv/bin/activate && /bin/bash
