import pathlib

import yaml

import jupyter_book.cli.main
from sphinx_external_toc.parsing import FILE_FORMATS, create_toc_dict
from sphinx_external_toc.tools import create_site_map_from_path

# TODO: Get repo path from pants pex
REPO_ROOT = pathlib.Path.home() / "git" / "OpenSaMD"
DOCS_DIR = REPO_ROOT / "docs"


def main():
    site_map = create_site_map_from_path(DOCS_DIR)
    data = create_toc_dict(site_map)

    with open(DOCS_DIR / "_toc.yml", "w") as f:
        f.write(yaml.dump(data, sort_keys=False, default_flow_style=False))


if __name__ == "__main__":
    main()
