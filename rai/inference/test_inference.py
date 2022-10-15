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

import raicontours

import rai

TG263 = raicontours.TG263


def test_inference():
    """Testing inference over jittered grid"""
    cfg = raicontours.get_config()

    image_paths, structure_path = rai.download_deepmind_example()

    x_grid, y_grid, image_stack, image_uids = rai.paths_to_image_stack_hfs(image_paths)

    z = [35, 45, 55]
    y = [140, 155, 175, 195, 215, 230]
    x = [210, 230, 250, 270, 290, 310]

    model = rai.load_model(cfg=cfg)
    masks_pd = rai.inference_over_jittered_grid(
        cfg=cfg, model=model, image_stack=image_stack, grid=(z, y, x)
    )

    predicted_contours_by_structure = rai.masks_to_contours_by_structure(
        cfg=cfg, x_grid=x_grid, y_grid=y_grid, masks=masks_pd
    )

    structure_ds = pydicom.read_file(structure_path)

    align_map = {
        "Orbit-Lt": [TG263.Eye_L],
        "Orbit-Rt": [TG263.Eye_R],
        "Lacrimal-Lt": [TG263.Glnd_Lacrimal_L],
        "Lacrimal-Rt": [TG263.Glnd_Lacrimal_R],
        "Lens-Lt": [TG263.Lens_L],
        "Lens-Rt": [TG263.Lens_R],
        "Optic-Nerve-Lt": [TG263.OpticNrv_L],
        "Optic-Nerve-Rt": [TG263.OpticNrv_R],
        # If there was an "Eyes" structure, would do the following:
        # "Eyes": [TG263.Eye_L, TG263.Eye_R]
    }

    dicom_structure_names = list(align_map.keys())
    dicom_contours_by_structure = rai.dicom_to_contours_by_structure(
        ds=structure_ds, image_uids=image_uids, structure_names=dicom_structure_names
    )

    aligned_predicted_contours_by_structure = rai.merge_contours_by_structure(
        predicted_contours_by_structure, align_map
    )

    dice = {}
    for name in align_map:
        dice[name] = rai.dice_from_contours_by_slice(
            dicom_contours_by_structure[name],
            aligned_predicted_contours_by_structure[name],
        )

    assert dice["Orbit-Lt"] > 0.89
    assert dice["Orbit-Rt"] > 0.89

    assert dice["Lacrimal-Lt"] > 0.50
    assert dice["Lacrimal-Rt"] > 0.70

    assert dice["Lens-Lt"] > 0.50
    assert dice["Lens-Rt"] > 0.50

    assert dice["Optic-Nerve-Lt"] > 0.60
    assert dice["Optic-Nerve-Rt"] > 0.60
