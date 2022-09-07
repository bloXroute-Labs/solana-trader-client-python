all:
	python -m build

clean:
	rm -rf dist build *.egg-info

release: clean all
	python -m twine upload dist/*

proto:
	protoc \
		-I $(CURDIR)/solana-trader-proto/proto \
		--python_betterproto_out=$(CURDIR)/bxserum/proto \
		$(CURDIR)/solana-trader-proto/proto/api.proto \
		&& echo 'from .api import *' > $(CURDIR)/bxserum/proto/__init__.py

lint: typecheck analyze fmt-check

fmt:
	black bxserum

fmt-check:
	black bxserum --check

analyze:
	flake8 bxserum

typecheck:
	pyre check

test:
	python -m unittest discover