SHELL := /bin/bash -o pipefail -e
.SUFFIXES:
.SECONDARY:
.DELETE_ON_ERROR:

release := ./docs
src := ./src

CONFIG := $(src)/config.yml
DATA_FILES := $(wildcard $(src)/data/*.yml)

SRC_MDS := $(shell find $(src)/documents/ -type f -name '*.md')
SRC_PNGS := $(shell find $(src)/documents/ -type f -name '*.png')
SRC_JPGS := $(shell find $(src)/documents/ -type f -name '*.jpg')

RELEASE_MDS := $(patsubst $(src)/documents/%.md,$(release)/%.md,$(SRC_MDS))
RELEASE_PNGS := $(patsubst $(src)/documents/%.png,$(release)/%.png,$(SRC_PNGS))
RELEASE_JPGS := $(patsubst $(src)/documents/%.jpg,$(release)/%.jpg,$(SRC_JPGS))
RELEASE_JB_FILES = $(release)/_config.yml $(release)/_toc.yml $(release)/references.bib

RELEASE_ALL := $(RELEASE_PNGS) $(RELEASE_JPGS) $(RELEASE_MDS) $(RELEASE_JB_FILES)

all: $(RELEASE_ALL)

$(release)/%.md: $(src)/documents/%.md $(CONFIG) $(DATA_FILES)
	@mkdir -p $(@D)
	poetry run rdm render $< $(CONFIG) $(DATA_FILES) > $@

$(release)/%.png: $(src)/documents/%.png
	@mkdir -p $(@D)
	cp $< $@

$(release)/%.jpg: $(src)/documents/%.jpg
	@mkdir -p $(@D)
	cp $< $@

$(release)/%.yml: $(src)/jupyter-book/%.yml
	cp $< $@

$(release)/%.bib: $(src)/jupyter-book/%.bib
	cp $< $@

# Manually call recipe to pull down your development history
$(src)/data/history.yml:
	poetry run rdm pull $< > $@

.PHONY:
clean:
	rm -rf $(release)
