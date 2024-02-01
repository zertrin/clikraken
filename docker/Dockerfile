FROM python:3.11-alpine
ARG CLIKRAKEN_VERSION

RUN adduser -D marcel
USER marcel

RUN mkdir -p ~/.venv && \
    python3 -m venv ~/.venv/clikraken && \
    source ~/.venv/clikraken/bin/activate && \
    pip --no-cache-dir install clikraken==$CLIKRAKEN_VERSION && \
    mkdir -p ~/.config/clikraken

WORKDIR /home/marcel
VOLUME ["/home/marcel/.config/clikraken"]
ENTRYPOINT ["/home/marcel/.venv/clikraken/bin/clikraken"]
CMD ["--help"]
