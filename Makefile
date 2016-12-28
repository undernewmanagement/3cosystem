include utils/*.mk

PROJECT_NAME=3cosystem
DC=docker-compose -p $(PROJECT_NAME)

##################### DOCKER COMPOSE ##############################
.PHONY: build
build:: ##@Docker Compose	Build the docker images
	$(DC) build

.PHONY: down
down:: ##@Docker Compose	Stop, delete, and remove docker images
	$(DC) down

.PHONY: up
up:: ##@Docker Compose	Create and start docker images
	$(DC) up -d

.PHONY: rebuild
rebuild:: ##@Docker Compose	Rebuild the docker images
	$(DC) down
	$(DC) up -d


.PHONY: start
start:: ##@Docker Compose	Start the docker images
	$(DC) start


.PHONY: stop
stop:: ##@Docker Compose	Stop the docker images
	$(DC) stop

.PHONY: logs
logs:: ##@Docker Compose	View logs from docker-compose
	$(DC) logs
#####################################################################


.PHONY: docker-build
docker-build:: ##@Docker	Build an image
	docker build -t 3cosystem .

.PHONY: docker-ship
docker-ship:: ##@Docker	Ship the image (build, ship)

.PHONY: docker-run
docker-run:: ##@Docker	Run a container (build, run attached)

.PHONY: docker-start
docker-start:: ##@Docker	Run a container (build, run detached)

.PHONY: docker-stop
docker-stop:: ##@Docker	Stop the running container

.PHONY: docker-clean
docker-clean:: ##@Docker	Remove the container

.PHONY: docker-release
docker-release:: ##@Docker	Build and Ship



.PHONY: migrations
migrations:: ##@Django	Run database migrations
	$(DC) run --rm django python /app/manage.py migrate


.PHONY: deploy-production
deploy-production:: ##@3cosystem	Deploy to production (probably dokku)
	# TODO: make sure all the code is commited to local
	# TODO: maybe make sure code is committed to origin
	git push dokku master

.PHONY: clean
clean:: ##@3cosystem	Clean up build artifacts (*.pyc, __pycache__, etc)
	find . -name "*.pyc" -exec rm {} \;


