FROM python:3.7-slim

COPY ./server/requirements.txt ./

RUN set -x \
    && apt-get update \
    && apt-get install -y \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender1 \
        python3-keras \
    && pip3 install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./data/ ./data/
COPY ./protos/ ./protos/
COPY ./server/ ./server/

WORKDIR /app/server

STOPSIGNAL SIGKILL
CMD ["python", "./server.py"]
