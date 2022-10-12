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

import itertools

import numpy as np
import pydicom
from raicontours import TG263, cfg

from rai.data import download as _data_download
from rai.data import images as _images_data
from rai.dicom import structures as _dicom_structures
from rai.mask import convert as _mask_convert
from rai.metrics import dice as _dice_metric

from . import main as _inference


def test_inference():
    image_paths, structure_path = _data_download.hnscc_example()

    x_grid, y_grid, image_stack, image_uids = _images_data.paths_to_image_stack_hfs(
        image_paths
    )
    structure_ds = pydicom.read_file(structure_path)

    name_to_number_map = {
        item.ROIName: item.ROINumber for item in structure_ds.StructureSetROISequence
    }

    name_map = {
        "Eyes": [TG263.Eye_L, TG263.Eye_R],
        "L Optic Nerve": [TG263.OpticNrv_L],
        "R Optic Nerve": [TG263.OpticNrv_R],
    }

    number_to_contour_sequence_map = {
        item.ReferencedROINumber: item.ContourSequence
        for item in structure_ds.ROIContourSequence
    }

    structure_name_to_contour_sequence_map = {
        structure_name: number_to_contour_sequence_map[
            name_to_number_map[structure_name]
        ]
        for structure_name in name_map
    }

    z = [35, 45, 55]
    y = [155, 175, 195, 215]
    x = [210, 230, 250, 270, 290, 310]

    points = []
    for point in itertools.product(z, y, x):
        point = np.random.randint(-1, 2, size=3) + point
        points.append(tuple(point.tolist()))

    masks_pd = _inference.run_inference(image_stack=image_stack, points=points)

    #

    contours_by_structure_pd = {}

    for structure_index, structure_name in enumerate(cfg["structures"]):
        this_structure_pd = masks_pd[..., structure_index]

        contours_by_slice_pd = []
        for z_index in range(image_stack.shape[0]):
            this_slice_pd = this_structure_pd[z_index, ...]
            contours_pd = _mask_convert.mask_to_contours(x_grid, y_grid, this_slice_pd)
            contours_by_slice_pd.append(contours_pd)

        contours_by_structure_pd[structure_name] = contours_by_slice_pd

    #

    contours_by_structure_gt = {}
    dice = {}

    for hnscc_name, tg263_names in name_map.items():
        contours_by_slice_gt = _dicom_structures.contour_sequence_to_contours_by_slice(
            image_uids,
            structure_name_to_contour_sequence_map[hnscc_name],
        )
        contours_by_structure_gt[hnscc_name] = contours_by_slice_gt

        contours_by_slice_pd = []
        for z_index, _ in enumerate(image_uids):

            contours_for_this_slice = []
            for tg263_name in tg263_names:
                contours_for_this_slice += contours_by_structure_pd[tg263_name][z_index]

            contours_by_slice_pd.append(contours_for_this_slice)

        dice[hnscc_name] = _dice_metric.from_contours_by_slice(
            contours_by_slice_gt, contours_by_slice_pd
        )

    assert dice["Eyes"] > 0.88

    # Reference contours here are not ideal
    assert dice["L Optic Nerve"] > 0.50
    assert dice["R Optic Nerve"] > 0.50

    #

    colours = {
        TG263.Eye_L: "C0",
        TG263.Eye_R: "C1",
        TG263.OpticNrv_L: "C2",
        TG263.OpticNrv_R: "C3",
        "Eyes": "C4",
        "L Optic Nerve": "C5",
        "R Optic Nerve": "C6",
    }

    labels = {
        TG263.Eye_L: "RAi Eye_L",
        TG263.Eye_R: "RAi Eye_R",
        TG263.OpticNrv_L: "RAi OpticNrv_L",
        TG263.OpticNrv_R: "RAi OpticNrv_R",
        "Eyes": "HNSCC Eyes",
        "L Optic Nerve": "HNSCC OpticNrv_L",
        "R Optic Nerve": "HNSCC OpticNrv_R",
    }


def _plot_model_result(image_stack, contours_by_structure, colours, labels):
    vmin = 0.2
    vmax = 0.4

    ylim = [-np.inf, np.inf]
    xlim = [np.inf, -np.inf]

    axs = []

    for z_index in range(image_stack.shape[0]):
        has_a_contour = False

        for structure_name, contours_by_slice in contours_by_structure.items():
            contours = contours_by_slice[z_index]
            if len(contours) > 0:
                has_a_contour = True
                break

        if not has_a_contour:
            continue

        fig, ax = plt.subplots()
        axs.append(ax)

        ax.pcolormesh(
            x_grid,
            y_grid,
            image_stack[z_index, :, :],
            vmin=vmin,
            vmax=vmax,
            shading="nearest",
            cmap="gray",
        )

        for structure_name, contours_by_slice in contours_by_structure.items():
            contours = contours_by_slice[z_index]

            for contour in contours:
                contour_array = np.array(contour + [contour[0]])

                ax.plot(
                    contour_array[:, 0],
                    contour_array[:, 1],
                    label=labels[structure_name],
                    c=colours[structure_name],
                )

                xlim[1] = np.max([np.max(contour_array[:, 0]), xlim[1]])
                xlim[0] = np.min([np.min(contour_array[:, 0]), xlim[0]])
                ylim[0] = np.max([np.max(contour_array[:, 1]), ylim[0]])
                ylim[1] = np.min([np.min(contour_array[:, 1]), ylim[1]])

        ax.set_aspect("equal", "box")

        plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
        plt.title(f"Slice: {z_index}")

    x_range = xlim[1] - xlim[0]
    y_range = ylim[0] - ylim[1]

    margin = 0.2

    xlim[0] -= x_range * margin
    xlim[1] += x_range * margin

    ylim[1] -= y_range * margin
    ylim[0] += y_range * margin

    for ax in axs:
        ax.set_ylim(ylim)
        ax.set_xlim(xlim)
