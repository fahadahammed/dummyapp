APPLICATION_NAME ?= dummyapp
VERSION ?= v1
REGISTRY ?= docker.io
USERN ?= fahadahammed
CONTAINER_IMAGE = $(REGISTRY)/$(USERN)/$(APPLICATION_NAME)

dockerBuildLatest:
	@echo "Latest Build Started >>"
	docker build --tag $(CONTAINER_IMAGE):latest .
	@echo "Latest Build Done!"

dockerBuild:
	@echo "Version Build Started >>"
	docker build --tag $(CONTAINER_IMAGE):$(VERSION) .
	@echo "Build Done!"

dockerPush:
	@echo "Docker Image Push Started >>"
	docker push $(CONTAINER_IMAGE):latest
	docker push $(CONTAINER_IMAGE):$(VERSION)
	@echo "Docker push Done!"

build: dockerBuild
	$(MAKE) dockerBuildLatest
	$(MAKE) dockerPush
	@echo "Done!"

run:
	python3 app.py