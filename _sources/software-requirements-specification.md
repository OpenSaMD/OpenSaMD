---
id: SRS-001
revision: 1
title: Software Requirements Specification
---

# Software Requirements Specification

## Purpose

This document describe _what_ Radiotherapy AI Contour Recommendations software must do.

This document is meant to be read and agreed-upon by the project owners and by software developers during design and construction.



[[FDA-CPSSCMD:srs]]

## Scope

This document applies to Radiotherapy AI Contour Recommendations release `v0.1.16`.

## Definitions

The **Food and Drug Administration (FDA)** is a United State government agency responsible for protecting the public health by ensuring the safety, efficacy, and security of human and veterinary drugs, biological products, and medical devices.

The **Health Insurance Portability and Accountability Act** (HIPAA) is a United States law designed to provide privacy standards to protect patients' medical records and other health information provided to health plans, doctors, hospitals and other healthcare providers.

**Protected Health Information** (PHI) means individually identifiable information that is created by Radiotherapy AI Contour Recommendations and relates to the past, present, or future physical or mental health or condition of any individual, the provision of health care to an individual, or the past, present, or future payment for the provision of health care to an individual.

A **User** is a person who interacts with (i.e., operates or handles) the device.

**UI** is an acronym for user interface.

## Users

TODO: Device Users are anyone who interacts with (i.e., operates or handles) the device. Different users will have different requirements, so it is useful to enumerate all of them so that no important requirements are missed. A few common stakeholders are listed below for convenience.

There may be several different types of users, in which case it is worth adding more sections for each type.

- Physical size, strength, and stamina,
- Physical dexterity, flexibility, and coordination,
- Sensory abilities (i.e., vision, hearing, tactile sensitivity),
- Cognitive abilities, including memory,
- Medical condition for which the device is being used,
- Comorbidities (i.e., multiple conditions or diseases),
- Literacy and language skills,
- General health status,
- Mental and emotional state,
- Level of education and health literacy relative to the medical condition involved,
- General knowledge of similar types of devices,
- Knowledge of and experience with the particular device,
- Ability to learn and adapt to a new device, and
- Willingness and motivation to learn to use a new device.

ENDTODO

This section enumerates the types of device users, describe their characteristics, and why they are interested in the device [[FDA-HFE:5.1]].

### Patient

TODO: write in details, or remove this section

### Physician

TODO: write in details, or remove this section

### Hospital IT Personnel

TODO: write in details, or remove this section

## Use Environments

TODO:

You should evaluate and understand relevant characteristics of all intended use environments and describe them for the purpose of HFE/UE evaluation and design. These characteristics should be taken into account during the medical device development process, so that devices might be more accommodating of the conditions of use that could affect their use safety and effectiveness.

The environments in which medical devices are used might include a variety of conditions that could determine optimal user interface design. Medical devices might be used in clinical environments or non-clinical environments, community settings or moving vehicles. Examples of environmental use conditions include the following:

- The lighting level might be low or high, making it hard to see device displays or controls.
- The noise level might be high, making it hard to hear device operation feedback or audible alerts and alarms or to distinguish one alarm from another.
- The room could contain multiple models of the same device, component or accessory, making it difficult to identify and select the correct one.
- The room might be full of equipment or clutter or busy with other people and activities, making it difficult for people to maneuver in the space and providing distractions that could confuse or overwhelm the device user.
- The device might be used in a moving vehicle, subjecting the device and the user to jostling and vibration that could make it difficult for the user to read a display or perform fine motor movements.

You should evaluate and understand relevant characteristics of all intended use environments and describe them for the purpose of HFE/UE evaluation and design. These characteristics should be taken into account during the medical device development process, so that devices might be more accommodating of the conditions of use that could affect their use safety and effectiveness.

ENDTODO

This section enumerates the environments in which the Radiotherapy AI Contour Recommendations will be used [[FDA-HFE:5.2]].

### Radiology Reading Room

TODO: write in details, or remove this section

### Radiologist's Home

TODO: write in details, or remove this section

## Use Cases

### Problem X

Brief description.

### Problem Y

Brief description.

## Requirement Details



### Patient privacy is retained

_Requirement ID:_ r-1-1

When patient data is submitted to the cloud infrastructure it shall be de-identified.



