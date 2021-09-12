DATESTR := $(shell date +%Y-%m-%d_%H%M%S)

all: clean_dist build_sdist build_wheel

clean_dist:
	mkdir -p dist_archive/$(DATESTR)
	-mv dist/* dist_archive/$(DATESTR)/

build_sdist:
	python setup.py sdist

build_wheel:
	python setup.py bdist_wheel

publish_to_pypi:
	twine upload -r pypi dist/*

setup_dev: inst_req_prod inst_req_dev inst_dev

inst_req_prod:
	pip install -r requirements.txt

inst_req_dev:
	pip install -r requirements_dev.txt

dev: uninst_dev inst_dev

uninst_dev:
	python setup.py develop --uninstall

inst_dev:
	python setup.py develop

test:
	tox

