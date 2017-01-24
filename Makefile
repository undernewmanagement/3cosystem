
DOCKER_RUN := docker run -it --rm -v $$PWD:/usr/src/app 3cosystem/website
DC := docker-compose run --rm website


.PHONY: check-env
check-env:

.PHONY: build
build:
	docker build -t 3cosystem/website .

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


#ship:

.PHONY: clean
clean:
	rm *.pyc
	rm -rf __pycache__/
