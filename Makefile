IMAGE_NAME := 3cosystem/website

SITE_VERSION := $(shell semver.sh bump patch)

DOCKER_RUN := docker run -it --rm -v $$PWD:/usr/src/app --env-file=env 3cosystem/website


.PHONY: build
build:
	docker build --build-arg SITE_VERSION=$(SITE_VERSION) -t $(IMAGE_NAME) .


.PHONY: run
run:
	$(DOCKER_RUN) $(CMD)

.PHONY: test
test:
	$(DOCKER_RUN) /app/manage.py test


.PHONY: migrate
migrate:
	$(DOCKER_RUN) ./manage.py makemigrations
	$(DOCKER_RUN) ./manage.py migrate


.PHONY: cachetable
cachetable:
	$(DOCKER_RUN) ./manage.py createcachetable


# TODO: I don't know if this target works.
#.PHONY: fixtures
#fixtures:
#	$(DOCKER_RUN) ./manage.py loaddata 


.PHONY: clean
clean:
	find src/ -type f -name *.pyc -delete
	find src/ -type d -name __pycache__ -delete


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
	git push github $(SITE_VERSION)
