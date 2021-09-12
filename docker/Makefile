IMAGENAME := clikraken/clikraken
DATESTR := $(shell date +%Y%m%d-%H%M%S)
CLIKRAKEN_VERSION := $(shell ../src/clikraken/__about__.py)

build:
	docker build --network=host --build-arg CLIKRAKEN_VERSION=$(CLIKRAKEN_VERSION) -t $(IMAGENAME):latest .
	docker tag $(IMAGENAME):latest $(IMAGENAME):$(DATESTR)
	docker tag $(IMAGENAME):latest $(IMAGENAME):$(CLIKRAKEN_VERSION)

rmi:
	docker rmi $(IMAGENAME):latest

