TAG := $(shell date +%Y%m%d%H%M)

.PHONY: help
help:
	cat Makefile

.PHONY: build
build:
	docker build --build-arg TAG=$(TAG) -t 3cosystem:$(TAG) .
	docker tag 3cosystem:$(TAG) 3cosystem:latest

.PHONY: prod-deploy
prod-deploy: build
	docker tag 3cosystem:$(TAG) rg.fr-par.scw.cloud/simplecto/3cosystem:$(TAG)
	docker push rg.fr-par.scw.cloud/simplecto/3cosystem:$(TAG)
	#docker save 3cosystem:$(TAG) | ssh prod.m3b 'docker load'
	ssh deploy@prod.m3b "cd /home/deploy/deployment/containers/3cosystem && make deploy RELEASE=$(TAG)"

.PHONY: prod-migrate
prod-migrate:
	ssh deploy@prod.m3b "cd /home/deploy/deployment/containers/3cosystem && make migrate RELEASE=$(TAG)"

.PHONY: prod-start
prod-start:
	docker container stop 3cosystem || true
	docker container rm 3cosystem || true
	docker container run \
		--name 3cosystem \
		--hostname 3cosystem \
		--env-file env \
		3cosystem:latest

.PHONY: clean
clean:
	find src/ -type f -name *.pyc -delete
	find src/ -type d -name __pycache__ -delete

.PHONY: postgres-start
postgres-start: postgres-stop
	docker run \
		-d \
		-v $(PWD)/postgres-data:/var/lib/postgresql \
		-p 5433:5432 \
		--name postgis \
		mdillon/postgis

.PHONY: postgres-stop
postgres-stop:
	docker container stop postgis || true
	docker container rm postgis || true

.PHONY: import-data
import-data:
	cd src && python manage.py loaddata data/geography