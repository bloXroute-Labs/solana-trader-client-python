.PHONY: all clean pkg release proto lint fmt fmt-check analyze typecheck test
.PHONY: environment-integration

all: clean pkg

clean:
	rm -rf dist build *.egg-info

pkg:
	python -m build

release: all
	python -m twine upload dist/*

lint: typecheck analyze fmt-check

fmt:
	black bxsolana
	black example

fmt-check:
	black bxsolana --check && black example --check

analyze:
	flake8 bxsolana

typecheck:
	pyre check

test:
	python -m unittest discover test/unit

environment-integration:
	aws s3 cp s3://files.bloxroute.com/trader-api/test_state.json $(CURDIR)/test_state.json