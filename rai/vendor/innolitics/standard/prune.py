# Copyright (C) 2022 Radiotherapy AI Holdings Pty Ltd

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import pathlib

from rai.dicom._inheritance import RTSTRUCT_DICOM_MODULES

from .load import get_standard

HERE = pathlib.Path(__file__).parent.resolve()


def prune_module_attributes():
    standard_to_prune = "module_to_attributes"

    module_to_attributes = get_standard(standard_to_prune)

    modules_to_keep = set(RTSTRUCT_DICOM_MODULES.keys())

    pruned_module_to_attributes = [
        item for item in module_to_attributes if item["moduleId"] in modules_to_keep
    ]

    with open(HERE / f"data/{standard_to_prune}.json", "w") as f:
        json.dump(pruned_module_to_attributes, f, indent=2)
