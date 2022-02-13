SHELL := /bin/bash -o pipefail -e
.SUFFIXES:
.SECONDARY:
.DELETE_ON_ERROR:

release := ./docs/foo
src := ./src

CONFIG := $(src)/config.yml
DATA_FILES := $(wildcard $(src)/data/*.yml)
SRC_MDS := $(wildcard $(src)/documents/**/*.md $(src)/documents/*.md)
RELEASE_MDS := $(patsubst $(src)/documents/%.md,$(release)/%.md,$(SRC_MDS))
RELEASE_PDFS := $(patsubst $(src)/documents/%.md,$(release)/%.pdf,$(SRC_MDS))
RELEASE_DOCS := $(patsubst $(src)/documents/%.md,$(release)/%.docx,$(SRC_MDS))

all: $(RELEASE_MDS)

pdfs: $(RELEASE_PDFS)

docs: $(RELEASE_DOCS)

$(release)/%.md: $(src)/documents/%.md $(CONFIG) $(DATA_FILES)
	@mkdir -p $(@D)
	poetry run rdm render $< $(CONFIG) $(DATA_FILES) > $@

$(release)/%.pdf: $(release)/%.md $(src)/pandoc_pdf.yml $(src)/template.tex
	@mkdir -p $(@D)
	pandoc --defaults=$(src)/pandoc_pdf.yml $< -o $@

$(release)/%.docx: $(release)/%.md $(src)/pandoc_docx.yml
	@mkdir -p $(@D)
	pandoc --defaults=$(src)/pandoc_docx.yml $< -o $@

# useful for debugging
$(release)/%.tex: $(release)/%.md $(src)/pandoc_pdf.yml $(src)/template.tex
	@mkdir -p $(@D)
	pandoc --defaults=$(src)/pandoc_pdf.yml -t latex $< -o $@

# Manually call recipe to pull down your development history
$(src)/data/history.yml:
	poetry run rdm pull $< > $@

.PHONY:
clean:
	rm -rf tmp $(release)
