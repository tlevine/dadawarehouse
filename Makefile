.PHONY: test check

PYTHONPATH=.
export PYTHONPATH

check:
	python3 example/export_to_cubes.py
	slicer model validate /tmp/model.json

test:
	nosetests3
