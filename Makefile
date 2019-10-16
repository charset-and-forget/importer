IMAGE := importer

.PHONY: start
start: build
	docker-compose up


.PHONY: build
build:
	docker-compose build
