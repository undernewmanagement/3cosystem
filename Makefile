include utils/common.mk

PROJECT_NAME=3cosystem
DC=docker-compose -p $(PROJECT_NAME)


.PHONY: build
build:: ##@3cosystem	Build the docker image
	$(DC) build


.PHONY: rebuild
rebuild:: ##@3cosystem	Rebuild the docker image
	$(DC) down
	$(DC) up


.PHONY: start
start:: ##@3cosystem	Start the docker image
	$(DC) start


.PHONY: stop
stop:: ##@3cosystem	Stop the docker image
	$(DC) stop


.PHONY: deploy-production
deploy-production:: ##@3cosystem	Deploy to production (probably dokku)
	# TODO: make sure all the code is commited to local
	# TODO: maybe make sure code is committed to origin
	git push dokku master

.PHONY: clean
clean:: ##@3cosystem	Clean up build artifacts (*.pyc, __pycache__, etc)
	find . -name "*.pyc" -exec rm {} \;
