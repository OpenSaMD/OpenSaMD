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


import copy
import datetime
import functools
import itertools
import logging
from typing import Dict, List, Tuple

import matplotlib
import matplotlib.cm
import numpy as np
import pydicom
import pydicom.dataset
import pydicom.uid

import raicontours
from raicontours import TG263, Config

import rai
from rai.contours.convert import contour_to_dicom_format
from rai.typing.contours import ContoursByStructure
from rai.vendor.fma.codes import DEFAULT_FMA_CODES, FMA_NAMES

from . import _codes, _inheritance, append
from . import uid as _uid
from .anonymise import _tags, _typing
from .anonymise import encrypt as _encrypt

TypedDataset = _typing.TypedDataset

AttributeType = _inheritance.AttributeType
RTSTRUCT_DICOM_MODULES = _inheritance.RTSTRUCT_DICOM_MODULES
Usage = _inheritance.Usage
Inheritance = _inheritance.Inheritance
ModuleOptions = _inheritance.ModuleOptions


def create_dicom_structure_set(
    cfg: Config,
    image_series_headers: List[pydicom.Dataset],
    contours_by_structure: ContoursByStructure,
):

    structure_names = cfg["structures"]
    structure_codes = [DEFAULT_FMA_CODES[item] for item in structure_names]
    roi_description = "{structure_name}"
    structure_set_description = (
        f"Created using rai v{rai.__version__} "
        f"and raicontours v{raicontours.__version__}"
    )
    structure_set_label = "RAi"

    colour = get_colours()
    structure_colours = []
    for _ in structure_names:
        structure_colours.append(next(colour))

    _tags.add_tags_to_pydicom()

    for item in image_series_headers:
        if not np.allclose(np.abs(item.ImageOrientationPatient), [1, 0, 0, 0, 1, 0]):
            raise ValueError("Image Orientation must be one of HFS, HFP, FFS, or FFP.")

    study_header_reference = _get_study_header_reference(image_series_headers)
    ds = _create_base(
        study_header_reference,
        structure_set_label,
        structure_set_description=structure_set_description,
    )
    ds = append.append_dict_to_dataset(
        to_append={
            "ReferencedStudySequence": [_get_referenced_study(study_header_reference)],
        },
        ds=ds,
    )
    _add_frame_of_reference(
        ds=ds,
        study_header_reference=study_header_reference,
        image_series_headers=image_series_headers,
    )
    _codes.add_coding_context_and_mapping_header_items(ds=ds)
    name_to_number_map = _add_roi_sequence(
        ds=ds,
        study_header_reference=study_header_reference,
        structure_names=structure_names,
        structure_codes=structure_codes,
        roi_description=roi_description,
    )

    name_to_colour_map = dict(zip(structure_names, structure_colours))
    _add_contour_sequence(
        ds=ds,
        image_series_headers=image_series_headers,
        name_to_number_map=name_to_number_map,
        name_to_colour_map=name_to_colour_map,
        contours_by_structure=contours_by_structure,
    )

    return ds


def get_colours():
    cmaps_to_pull_from = ["tab10", "Set3", "Set1", "Set2"]
    loaded_colours = []
    for cmap in cmaps_to_pull_from:
        loaded_colours += matplotlib.cm.get_cmap(cmap).colors

    colours = np.round(np.array(loaded_colours) * 255).astype(int)

    greys_ref = np.logical_and(
        np.abs(colours[:, 0] - colours[:, 1]) < 40,
        np.abs(colours[:, 0] - colours[:, 2]) < 40,
        np.abs(colours[:, 1] - colours[:, 2]) < 40,
    )
    colours: np.ndarray = colours[np.invert(greys_ref)]
    colours: list[tuple[int, int, int]] = [tuple(item) for item in colours]

    return itertools.cycle(colours)


