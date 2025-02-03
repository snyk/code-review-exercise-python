############################### CONFIG ##############################
SHELL := /bin/bash
RUN_NPM_DEPS=
NPM_DEPS_PORT=3000

DOCKER=docker
DOCKER_IMAGE_NAME=npm-deps

RUN_PY=poetry run
PLATFORM=$(shell test $$(uname) == "Darwin" && echo "macos" || echo "linux")
OPEN=$(shell test $(PLATFORM) == "linux" && echo "xdg-open" || echo "open")


docker-only:
ifeq ($(USE_DOCKER), false)
	$(error this command only works without USE_DOCKER=false)
endif

local-only:
ifneq ($(USE_DOCKER), false)
	$(error this command only works with USE_DOCKER=false)
endif


DOCKER_RUN = $(DOCKER) run --rm -it $(DOCKER_IMAGE_NAME)
DOCKER_RUN_USER = $(DOCKER_RUN)
ifeq ($(PLATFORM), linux)
	# The --user flag is used here when our container will be writing to the host file system.
	# We want the file to be created under the owner of the current user (not the default root).
	# This particularly important on setups where docker runs natively (e.g. Linux)
	USER="$(shell id -u):$(shell id -g)"
	DOCKER_RUN_USER = $(DOCKER_RUN) --user $(USER)
endif


ifneq ($(USE_DOCKER), false)
	RUN_NPM_DEPS=$(DOCKER_RUN)
	RUN_NPM_DEPS_WITH_SERVICE_PORTS=$(DOCKER) run --rm -it -p ${NPM_DEPS_PORT}:${NPM_DEPS_PORT} $(DOCKER_IMAGE_NAME)
	RUN_NPM_DEPS_USER=$(DOCKER_RUN_USER) npm_deps
	RUN_NPM_DEPS_NO_DEPS=$(DOCKER_RUN) --no-deps npm_deps
	LOCALHOST=0.0.0.0
endif

RUN_NPM_DEPS=$(DOCKER_RUN) npm_deps
RUN_NPM_DEPS_USER=$(DOCKER_RUN_USER)
RUN_NPM_DEPS_NO_DEPS=$(DOCKER_RUN) --no-deps npm_deps

.SILENT: help
help: ## Shows all available commands
	set -x
	echo "Usage: make [target] ..."
	echo ""
	echo "Available targets:"
	grep ':.* ##\ ' ${MAKEFILE_LIST} | awk '{gsub(":[^#]*##","\t"); print}' | column -t -c 2 -s $$'\t' | sort


############################### BUILD ###############################
setup: docker-only clean build

clean: docker-only # Stop all containers
	${DOCKER} image rm ${DOCKER_IMAGE_NAME}

build:
	${DOCKER} build -t ${DOCKER_IMAGE_NAME} $(ARGS) .

build-dev:
	${DOCKER} build -t ${DOCKER_IMAGE_NAME} --build-arg MODE=development .

################################ RUN ################################

bash: ## Open a bash shell
	$(RUN_NPM_DEPS_USER) bash

test: build-dev ## Run tests
	$(RUN_NPM_DEPS_USER) $(RUN_PY) pytest

runserver: ## Run npm-deps backend using uvicorn
	$(RUN_NPM_DEPS_WITH_SERVICE_PORTS) $(RUN_PY) uvicorn app:app --host="0.0.0.0" --port="${NPM_DEPS_PORT}" --log-level="info"


########################## LINT AND FORMAT ##########################

pre-commit: ## Setup pre-commit linters
	poetry run pre-commit install --install-hooks
	poetry run pre-commit install --hook-type commit-msg

lint: ## Lint changes
	poetry run pre-commit run

lint-all: ## Lint all codebase
	poetry run pre-commit run -a
