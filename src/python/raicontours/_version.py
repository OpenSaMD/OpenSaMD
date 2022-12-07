"""Package version information"""

version_info = [0, 3, 0, "dev7"]


def _get__version__():
    major_minor_patch_as_string = ".".join(version_info[0:3])

    try:
        dev = f"-{version_info[3]}"
    except IndexError:
        dev = ""

    return major_minor_patch_as_string + dev


__version__ = _get__version__()
