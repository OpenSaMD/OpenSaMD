# Copyright (C) 2022 Radiotherapy AI Holdings Pty Ltd

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


import pydicom

from raicontours import TG263, cfg

import rai


def test_inference():
    image_paths, structure_path = rai.download_deepmind_example()

    x_grid, y_grid, image_stack, image_uids = rai.paths_to_image_stack_hfs(image_paths)

    z = [35, 45, 55]
    y = [140, 155, 175, 195, 215, 230]
    x = [210, 230, 250, 270, 290, 310]

    model = rai.load_model(cfg=cfg)
    masks_pd = rai.inference_over_jittered_grid(
        model=model, image_stack=image_stack, grid=(z, y, x)
    )

    pd_contours_by_structure_tg263 = rai.masks_to_contours_by_structure(
        x_grid, y_grid, masks_pd
    )

    structure_ds = pydicom.read_file(structure_path)

    merge_map = {
        "Orbit-Lt": [TG263.Eye_L],
        "Orbit-Rt": [TG263.Eye_R],
        "Lacrimal-Lt": [TG263.Glnd_Lacrimal_L],
        "Lacrimal-Rt": [TG263.Glnd_Lacrimal_R],
        "Lens-Lt": [TG263.Lens_L],
        "Lens-Rt": [TG263.Lens_R],
        "Optic-Nerve-Lt": [TG263.OpticNrv_L],
        "Optic-Nerve-Rt": [TG263.OpticNrv_R],
    }

    gt_contours_by_structure_dicom_names = rai.dicom_to_contours_by_structure(
        ds=structure_ds, image_uids=image_uids, structure_names=merge_map.keys()
    )

    pd_contours_by_structure_dicom_names = rai.merge_contours_by_structure(
        pd_contours_by_structure_tg263, merge_map
    )

    dice = {}
    for name in merge_map:
        dice[name] = rai.dice_from_contours_by_slice(
            gt_contours_by_structure_dicom_names[name],
            pd_contours_by_structure_dicom_names[name],
        )

    assert dice["Orbit-Lt"] > 0.89
    assert dice["Orbit-Rt"] > 0.89

    assert dice["Lacrimal-Lt"] > 0.50
    assert dice["Lacrimal-Rt"] > 0.70

    assert dice["Lens-Lt"] > 0.50
    assert dice["Lens-Rt"] > 0.50

    assert dice["Optic-Nerve-Lt"] > 0.60
    assert dice["Optic-Nerve-Rt"] > 0.60
