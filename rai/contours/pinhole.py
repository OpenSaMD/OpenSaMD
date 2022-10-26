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


import itertools
from typing import List, Tuple

import networkx as nx
import numpy as np
import shapely.geometry
import shapely.ops

from rai.typing.contours import ContoursXY

DEFAULT_EPSILON = 0.00001


def merge_contours_with_pinhole(contours: ContoursXY, simplify_tolerance, epsilon=None):
    polygons = _contours_to_polygons(contours)
    groups = _get_groups(polygons)

    merged_polygons = []
    for outer_polygon_index, inner_polygon_indices in groups:
        merged = polygons[outer_polygon_index]
        for inner_index in inner_polygon_indices:
            inner_polygon = polygons[inner_index]
            merged = _merge_with_pinhole(merged, inner_polygon, epsilon=epsilon)

        merged = merged.simplify(simplify_tolerance)

        merged_polygons.append(merged)

    merged_contours: ContoursXY = [
        list(polygon.exterior.coords) for polygon in merged_polygons
    ]

    return merged_contours


def _contours_to_polygons(contours: ContoursXY) -> List[shapely.geometry.Polygon]:
    polygons = []
    for xy_coords in contours:
        polygons.append(shapely.geometry.Polygon(xy_coords))

    return polygons


def _get_groups(
    polygons: List[shapely.geometry.Polygon],
) -> List[Tuple[int, List[int]]]:
    digraph = _build_digraph(polygons)

    groups = []
    while list(digraph.nodes):
        node = next(iter(digraph.nodes))
        root = _get_root(digraph, node)

        successors = list(digraph.successors(root))

        groups.append((root, successors))
        digraph.remove_node(root)
        for successor in successors:
            digraph.remove_node(successor)

    return groups


def _merge_with_pinhole(
    outer: shapely.geometry.Polygon, inner: shapely.geometry.Polygon, epsilon=None
):
    point_outer, point_inner = shapely.ops.nearest_points(
        outer.exterior, inner.exterior
    )
    outer_start_index, outer_end_index, outer_polygon = _append_points(
        outer, point_outer, epsilon=epsilon
    )
    inner_start_index, inner_end_index, inner_polygon = _append_points(
        inner, point_inner, epsilon=epsilon
    )

    outer_coords = list(outer_polygon.exterior.coords)
    inner_coords = list(inner_polygon.exterior.coords)

    joined_coords = (
        outer_coords[0 : outer_start_index + 1]
        + inner_coords[inner_end_index:]
        + inner_coords[0 : inner_start_index + 1]
        + outer_coords[outer_end_index:]
    )

    joined_polygon = shapely.geometry.Polygon(joined_coords)

    return joined_polygon


def _append_points(
    polygon: shapely.geometry.Polygon,
    point: shapely.geometry.Point,
    epsilon=None,
):
    if epsilon is None:
        epsilon = DEFAULT_EPSILON

    lengths = [
        polygon.exterior.project(shapely.geometry.Point(coord))
        for coord in polygon.exterior.coords
    ]

    new_point_location = polygon.exterior.project(point)
    start_point = new_point_location - epsilon
    end_point = new_point_location + epsilon

    lengths += [start_point, end_point]
    lengths = sorted(np.unique(lengths))
    start_point_index = lengths.index(start_point)
    end_point_index = lengths.index(end_point)

    new_polygon = shapely.geometry.Polygon(
        [polygon.exterior.interpolate(length) for length in lengths]
    )

    return start_point_index, end_point_index, new_polygon


def _build_digraph(polygons: List[shapely.geometry.Polygon]) -> nx.DiGraph:
    polygon_dg = nx.DiGraph()

    for i in range(len(polygons)):
        polygon_dg.add_node(i)

    for node_a, node_b in itertools.combinations(polygon_dg.nodes, 2):
        p_a = polygons[node_a]
        p_b = polygons[node_b]

        if p_a.contains(p_b):
            polygon_dg.add_edge(node_a, node_b)
        elif p_b.contains(p_a):
            polygon_dg.add_edge(node_b, node_a)
        elif p_a.disjoint(p_b):
            continue
        else:
            raise ValueError(
                "All contours should either be disjoint, or be fully contained"
            )

    transitive_reduction = nx.transitive_reduction(polygon_dg)

    return transitive_reduction


def _get_root(graph: nx.DiGraph, node: int):
    predecessors = [node]

    while predecessors:
        node = predecessors[0]
        predecessors = list(graph.predecessors(node))

    return node
