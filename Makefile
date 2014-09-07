.PHONY: test

PYTHONPATH=.
export PYTHONPATH
test:
	python3 example/export_to_cubes.py
	slicer model validate /tmp/model.json
