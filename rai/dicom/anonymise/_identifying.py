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


import functools
import re

import pydicom
import pydicom.datadict
import pydicom.tag

from rai.vendor.innolitics.standard.load import get_standard

EXPLICITLY_ALLOW = {"ROIName", "ROIObservationLabel"}


@functools.lru_cache(maxsize=1)
def get_non_identifying():
    identifying_keywords, _ = get_identifying()

    attributes = get_standard("attributes")
    all_keywords = {attribute["keyword"] for attribute in attributes}

    assert all_keywords.issuperset(identifying_keywords)
    non_identifying_keywords = all_keywords.difference(identifying_keywords)

    non_identifying_tags = set()
    for keyword in non_identifying_keywords:
        try:
            non_identifying_tags.add(pydicom.tag.Tag(keyword))
        except ValueError:
            pass

    return non_identifying_keywords, non_identifying_tags


@functools.lru_cache(maxsize=1)
def get_identifying():
    confidentiality_profile = get_standard("confidentiality_profile_attributes")

    all_innolitics_names = [item["name"] for item in confidentiality_profile]
    all_copy_paste_names = get_standard("identifying_copy_paste")

    allow_uids_profile_names = [
        item["name"]
        for item in confidentiality_profile
        if ("rtnUIDsOpt" in item.keys() and item["rtnUIDsOpt"] == "K")
    ]
    allow_uids_profile_names += [
        "ReferencedImageSequence",
        "ReferencedStudySequence",
    ]
    allow_uids_profile_keywords = set(
        _convert_names_to_keywords(allow_uids_profile_names)
    )

    all_innolitics_keywords = set(_convert_names_to_keywords(all_innolitics_names))

    # Copied from the webpage <http://dicom.nema.org/Medical/Dicom/2021b/output/chtml/part15/chapter_E.html>
    all_copy_paste_keywords = set(_convert_names_to_keywords(all_copy_paste_names))

    all_keywords = all_innolitics_keywords.union(all_copy_paste_keywords).union(
        INDEPENDENT_LIST
    )
    identifying_keywords = all_keywords.difference(allow_uids_profile_keywords)
    identifying_keywords = identifying_keywords.difference(EXPLICITLY_ALLOW)

    identifying_tags = {pydicom.tag.Tag(keyword) for keyword in identifying_keywords}

    return identifying_keywords, identifying_tags


def _convert_names_to_keywords(names):
    caps_exceptions = {
        "DateTime",
        "ID",
        "UID",
        "GPS",
        "DOP",
        "MAC",
        "IDs",
        "AE",
        "RT",
        "SOP",
        "ROI",
        "UTC",
        "UDI",
    }
    ignore = {"CurveData", "OverlayComments", "OverlayData", "PrivateAttributes"}
    maps = {
        "MultiEnergy": "Multienergy",  # Why the inconsistency in the standard here?
        "PerformersOrganization": "PerformerOrganization",
        "PhysiciansName": "PhysicianName",
        "RecipientOfResults": "RecipientsOfResults",
        "PerformersName": "PerformerName",
        "OperatorsIdentification": "OperatorIdentification",
    }

    keywords = []
    for name in names:
        name = name.split("\n")[0]
        name = (
            name.replace("'s", "").replace("'s", "").replace("(", "").replace(")", "")
        )

        split = re.split("[ -/]", name)
        split_with_caps = [
            item.capitalize() if item not in caps_exceptions else item for item in split
        ]

        keyword = "".join(split_with_caps)
        if keyword in ignore:
            continue

        for initial, replace_with in maps.items():
            keyword = keyword.replace(initial, replace_with)

        keywords.append(keyword)

    return keywords


