# Docker container for clikraken

This folders contains:

- a `Dockerfile` to build a container based on python3.x-alpine with `clikraken` installed using pip.
- a `Makefile` to help build and tag the built images.
    - Note: The `CLIKRAKEN_VERSION` environement variable should be set to the version of `clikraken` to install in the container. For example: `CLIKRAKEN_VERSION=0.8.3.2 make build`.
- a `run.sh` script that demonstrate usage of the docker container

The latest image I built is published on docker hub: <https://hub.docker.com/r/clikraken/clikraken>

In a nutshell, once you have either built the image or pulled from docker hub, you can use it like this:

```
docker run --rm -v ~/.config/clikraken:/home/clikraken/.config/clikraken:ro clikraken/clikraken:latest <clikraken arguments>
```

Note that you can pass your local clikraken settings directory by mounting it to `/home/clikraken/.config/clikraken` inside the container.

Examples:

```
docker run --rm -v ~/.config/clikraken:/home/clikraken/.config/clikraken:ro clikraken/clikraken:latest --help
docker run --rm -v ~/.config/clikraken:/home/clikraken/.config/clikraken:ro clikraken/clikraken:latest balance
docker run --rm -v ~/.config/clikraken:/home/clikraken/.config/clikraken:ro clikraken/clikraken:latest place buy 0.08 587.12 -p XXBTZEUR
docker run --rm -v ~/.config/clikraken:/home/clikraken/.config/clikraken:ro clikraken/clikraken:latest ticker -p XETHXXBT
```