def _add_contour_sequence(
    ds,
    image_series_headers: List[pydicom.Dataset],
    name_to_number_map: Dict[TG263, str],
    name_to_colour_map: Dict[str, Tuple[int, int, int]],
    # contours_per_slice: list[Dict[str, list[np.ndarray]]],
    contours_by_structure: ContoursByStructure,
):
    roi_contour_sequence = []

    for structure_name, roi_number in name_to_number_map.items():
        contour_sequence = []

        contours_by_slice = contours_by_structure[structure_name]

        for contours, image_header in zip(contours_by_slice, image_series_headers):
            if len(contours) == 0:
                continue

            z_position = image_header.ImagePositionPatient[-1]

            for contour in contours:
                contour_in_dcm_format = contour_to_dicom_format(contour, z_position)
                contour_data = np.round(contour_in_dcm_format, decimals=6)
                num_contours = len(contour_data) // 3
                assert num_contours * 3 == len(contour_data)

                contour = {
                    "ContourImageSequence": [
                        {
                            "ReferencedSOPClassUID": image_header.SOPClassUID,
                            "ReferencedSOPInstanceUID": image_header.SOPInstanceUID,
                        }
                    ],
                    "ContourGeometricType": "CLOSED_PLANAR",
                    "NumberOfContourPoints": num_contours,
                    "ContourData": contour_data,
                }

                contour_sequence.append(contour)

        roi_contour = {
            "ROIDisplayColor": list(name_to_colour_map[structure_name]),
            "ReferencedROINumber": roi_number,
            "ContourSequence": contour_sequence,
        }

        roi_contour_sequence.append(roi_contour)

    ds = append.append_dict_to_dataset(
        to_append={
            "ROIContourSequence": roi_contour_sequence,
        },
        ds=ds,
    )


def _add_roi_sequence(
    ds,
    study_header_reference,
    structure_names: List[TG263],
    structure_codes: List[int],
    roi_description: str,
):
    frame_of_reference_uid = study_header_reference.FrameOfReferenceUID

    roi_sequence = []
    roi_observation_sequence = []
    name_to_number_map: Dict[TG263, str] = {}
    for i, (structure_name, structure_code) in enumerate(
        zip(structure_names, structure_codes)
    ):
        roi_number = str(i + 1)

        name_to_number_map[structure_name] = roi_number

        roi_sequence.append(
            {
                "ROINumber": roi_number,
                "ReferencedFrameOfReferenceUID": frame_of_reference_uid,
                "ROIName": structure_name.value,
                "ROIDescription": roi_description.format(
                    structure_name=structure_name.value
                ),
                "ROIGenerationAlgorithm": "AUTOMATIC",
            }
        )

        observation_sequence_item = {
            "ObservationNumber": roi_number,
            "ReferencedROINumber": roi_number,
            "RTROIInterpretedType": "ORGAN",
            "ROIObservationLabel": structure_name.value,
            "ROIInterpreter": "",
        }

        if structure_code is not None:
            observation_sequence_item["RTROIIdentificationCodeSequence"] = [
                {
                    "CodeValue": str(structure_code),
                    "CodingSchemeDesignator": "FMA",
                    "CodingSchemeVersion": "3.2",
                    "CodeMeaning": FMA_NAMES[structure_code],
                    "MappingResource": "99VMS",
                    "ContextGroupVersion": "20161209",
                    "ContextIdentifier": "VMS011",
                    "ContextUID": "1.2.246.352.7.2.11",
                    "MappingResourceUID": "1.2.246.352.7.1.1",
                    "MappingResourceName": "Varian Medical Systems",
                }
            ]

        roi_observation_sequence.append(observation_sequence_item)

    ds = append.append_dict_to_dataset(
        to_append={
            "StructureSetROISequence": roi_sequence,
            "RTROIObservationsSequence": roi_observation_sequence,
        },
        ds=ds,
    )

    return name_to_number_map


def _get_referenced_study(study_header_reference):
    return {
        "ReferencedSOPClassUID": "1.2.840.10008.3.1.2.3.2",
        "ReferencedSOPInstanceUID": study_header_reference.StudyInstanceUID,
    }


