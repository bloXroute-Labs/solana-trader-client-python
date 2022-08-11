proto:
	protoc \
		-I $(CURDIR)/solana-trader-proto/proto \
		--python_betterproto_out=$(CURDIR)/bxserum/proto \
		$(CURDIR)/solana-trader-proto/proto/api.proto \
		&& echo 'from .api import *' > $(CURDIR)/bxserum/proto/__init__.py

lint: typecheck pylint

fmt:
	black bxserum

fmt-check:
	black bxserum --check

flake8:
	flake8 bxserum
pylint:
	pylint bxserum

typecheck:
	pyre check

test:
	python -m unittest discover