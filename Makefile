.PHONY: test check

PYTHONPATH=.
export PYTHONPATH

check:
	./bin/dada-model
	slicer model validate /tmp/model.json

test:
	nosetests3