def _add_frame_of_reference(
    ds: pydicom.Dataset,
    study_header_reference: pydicom.Dataset,
    image_series_headers: List[pydicom.Dataset],
):
    frame_of_reference_uid = study_header_reference.FrameOfReferenceUID
    referenced_series_instance_uid = _get_series_uid(image_series_headers)

    contour_image_sequence = [
        {
            "ReferencedSOPClassUID": image_header.SOPClassUID,
            "ReferencedSOPInstanceUID": image_header.SOPInstanceUID,
        }
        for image_header in image_series_headers
    ]

    ds = append.append_dict_to_dataset(
        to_append={
            "ReferencedFrameOfReferenceSequence": [
                {
                    "FrameOfReferenceUID": frame_of_reference_uid,
                    "RTReferencedStudySequence": [
                        {
                            **_get_referenced_study(study_header_reference),
                            "RTReferencedSeriesSequence": [
                                {
                                    "SeriesInstanceUID": referenced_series_instance_uid,
                                    "ContourImageSequence": contour_image_sequence,
                                }
                            ],
                        }
                    ],
                }
            ],
        },
        ds=ds,
    )


def _get_series_uid(image_series_headers: List[pydicom.Dataset]):
    series_instance_uid = image_series_headers[0].SeriesInstanceUID
    if len(image_series_headers) == 1:
        return series_instance_uid

    for ds in image_series_headers[1::]:
        if ds.SeriesInstanceUID != series_instance_uid:
            raise ValueError(
                "Series Instance UID does not agree across provided images"
            )

    return series_instance_uid


def _get_study_header_reference(
    image_series_headers: List[pydicom.Dataset],
) -> pydicom.Dataset:
    datasets: List[pydicom.Dataset] = []

    for reference_header in image_series_headers:
        ds = pydicom.Dataset()
        _pull_from_reference(reference_header, ds)
        datasets.append(ds)

    study_header_reference = datasets[0]

    for ds in datasets[1::]:
        if ds != study_header_reference:
            raise ValueError("Provided Datasets don't agree")

    encrypted_tags_datasets: List[TypedDataset] = []

    for reference_header in image_series_headers:
        ds = copy.deepcopy(study_header_reference)
        _pull_encrypted_tags_from_reference(reference_header, ds)
        encrypted_tags_datasets.append(ds)

    study_header_reference = encrypted_tags_datasets[0]

    # Can't test that the encrypted datasets agree as every encryption
    # result ends up being different. Instead, verify that the HMAC
    # search terms all agree.
    for ds in encrypted_tags_datasets[1::]:
        try:
            test_sequence = ds[_tags.STORAGE_SEQUENCE_TAG].value
            reference_sequence = study_header_reference[
                _tags.STORAGE_SEQUENCE_TAG
            ].value
        except KeyError:
            continue

        for test, reference in zip(test_sequence, reference_sequence):
            try:
                test_search_terms = test[_tags.SEARCH_INDEX_SEQUENCE_TAG]
                reference_search_terms = reference[_tags.SEARCH_INDEX_SEQUENCE_TAG]
            except KeyError:
                continue

            if test_search_terms != reference_search_terms:
                for test_search_term, reference_search_term in zip(
                    test_search_terms, reference_search_terms
                ):
                    logging.info(
                        f"{test_search_term} should equal {reference_search_term}"
                    )

                raise ValueError("Search terms within provided datasets don't agree")

    return study_header_reference


def _create_base(
    study_header_reference, structure_set_label, structure_set_description
):
    ds = create_bare_bones_ds(_uid.RT_STRUCTURE_SET_STORAGE_UID)
    date = ds.InstanceCreationDate
    time = ds.InstanceCreationTime

    assert ds.SOPClassUID == ds.file_meta.MediaStorageSOPClassUID
    assert ds.SOPInstanceUID == ds.file_meta.MediaStorageSOPInstanceUID
    assert ds.file_meta.TransferSyntaxUID == pydicom.uid.ImplicitVRLittleEndian
    assert (
        ds.file_meta.ImplementationClassUID == rai.RAI_CONTOURS_IMPLEMENTATION_CLASS_UID
    )
    assert ds.file_meta.ImplementationVersionName == rai.RAI_IMPLEMENTATION_VERSION_NAME

    _pull_from_reference(study_header_reference, ds)
    _pull_encrypted_tags_from_reference(study_header_reference, ds)
    modules_to_inherit = [
        module_id
        for module_id, module_options in RTSTRUCT_DICOM_MODULES.items()
        if module_options.inheritance == Inheritance.INHERIT
    ]
    for module_id in modules_to_inherit:
        _raise_if_module_is_invalid(ds, module_id)

    _add_general_equipment(ds)
    _add_rt_series(ds, date, time)
    _add_structure_set_module(
        ds=ds,
        date=date,
        time=time,
        structure_set_label=structure_set_label,
        structure_set_description=structure_set_description,
    )
    _add_roi_modules(ds)
    _add_approval_module(ds)

    for module_id in RTSTRUCT_DICOM_MODULES:
        _raise_if_module_is_invalid(ds, module_id)

    return ds


