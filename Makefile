PROJECT = $(shell basename $(shell pwd))
ID = pikesley/${PROJECT}

all: format lint test clean  ## format, lint, test, clean (default)

black:
	python -m black .

isort:
	python -m isort .

format: black isort  ## run the formatters

lint:  ## run the linters
	python -m pylama

test:  ## run the tests
	PYTHONDONTWRITEBYTECODE=1 \
	python -m pytest \
		--random-order \
		--verbose \
		--capture no \
		--failed-first \
		--cov \
		--exitfirst

clean:  ## clean up artefacts
	@rm -fr .pytest_cache
	@rm -fr __pycache__

install:  ## install dependencies
	python -m pip install -r requirements.txt

###

extract:  ## extract the tweets from the archive
	cat tweets.js | sed "s:window.YTD.tweets.part0 = ::" |  jq '.[] | .tweet.full_text' > raw-tweets.txt

sanitise:  ## sanitise the tweets
	python sanitiser.py

toot:  ## send a toot
	python toot.py

###

build:  ## build the container (laptop only)
	docker build \
		--tag ${ID} .

run:  ## run the container (laptop only)
	docker run \
		--name ${PROJECT} \
		--hostname ${PROJECT} \
		--volume $(shell pwd):/opt/${PROJECT} \
		--interactive \
		--tty \
		--rm \
		${ID} \
		bash

###

# absolute voodoo from @rgarner
help:  ## show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' ${MAKEFILE_LIST} | sed "s/.*:\(.*:.*\)/\1/" | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
