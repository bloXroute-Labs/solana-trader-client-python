proto:
	protoc \
		-I $(CURDIR)/solana-trader-proto/proto \
		--python_betterproto_out=$(CURDIR)/bxserum/proto \
		$(CURDIR)/solana-trader-proto/proto/api.proto \
		&& echo 'from .api import *' > $(CURDIR)/bxserum/proto/__init__.py
