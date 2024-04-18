APPLICATION_NAME ?= dummyapp
VERSION ?= v1
REGISTRY ?= docker.io
USERN ?= fahadahammed
CONTAINER_IMAGE = $(REGISTRY)/$(USERN)/$(APPLICATION_NAME)

test:
	@python3 -m unittest -v tests/*.py -v

dockerBuildLatest:
	@echo "Latest Build Started >>"
	docker build --tag $(CONTAINER_IMAGE):latest .
	@echo "Latest Build Done!"

dockerBuildVersion:
	@echo "Version Build Started >>"
	docker build --tag $(CONTAINER_IMAGE):$(VERSION) .
	@echo "Build Done!"

dockerBuild:
	@echo "Build Started >>"
	$(MAKE) dockerBuildVersion
	$(MAKE) dockerBuildLatest
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
	@python3 app.py

lintCheck:
	@( \
    	pip install pylint; \
		pylint app.py tests/*.py --fail-under 8 --fail-on E; \
	)

securityCheck:
	@( \
		pip3 install bandit; \
		bandit -r app.py tests/*.py -f json | jq '.metrics._totals'; \
		bandit -r app.py tests/*.py -f json | jq -e '.metrics._totals."SEVERITY.HIGH" == 0'; \
	)


check:
	$(MAKE) lintCheck
	$(MAKE) securityCheck

check_and_test:
	$(MAKE) check
	$(MAKE) test