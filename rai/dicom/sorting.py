# Copyright (C) 2022 Radiotherapy AI Holdings Pty Ltd
# Copyright (C) 2017-2021 Innolitics, LLC.

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


import numpy as np
import pydicom


# Adapted from
# https://github.com/innolitics/dicom-numpy/blob/7a2a63e331b263587d09405d34e937542803bbcb/dicom_numpy/combine_slices.py#L240-L243
def slice_position(slice_dataset: pydicom.Dataset):
    image_orientation = slice_dataset.ImageOrientationPatient
    _row_cosine, _column_cosine, slice_cosine = _extract_cosines(image_orientation)

    return float(np.dot(slice_cosine, slice_dataset.ImagePositionPatient))


# Adapted from
# https://github.com/innolitics/dicom-numpy/blob/7a2a63e331b263587d09405d34e937542803bbcb/dicom_numpy/combine_slices.py#L214-L218
def _extract_cosines(image_orientation):
    row_cosine = np.array(image_orientation[:3])
    column_cosine = np.array(image_orientation[3:])
    slice_cosine = np.cross(row_cosine, column_cosine)

    return row_cosine, column_cosine, slice_cosine