### Patient data stays within the organisation's legislative jurisdiction

_Requirement ID:_ r-1-2

All storage and computation on the de-identified patient data has to be undergone within the organisation's legislative jurisdiction.



### Contour quality

_Requirement ID:_ r-2

The contour quality is sufficient such that a clinician or radiotherapist are able to refine the contours as opposed to throwing them away and starting again. This is quantified by having the Dice, Surface Dice, and Hausdorff metrics be similar to inter-observer variance between health practitioners.



### Timeliness and robustness

_Requirement ID:_ r-3

The software is able to produce results promptly and reliably. Turn around times should be reliably on the order of 1-5 minutes.



### Seamless integration into workflow

_Requirement ID:_ r-4

The software shall seamlessly integrate into the current organisation's workflows. No manual steps shall be needed for the data to be sent from the organisation's imaging device using the standard DICOM export and to have it arrive within the planning system with all of the extra utility expected by the organisation within a DICOM structure file.



### Continuous validation of appropriate model refinement

_Requirement ID:_ r-5-1

Every patient where contours are refined shall be able to be used continuously to validate whether the results are being appropriately refined and hence being used according to the software's intended purpose



### Continuous validation of the model meeting requirements

_Requirement ID:_ r-5-2

Every patient where contours are refined shall be able to be used continuously to validate whether the refinements being undergone are overly onerous, indicating that potentially the current model is not, or is no longer meeting requirements.



### Bulk historical validation for new models

_Requirement ID:_ r-5-3

When a new model is available there will be a means for bulk submission and validation of historical data to validate whether or not the new model is fit for purpose and subsequent deployment.
It shall be clear which historical data was utilised to train the model and which data was specifically held out from the model so as to appropriately inform the wider generalisability of the model.



### Validation notification system

_Requirement ID:_ r-5-4

Provide a means to set up automated notifications, alerts, and reports to a designated email address.



### Improve the models based directly on the organisation's usage

_Requirement ID:_ r-6

The models utilised shall be able to be updated using the clinic's refinements. So that contour quality continuously improves and keeps up with current clinical practice.
The software shall be able to promptly facilitate whenever the clinic desires a new contour type, or adjustment of the trained contouring protocols.



### Simple distributed configuration

_Requirement ID:_ r-7

Any user with access to the organisation's configuration dashboard should be able to easily and remotely bulk configure any DICOM server installed for that organisation. This includes DICOM servers that are installed within separate legislative jurisdictions.



### Simple installation and minimal system requirements

_Requirement ID:_ r-8

The DICOM server shall install simply and quickly. It shall be able to install on a standard Windows 10 machine with minimal systems specifications. Installation alongside other software shall cause no issue.



### Provide clear reference to the basis of the contour recommendation

_Requirement ID:_ r-9

Shall clearly reference the basis of the contour recommendations, by including a reference to the organisation's contouring protocols. This is so that these protocols can be easily and readily independently reviewed by the health practitioner. Their judgement can then be utilised whether or not the contour recommendations appropriately align with the written protocol.
This is as per the requirement of the TGA for exempt clinical decision support software.



### Structure DICOM files are not pre-approved

_Requirement ID:_ r-10

The software shall only send unapproved structure files to the TPS.



### Able to opt to only upload data

_Requirement ID:_ r-11

Provide a DICOM target which allows for the option for only data uploading.



## Traceability Tables



### Software Requirements Table

[[Each requirement has a unique id satisfying 62304:5.2.6.e]]
| ID | Title |
| --- | --- |
| r-1-1 | Patient privacy is retained |
| r-1-2 | Patient data stays within the organisation's legislative jurisdiction |
| r-2 | Contour quality |
| r-3 | Timeliness and robustness |
| r-4 | Seamless integration into workflow |
| r-5-1 | Continuous validation of appropriate model refinement |
| r-5-2 | Continuous validation of the model meeting requirements |
| r-5-3 | Bulk historical validation for new models |
| r-5-4 | Validation notification system |
| r-6 | Improve the models based directly on the organisation's usage |
| r-7 | Simple distributed configuration |
| r-8 | Simple installation and minimal system requirements |
| r-9 | Provide clear reference to the basis of the contour recommendation |
| r-10 | Structure DICOM files are not pre-approved |
| r-11 | Able to opt to only upload data |
