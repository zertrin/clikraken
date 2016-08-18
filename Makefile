DATESTR := $(shell date +%Y-%m-%d_%H%M%S)

all: clean_dist build_sdist build_wheel publish_to_pypi

clean_dist:
	mkdir -p dist_archive/$(DATESTR)
	mv dist/* dist_archive/$(DATESTR)/

build_sdist:
	python setup.py sdist

build_wheel:
	python setup.py bdist_wheel

publish_to_pypi:
	twine upload -r pypi dist/*

dev: uninst_dev inst_dev

uninst_dev:
	python setup.py develop --uninstall

inst_dev:
	python setup.py develop
