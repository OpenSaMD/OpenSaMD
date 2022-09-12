poetry run jupyter-book toc from-project docs > docs/_toc.yml
poetry run jupyter-book clean docs
poetry run jupyter-book build docs