INDEPENDENT_LIST = [
    "AccessionNumber",
    "AcquisitionComments",
    "AcquisitionContextSequence",
    "AcquisitionDate",
    "AcquisitionDateTime",
    "AcquisitionDeviceProcessingDescription",
    "AcquisitionTime",
    "ActualHumanPerformersSequence",
    "AdditionalPatientHistory",
    "AdmissionID",
    "AdmittingDate",
    "AdmittingDiagnosesCodeSequence",
    "AdmittingDiagnosesDescription",
    "AdmittingTime",
    "Allergies",
    "Arbitrary",
    "AuthorObserverSequence",
    "BranchOfService",
    "CassetteID",
    "CommentsOnThePerformedProcedureStep",
    "ConfidentialityConstraintOnPatientDataDescription",
    "ContentCreatorName",
    "ContentDate",
    "ContentSequence",
    "ContentTime",
    "ContrastBolusAgent",
    "ContributionDescription",
    "CountryOfResidence",
    "CurrentPatientLocation",
    "CurveDate",
    "CurveTime",
    "CustodialOrganizationSequence",
    "DataSetTrailingPadding",
    "Date",
    "DateTime",
    "DerivationDescription",
    "DetectorID",
    "DeviceSerialNumber",
    "DigitalSignaturesSequence",
    "DischargeDiagnosisDescription",
    "DistributionAddress",
    "DistributionName",
    "EthnicGroup",
    "FillerOrderNumberImagingServiceRequest",
    "FrameComments",
    "GantryID",
    "GeneratorID",
    "GraphicAnnotationSequence",
    "HumanPerformerName",
    "HumanPerformerOrganization",
    "IconImageSequence",
    "IdentifyingComments",
    "ImageComments",
    "ImagePresentationComments",
    "ImagingServiceRequestComments",
    "Impressions",
    "InstanceCreationDate",
    "InstanceCreationTime",
    "InstitutionAddress",
    "InstitutionCodeSequence",
    "InstitutionalDepartmentName",
    "InstitutionName",
    "InsurancePlanIdentification",
    "IntendedRecipientsOfResultsIdentificationSequence",
    "InterpretationApproverSequence",
    "InterpretationAuthor",
    "InterpretationDiagnosisDescription",
    "InterpretationIDIssuer",
    "InterpretationRecorder",
    "InterpretationText",
    "InterpretationTranscriber",
    "IssuerOfAdmissionID",
    "IssuerOfPatientID",
    "IssuerOfServiceEpisodeID",
    "LastMenstrualDate",
    "MAC",
    "MedicalAlerts",
    "MedicalRecordLocator",
    "MilitaryRank",
    "ModifiedAttributesSequence",
    "ModifiedImageDescription",
    "ModifyingDeviceID",
    "ModifyingDeviceManufacturer",
    "NameOfPhysiciansReadingStudy",
    "NamesOfIntendedRecipientsOfResults",
    "Occupation",
    "OperatorIdentificationSequence",
    "OperatorsName",
    "OriginalAttributesSequence",
    "OrderCallbackPhoneNumber",
    "OrderEnteredBy",
    "OrderEntererLocation",
    "OtherPatientIDs",
    "OtherPatientIDsSequence",
    "OtherPatientNames",
    "OverlayDate",
    "OverlayTime",
    "ParticipantSequence",
    "PatientAddress",
    "PatientAge",
    "PatientBirthDate",
    "PatientBirthName",
    "PatientBirthTime",
    "PatientComments",
    "PatientID",
    "PatientInstitutionResidence",
    "PatientInsurancePlanCodeSequence",
    "PatientMotherBirthName",
    "PatientName",
    "PatientPrimaryLanguageCodeSequence",
    "PatientPrimaryLanguageModifierCodeSequence",
    "PatientReligiousPreference",
    "PatientSex",
    "PatientSexNeutered",
    "PatientSize",
    "PatientState",
    "PatientTelephoneNumbers",
    "PatientTransportArrangements",
    "PatientWeight",
    "PerformedLocation",
    "PerformedProcedureStepDescription",
    "PerformedProcedureStepID",
    "PerformedProcedureStepStartDate",
    "PerformedProcedureStepStartTime",
    "PerformedStationAETitle",
    "PerformedStationGeographicLocationCodeSequence",
    "PerformedStationName",
    "PerformedStationNameCodeSequence",
    "PerformingPhysicianIdentificationSequence",
    "PerformingPhysicianName",
    "PersonAddress",
    "PersonIdentificationCodeSequence",
    "PersonName",
    "PersonTelephoneNumbers",
    "PhysicianApprovingInterpretation",
    "PhysiciansReadingStudyIdentificationSequence",
    "PhysiciansOfRecord",
    "PhysiciansOfRecordIdentificationSequence",
    "PhysiciansReadingStudyIdentificationSequence",
    "PlacerOrderNumberImagingServiceRequest",
    "PlateID",
    "PreMedication",
    "PregnancyStatus",
    "ProtocolName",
    "ReasonForTheImagingServiceRequest",
    "ReasonForStudy",
    "ReferencedDigitalSignatureSequence",
    "ReferencedImageSequence",
    "ReferencedPatientAliasSequence",
    "ReferencedPatientSequence",
    "ReferencedPerformedProcedureStepSequence",
    "ReferencedSOPInstanceMACSequence",
    "ReferencedStudySequence",
    "ReferringPhysicianAddress",
    "ReferringPhysicianIdentificationSequence",
    "ReferringPhysicianName",
    "ReferringPhysicianTelephoneNumbers",
    "RegionOfResidence",
    "RequestAttributesSequence",
    "RequestedContrastAgent",
    "RequestedProcedureComments",
    "RequestedProcedureDescription",
    "RequestedProcedureID",
    "RequestedProcedureLocation",
    "RequestingPhysician",
    "RequestingService",
    "ResponsibleOrganization",
    "ResponsiblePerson",
    "ResultsComments",
    "ResultsDistributionListSequence",
    "ResultsIDIssuer",
    "ReviewerName",
    "ScheduledHumanPerformersSequence",
    "ScheduledPatientInstitutionResidence",
    "ScheduledPerformingPhysicianIdentificationSequence",
    "ScheduledPerformingPhysicianName",
    "ScheduledProcedureStepDescription",
    "ScheduledProcedureStepEndDate",
    "ScheduledProcedureStepEndTime",
    "ScheduledProcedureStepLocation",
    "ScheduledProcedureStepStartDate",
    "ScheduledProcedureStepStartTime",
    "ScheduledStationAETitle",
    "ScheduledStationGeographicLocationCodeSequence",
    "ScheduledStationName",
    "ScheduledStationNameCodeSequence",
    "ScheduledStudyLocation",
    "ScheduledStudyLocationAETitle",
    "SecondaryReviewerName",
    "SeriesDate",
    "SeriesDescription",
    "SeriesTime",
    "ServiceEpisodeDescription",
    "ServiceEpisodeID",
    "SmokingStatus",
    "SourceImageSequence",
    "SpecialNeeds",
    "StationName",
    "StudyComments",
    "StudyDate",
    "StudyDescription",
    "StudyID",
    "StudyIDIssuer",
    "StudyTime",
    "TextComments",
    "TextString",
    "Time",
    "TimezoneOffsetFromUTC",
    "TopicAuthor",
    "TopicKeywords",
    "TopicSubject",
    "TopicTitle",
    "VerifyingObserverIdentificationCodeSequence",
    "VerifyingObserverName",
    "VerifyingObserverSequence",
    "VerifyingOrganization",
    "VisitComments",
]
