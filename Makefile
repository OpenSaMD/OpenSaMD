SHELL := /bin/bash -o pipefail -e
.SUFFIXES:
.SECONDARY:
.DELETE_ON_ERROR:

release := ./docs
src := ./src

CONFIG := $(src)/config.yml
DATA_FILES := $(wildcard $(src)/data/*.yml)

SRC_MDS := $(wildcard $(src)/documents/*/*/*.md $(src)/documents/**/*.md $(src)/documents/*.md)
RELEASE_MDS := $(patsubst $(src)/documents/%.md,$(release)/%.md,$(SRC_MDS))

SRC_PNGS := $(wildcard $(src)/documents/**/*.png $(src)/documents/*.png)
RELEASE_PNGS := $(patsubst $(src)/documents/%.png,$(release)/%.png,$(SRC_PNGS))

all: $(RELEASE_PNGS) $(RELEASE_MDS)

$(release)/%.md: $(src)/documents/%.md $(CONFIG) $(DATA_FILES)
	@mkdir -p $(@D)
	poetry run rdm render $< $(CONFIG) $(DATA_FILES) > $@

$(release)/%.png: $(src)/documents/%.png
	@mkdir -p $(@D)
	cp $< $@

# Manually call recipe to pull down your development history
$(src)/data/history.yml:
	poetry run rdm pull $< > $@

.PHONY:
clean:
	rm -f $(release)/**/*.md $(release)/*.md
	rm -rf $(release)/_build
