PROJECT = $(shell basename $(shell pwd))
ID = pikesley/${PROJECT}

build:
	docker build \
		--tag ${ID} .

run:
	docker run \
		--name ${PROJECT} \
		--hostname ${PROJECT} \
		--volume $(shell pwd):/opt/${PROJECT} \
		--interactive \
		--tty \
		--rm \
		${ID} \
		bash

exec:
	docker exec \
		--interactive \
		--tty \
		${PROJECT} \
		bash

###

all: format test clean

black:
	python -m black .

isort:
	python -m isort .

format: black isort

test:
	PYTHONDONTWRITEBYTECODE=1 \
	python -m pytest \
		--random-order \
		--verbose \
		--capture no \
		--failed-first \
		--cov \
		--exitfirst

clean:
	rm -fr .pytest_cache

###

extract:
	cat tweets.js | sed "s:window.YTD.tweets.part0 = ::" |  jq '.[] | .tweet.full_text' > raw-tweets.txt

sanitise:
	python sanitiser.py

toot: # we redirect stderr because there's a deprecation warning I don't care about
	python toot.py 2> /dev/null