def create_bare_bones_ds(sop_class_uid):
    dt = datetime.datetime.now()
    date = dt.strftime("%Y%m%d")
    time = dt.strftime("%H%M%S.%f")

    ds = pydicom.Dataset()
    _add_sop_common(ds, date, time, sop_class_uid)
    add_file_meta(ds)

    return ds


def _add_sop_common(ds, date, time, sop_class_uid):
    ds = append.append_dict_to_dataset(
        to_append={
            "SpecificCharacterSet": "ISO_IR 100",
            "InstanceCreationDate": date,
            "InstanceCreationTime": time,
            "InstanceCreatorUID": _uid.machine_uid(),
            "SOPClassUID": sop_class_uid,
            "SOPInstanceUID": _uid.generate_uid(),
        },
        ds=ds,
    )

    _raise_if_module_is_invalid(ds, "sop-common")


def _add_general_equipment(ds):
    append.append_dict_to_dataset(
        to_append={
            "Manufacturer": "Radiotherapy AI Pty Ltd",
        },
        ds=ds,
    )

    _raise_if_module_is_invalid(ds, "general-equipment")


def _add_rt_series(ds, date, time):
    append.append_dict_to_dataset(
        to_append={
            "SeriesDate": date,
            "SeriesTime": time,
            "Modality": "RTSTRUCT",
            "OperatorsName": "",
            "SeriesInstanceUID": _uid.generate_uid(),
            "SeriesNumber": "",
        },
        ds=ds,
    )

    _raise_if_module_is_invalid(ds, "rt-series")


def _add_structure_set_module(
    ds, date, time, structure_set_label, structure_set_description: str
):
    append.append_dict_to_dataset(
        to_append={
            "StructureSetLabel": structure_set_label,
            "StructureSetName": structure_set_label,
            "StructureSetDescription": structure_set_description,
            "StructureSetROISequence": pydicom.Sequence(),
            "StructureSetDate": date,
            "StructureSetTime": time,
        },
        ds=ds,
    )

    _raise_if_module_is_invalid(ds, "structure-set")


def _add_roi_modules(ds):
    append.append_dict_to_dataset(
        to_append={
            "ROIContourSequence": pydicom.Sequence(),
            "RTROIObservationsSequence": pydicom.Sequence(),
        },
        ds=ds,
    )

    _raise_if_module_is_invalid(ds, "roi-contour")
    _raise_if_module_is_invalid(ds, "rt-roi-observations")


def _add_approval_module(ds):
    append.append_dict_to_dataset(
        to_append={
            "ApprovalStatus": "UNAPPROVED",
        },
        ds=ds,
    )

    _raise_if_module_is_invalid(ds, "approval")


def _raise_if_module_is_invalid(ds, module_id):
    attribute_type_map = _inheritance.get_keyword_types_for_module(module_id)
    if RTSTRUCT_DICOM_MODULES[module_id].usage == Usage.USER_OPTIONAL:
        if not _is_there_any_attribute(attribute_type_map, ds):
            return

    try:
        _raise_if_attributes_are_invalid(ds, attribute_type_map)
    except ValueError as e:
        raise ValueError(
            "The provided dataset does not have all of the attributes "
            f"required by the {module_id} module."
        ) from e


