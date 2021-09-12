#!/bin/bash
docker run --rm -v ~/.config/clikraken:/home/clikraken/.config/clikraken:ro clikraken/clikraken:latest "$@"
