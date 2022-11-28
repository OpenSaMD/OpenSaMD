<!--
Copyright (C) 2022 Radiotherapy AI Holdings Pty Ltd
Copyright (C) 2021-2022 OpenRegulatory (OpenReg GmbH)
This work is licensed under the Creative Commons Attribution 4.0 International
License. <http://creativecommons.org/licenses/by/4.0/>.

Original work by OpenRegulatory available at
<https://github.com/openregulatory/templates>
-->

# Intended Use

## Mapping of Requirements to Document Sections

| MDR Class | MDR Section                   | Document Section |
| --------- | ----------------------------- | ---------------- |
| (All)     | Annex II, 1.1 a) - d), h), i) | (All)            |

| ISO 14971:2019 Section | Document Section |
| ---------------------- | ---------------- |
| 5.2                    | (All)            |

| IEC 62366-1:2015 Section | Document Section |
| ------------------------ | ---------------- |
| 5.1                      | (All)            |

## Product

- Name: {{device_name}}
- Version: {{device_version}}
- Basic UDI-DI: N/A

## {{device_name}} Intended Use

<!-- > Describe the core medical functionality of your device and how it treats,
> diagnoses or alleviates a disease. Keep it high-level so that this
> description is true for as long as possible even when the device is updated. -->

Utilised as clinical decision support software within the radiotherapy
treatment workflow. Provides anatomical contours utilised by health
practitioners to create a radiotherapy treatment plan to assist in cancer
treatment or other radiotherapy treatments.

## Intended Medical Indication

<!-- > Describe the condition(s) and/or disease(s) to be screened, monitored,
> treated, diagnosed, or prevented by your software. Importantly, also list
> exclusion criteria: Maybe patients with a certain diagnosis should not be
> using your device. -->

### Used in cases where there is already a clinically implemented contouring protocol

For each contour provided by the software to the user, the user needs to be
able to validate the contour against the clinically implemented contouring
protocol, and if needed, either refine the provided contour to come into
alignment with the protocol, or potentially completely redraw the contour.

(case-validation)=

### Limited by case validation of the deployed model

It is intended that the usage of the model be limited to use within the
radiotherapy treatment workflow in cases where the model has been validated for
the combination of:

- Contours based on the clinically utilised protocol
- Patient population demographics such as age group, sex, race and disease
  state
- Imaging region
- Patient orientation
- Imaging device
- Imaging modality
- Imaging parameters such as energy, resolution, reconstruction kernels, MRI
  sequences
- Scenario induced imaging artifacts such as metal spinal implants, dental
  work, metal hips

The recommended way to validate that the model appropriately handles the above
cases is to collect a representative clinical dataset of the above for model
validation, and if necessary a further independent dataset for model
refinement.

For new models this representative sample can be utilised in unison with the
provided tools to readily undergo bulk validation and investigation.

For more information on commissioning and ongoing quality assurance of AI
models in radiotherapy see the following article:

> Liesbeth, V., Michaël, C., Anna, M. D., Charlotte, L. B., Wouter, C., & Dirk,
> V. (2020).
> [Overview of artificial intelligence-based applications in radiotherapy: Recommendations for implementation and quality assurance.](https://doi.org/10.1016/j.radonc.2020.09.008)
> Radiotherapy and Oncology.

## Contraindications

<!-- > List anything that you want to explicitly exclude from your intended use. -->

Utilisation is to be limited to where the model itself has undergone in-centre
validation. See section [](case-validation) for further details.

## Patient Population

<!-- > Describe the patient population your software is intended to be used on. Note
> that this may overlap with the user profile (section below), but not
> necessarily. Your software could be used by physicians to diagnose diseases
> in patients, so in that case, they don't overlap. Some ideas for
> characteristics to describe: Age group, weight range, health, condition(s). -->

The patient population is to be limited to where the model itself has undergone
in-centre validation. See section [](case-validation) for further details.

## User Profile

<!-- > Describe the typical user of the software. Some ideas could be:
> Qualifications, prior training (for your software), technical proficiency,
> time spent using the software. -->

### Used by those with appropriate training and knowledge

The contours provided by the {{device_name}} software are a recommendation
only. When being used to support clinical radiotherapy treatment within
Australia these contours are to be provided to a RANZCR certified Radiation
Oncologist or an ASMIRT certified Radiation Therapist for subsequent refinement
according to that clinic's approved contouring protocols.

### Refined by a relevant health professional and subsequently checked by an independent relevant health professional

It is intended that the software results be refined by a relevant health
professional and then be subsequently checked by a separate and independent
relevant health professional before the patient contours are utilised to create
the radiotherapy treatment plan.

### Provides a recommendation only and is not intended to replace clinical judgement

The software provides unapproved DICOM-RT Structure set files. These are then
sent through to a contour drawing, refining and approval system, either a TPS
or a dedicated contouring software system.

The health practitioner, either a Radiation Oncologist or a Radiation
Therapist, is to use their clinical judgement to decide whether or not
refinement is appropriate before approval and whether or not approval is
appropriate at all. This clinical judgement is to be informed by the
department's published contouring protocols to which the software's recommended
contours can be directly compared.

The software is not to be used in situations where the software provides
recommendations that cannot be corroborated with current published clinical
protocols.

## Use Environment Including Software/Hardware

<!-- > Describe the typical use environment. What sort of devices is this running
> on? Does the software only run on one device or on multiple devices? Is it
> loud and chaotic like in an emergency ward? How's the lighting?
>
> Also, add other software or hardware which is required by your device. Most
> commonly, apps require users to have a smartphone with a compatible operating
> system (iOS / Android). -->

The {{device_name}} software is to be installed on a local server with one of
the following OS types and versions:

- Windows >= 10
- Ubuntu LTS >= 22.04

## Operating Principle

<!-- > It's kind of a stretch to describe the "operating principle" of software. I
> guess this makes more sense for hardware devices. In any case, I'd just
> generally state what sort of input goes in and what output comes out, e.g.
> you could be processing images and returning diagnoses. -->

The {{device_name}} software is designed to fulfil the `Automated Contourer`
role within the [IHE RO BRTO-II profile](http://ihe-ro.org/doku.php?id=doc:profiles:brto-ii).

This is defined as:

> A system that consumes [an image series] and creates an RT Structure Set. ...

### To be utilised within the framework of standard DICOM input and output

The software is intended to receive DICOM files that conform to the DICOM
standard. The software that it provides results to is intended to receive and
appropriately handle standards compliant DICOM structure files. It is not
intended to directly interface with another medical device except via this
standard DICOM input output (either file based or DICOM network protocol
based).

### Prompt access to notifications, warnings and alerts

Through the dashboard interface users can designate warning and alert
thresholds for a range of relevant scenarios. The software itself may also
present warnings and alerts. The email address of the user account used to
access the software needs to be able to be readily accessed so that these
configurable alerts and warnings can provide the appropriate notification.

## Part of the Body / Type of Tissue Interacted With

The device is stand-alone software. It receives input from the user and outputs
information. It does not come in contact with tissue or bodily fluids.

## Variants / Accessories

<!-- > Describe variants and/or accessories of/to this device, if applicable. For
> typical stand-alone software of startups, this shouldn't be applicable. -->

This is stand-alone software and this is not applicable.
