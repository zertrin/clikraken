#!/bin/bash
docker run --rm -v ~/.config/clikraken:/home/marcel/.config/clikraken:ro zertrin/clikraken:latest "$@"