def _raise_if_attributes_are_invalid(
    ds: pydicom.Dataset, attribute_type_map: Dict[str, AttributeType]
):
    required_attributes = [
        keyword
        for keyword, attribute_type in attribute_type_map.items()
        if attribute_type
        in (AttributeType.REQUIRED, AttributeType.REQUIRED_EMPTY_IF_UNKNOWN)
    ]

    for attribute in required_attributes:
        if attribute not in ds:
            raise ValueError(f"{attribute} is a required.")

    return True


def _is_there_any_attribute(
    attribute_type_map: Dict[str, AttributeType], ds: "pydicom.Dataset"
):
    overlapping_attributes = set(attribute_type_map.keys()).intersection(dir(ds))
    is_there_any_attribute = len(overlapping_attributes) != 0

    return is_there_any_attribute


# TODO: Is nested inheritance needed?
def _pull_from_reference(reference: pydicom.Dataset, target: pydicom.Dataset):
    mandatory_modules = _module_attributes(
        Usage.MANDATORY, inheritance=Inheritance.INHERIT
    )
    for attribute_type_map in mandatory_modules.values():
        _pull_attributes(reference, target, attribute_type_map)

    optional_modules = _module_attributes(
        Usage.USER_OPTIONAL, inheritance=Inheritance.INHERIT
    )
    for attribute_type_map in optional_modules.values():
        if _is_there_any_attribute(attribute_type_map, reference):
            _pull_attributes(reference, target, attribute_type_map)


def _pull_encrypted_tags_from_reference(
    reference: TypedDataset,
    target: pydicom.Dataset,
):
    """Pull the encrypted private tags accross.

    Only pulls those tags that already correspond to an item within the
    target
    """
    try:
        encrypted_storage_sequence = reference[_tags.STORAGE_SEQUENCE_TAG].value
    except KeyError:
        logging.info("No encrypted data within reference dataset")
        return

    sequence = []
    stored_data: TypedDataset

    for stored_data in encrypted_storage_sequence:
        try:
            _encrypt.get_corresponding_data_element(ds=target, stored_data=stored_data)
        except KeyError:
            continue

        sequence.append(stored_data)

    if sequence:
        block = target.private_block(
            _tags.TAG_GROUP, _tags.PRIVATE_CREATOR, create=True
        )
        block.add_new(
            _tags.STORAGE_SEQUENCE_OFFSET,
            _tags.VR_LOOKUP[_tags.STORAGE_SEQUENCE_TAG],
            pydicom.Sequence(sequence),
        )

    for tag in [_tags.DATASET_GROUPING_TAG]:
        try:
            value = reference[tag]
        except KeyError:
            continue

        target[tag] = value


def _pull_attributes(reference, target, attribute_type_map: Dict[str, AttributeType]):
    for keyword, attribute_type in attribute_type_map.items():
        try:
            value = getattr(reference, keyword)
        except AttributeError:
            if attribute_type == AttributeType.REQUIRED_EMPTY_IF_UNKNOWN:
                value = ""
            else:
                continue

        setattr(target, keyword, value)


@functools.lru_cache()
def _module_attributes(usage: Usage, inheritance: Inheritance = None):
    modules = [
        module_id
        for module_id, module_options in RTSTRUCT_DICOM_MODULES.items()
        if module_options.usage == usage
        and (inheritance is None or module_options.inheritance == inheritance)
    ]

    attributes_to_be_inherited: Dict[str, Dict[str, AttributeType]] = dict()
    for module_id in modules:
        attributes_to_be_inherited[
            module_id
        ] = _inheritance.get_keyword_types_for_module(module_id)

    return attributes_to_be_inherited


def add_file_meta(ds: pydicom.Dataset):
    file_meta = pydicom.dataset.FileMetaDataset()
    append.append_dict_to_dataset(
        to_append={
            "ImplementationClassUID": rai.RAI_CONTOURS_IMPLEMENTATION_CLASS_UID,
            "ImplementationVersionName": rai.RAI_IMPLEMENTATION_VERSION_NAME,
        },
        ds=file_meta,
    )

    ds.file_meta = file_meta
    ds.is_little_endian = True
    ds.is_implicit_VR = True
    ds.fix_meta_info(enforce_standard=True)
