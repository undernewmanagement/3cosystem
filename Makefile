
DOCKER_RUN := docker run -it --rm -v $$PWD:/usr/src/app 3cosystem/website
DC := docker-compose run --rm website
SITE_VERSION := 1.0.0

.PHONY: check-env
check-env:

.PHONY: build
build:
	docker build --build-arg SITE_VERSION=$(SITE_VERSION) -t 3cosystem/website:$(SITE_VERSION) .

.PHONY: run
run:
	$(DC)

.PHONY: test
test:
	$(DC) pytest

.PHONY: migrate
migrate:
	$(DC) ./manage.py makemigrations
	$(DC) ./manage.py migrate

.PHONY: fixtures
fixtures:


#.PHONY: ship
#ship:
#	docker

.PHONY: clean
clean:
	rm *.pyc
	rm -rf __pycache__/
