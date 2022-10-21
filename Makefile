all: clean pkg

clean:
	rm -rf dist build *.egg-info

pkg:
	python -m build

release: clean all
	python -m twine upload dist/*

proto:
	protoc \
		-I $(CURDIR)/solana-trader-proto/proto \
		--python_betterproto_out=$(CURDIR)/bxsolana/proto \
		$(CURDIR)/solana-trader-proto/proto/api.proto \
		&& echo 'from .api import *' > $(CURDIR)/bxsolana/proto/__init__.py

lint: typecheck analyze fmt-check

fmt:
	black bxsolana

fmt-check:
	black bxsolana --check

analyze:
	flake8 bxsolana

typecheck:
	pyre check

test:
	python -m unittest discover
