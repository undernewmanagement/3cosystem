TAG := $(shell date +%Y%m%d%H%M)

############################################################################
# HELP / DEFAULT COMMAND
############################################################################
.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: build
build: ## build docker image for local and production
	docker build --build-arg TAG=$(TAG) -t 3cosystem:$(TAG) .
	docker tag 3cosystem:$(TAG) 3cosystem:latest

.PHONY: prod-deploy
prod-deploy: build ## deploy the docker image to production
	docker tag 3cosystem:$(TAG) rg.fr-par.scw.cloud/simplecto/3cosystem:$(TAG)
	docker push rg.fr-par.scw.cloud/simplecto/3cosystem:$(TAG)
	#docker save 3cosystem:$(TAG) | ssh prod.m3b 'docker load'
	ssh deploy@prod.m3b "cd /home/deploy/deployment/containers/3cosystem && make deploy RELEASE=$(TAG)"

.PHONY: prod-migrate
prod-migrate: ## run the django migrate command on production
	ssh deploy@prod.m3b "cd /home/deploy/deployment/containers/3cosystem && make migrate RELEASE=$(TAG)"

.PHONY: prod-start
prod-start: ## clean start the website container locally
	docker container stop 3cosystem || true
	docker container rm 3cosystem || true
	docker container run \
		--name 3cosystem \
		--hostname 3cosystem \
		--env-file env \
		3cosystem:latest

.PHONY: clean
clean: ## remove python cache files
	find src/ -type f -name *.pyc -delete
	find src/ -type d -name __pycache__ -delete

.PHONY: postgres-start
postgres-start: postgres-stop ## run postgres server via docker
	docker run \
		-d \
		-v $(PWD)/postgres-data:/var/lib/postgresql \
		-p 5433:5432 \
		--name postgis \
		mdillon/postgis

.PHONY: postgres-stop
postgres-stop: ## stop the postgres container
	docker container stop postgis || true
	docker container rm postgis || true

.PHONY: import-data
import-data: ## load the fixtures file for 3cosystem cities
	cd src && python manage.py loaddata data/geography
