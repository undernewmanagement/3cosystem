IMAGE_NAME := 3cosystem/website

SITE_VERSION := $(shell semver.sh bump patch)

DOCKER_RUN := docker run -it --rm -v $$PWD:/usr/src/app 3cosystem/website

DC := docker-compose -p 3cosystem 

.PHONY: boom
boom:
	echo $(SITE_VERSION)

.PHONY: build
build:
	docker build --build-arg SITE_VERSION=$(SITE_VERSION) -t $(IMAGE_NAME) .


.PHONY: run
run:
	$(DC) run --rm --no-deps website $(CMD)


.PHONY: start
start:
	$(DC) up -d


.PHONY: stop
stop:
	$(DC) down

.PHONY: logs
logs:
	$(DC) logs -f $(SERVICE)

.PHONY: test
test:
	$(DC) run --rm --no-deps website pytest


.PHONY: migrate
migrate:
	$(DC) ./manage.py makemigrations
	$(DC) ./manage.py migrate


.PHONY: cachetable
cachetable:
	$(DC) ./manage.py createcachetable


.PHONY: fixtures
fixtures:
	$(DC) ./manage.py loaddata 


.PHONY: clean
clean:
	rm *.pyc
	rm -rf __pycache__/


##### CI/CD Server commands

.PHONY: ci-build
ci-build: build


.PHONY: ci-test
ci-test: ci-build
	docker-compose -p 3cosystem_test -f docker-compose-test.yml run --rm website /app/manage.py test
	docker-compose -p 3cosystem_test -f docker-compose-test.yml down


.PHONY: ci-push
ci-push: ci-build
	$(eval IMAGE_ID := $(shell docker images -q $(IMAGE_NAME) | tail -n1))
	docker tag $(IMAGE_ID) $(IMAGE_NAME):latest
	docker tag $(IMAGE_ID) $(IMAGE_NAME):$(SITE_VERSION)

	docker login -u $(DOCKER_USER) -p $(DOCKER_PASS)
	docker push $(IMAGE_NAME)

	git tag $(SITE_VERSION)
	git push origin master --tags
