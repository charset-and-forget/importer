IMAGE := importer

.PHONY: build
build:
	docker build -t $(value IMAGE):latest .
