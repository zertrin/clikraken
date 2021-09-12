FROM python:3.9-alpine
ARG CLIKRAKEN_VERSION

RUN adduser -D clikraken
USER clikraken

RUN mkdir -p ~/.venv && \
    python3 -m venv ~/.venv/clikraken && \
    source ~/.venv/clikraken/bin/activate && \
    pip --no-cache-dir install clikraken==$CLIKRAKEN_VERSION && \
    mkdir -p ~/.config/clikraken

WORKDIR /home/clikraken
VOLUME ["/home/clikraken/.config/clikraken"]
ENTRYPOINT ["/home/clikraken/.venv/clikraken/bin/clikraken"]
CMD ["--help"]
