IMAGE := importer

.PHONY: up
up:
	docker-compose up --build


.PHONY: build
build:
	docker build -t $(value IMAGE):latest .

