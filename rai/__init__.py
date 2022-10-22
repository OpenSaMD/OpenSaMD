# RAi, machine learning solutions in radiotherapy
# Copyright (C) 2021-2022 Radiotherapy AI Holdings Pty Ltd

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# pylint: disable = useless-import-alias

from rai.contours.merge import (
    merge_contours_by_structure as merge_contours_by_structure,
)
from rai.data.download import deepmind_example as download_deepmind_example
from rai.data.download import hnscc_example as download_hnscc_example
from rai.data.download import lctsc_example as download_lctsc_example
from rai.data.images import paths_to_sorted_image_series as paths_to_sorted_image_series
from rai.data.images import (
    sorted_image_series_to_image_stack_hfs as sorted_image_series_to_image_stack_hfs,
)
from rai.dicom.rtstruct import create_dicom_structure_set as create_dicom_structure_set
from rai.dicom.structures import (
    dicom_to_contours_by_structure as dicom_to_contours_by_structure,
)
from rai.dicom.uid import (
    RAI_CONTOURS_IMPLEMENTATION_CLASS_UID,
    RAI_IMPLEMENTATION_VERSION_NAME,
)
from rai.display.animation import (
    auto_scroll_contours_by_orientation as auto_scroll_contours_by_orientation,
)
from rai.display.animation import (
    plot_contours_by_structure as plot_contours_by_structure,
)
from rai.display.animation import view_ranges_from_masks as view_ranges_from_masks
from rai.inference.main import inference as inference
from rai.mask.convert import (
    masks_to_contours_by_structure as masks_to_contours_by_structure,
)
from rai.metrics.dice import from_contours_by_slice as dice_from_contours_by_slice
from rai.model.load import load_models as load_models

from ._version import __version__ as __version__
from ._version import version_info as version_info
