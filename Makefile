.PHONY: poetry-install

APPS := discord

DISCORD_DIR := ./discord
DEV_DEPS := test,dev,docs,sandbox

dev_requirements := $(shell )
build: 
	docker-compose build 

poetry-install:
	poetry install

poetry-export-dev: poetry-install
	echo `poetry export --without-hashes --without app-openai --format=requirements.txt >  $(DISCORD_DIR)/dev.requirements.txt`

poetry-export-prod: poetry-install
	echo `poetry export --without-hashes --without app-openai,$(DEV_DEPS) --format=requirements.txt > $(DISCORD_DIR)/prod.requirements.txt`
