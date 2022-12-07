# Copyright 2017 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

# Adapted from https://github.com/pantsbuild/pants/blob/bca1b5a4ae311511fe87ff0dd3ccecc32955d024/src/python/pants/version.py#L1-L32

"""RAi version handling"""

from packaging.version import Version

from rai import _version

# Generate a inferrable dependency on the `rai._version` package and
# its associated resources.
from rai.vendor.pants.resources import read_resource

VERSION: str = read_resource(_version.__name__, "VERSION").decode().strip()

RAI_SEMVER = Version(VERSION)

# E.g. 2.0 or 2.2.
MAJOR_MINOR = f"{RAI_SEMVER.major}.{RAI_SEMVER.minor}"
