FROM continuumio/miniconda3
SHELL ["/bin/bash", "-c"]

ARG PYTHONDONTWRITEBYTECODE=true

COPY ./server/face-demo.yml .

RUN set -x \
    && conda env update -f face-demo.yml \
    && conda clean -afy \
    && find /opt/conda/ -follow -type f -name '*.a' -delete \
    && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
    && find /opt/conda/ -follow -type f -name '*.js.map' -delete

WORKDIR /app

COPY ./data/ ./data/
COPY ./protos/ ./protos/
COPY ./server/ ./server/

WORKDIR /app/server

STOPSIGNAL SIGKILL
CMD ["conda", "run", "-n", "face-demo", "python", "./server.py"]
