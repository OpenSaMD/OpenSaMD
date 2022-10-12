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


def merge_contours_by_structure(contours_by_structure, merge_map):
    number_of_slices_per_structure = list(
        {len(contours_by_slice) for contours_by_slice in contours_by_structure.values()}
    )
    assert len(number_of_slices_per_structure) == 1
    number_of_slices = number_of_slices_per_structure[0]

    new_contours_by_structure = {}
    for destination_name, original_names in merge_map.items():
        contours_by_slice = []
        for z_index in range(number_of_slices):
            contours_for_this_slice = []
            for name in original_names:
                contours_for_this_slice += contours_by_structure[name][z_index]

            contours_by_slice.append(contours_for_this_slice)

        new_contours_by_structure[destination_name] = contours_by_slice

    return new_contours_by_structure
