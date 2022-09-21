<!--
Copyright (C) 2022 Radiotherapy AI Holdings Pty Ltd
Copyright (C) 2021-2022 OpenRegulatory (OpenReg GmbH)
This work is licensed under the Creative Commons Attribution 4.0 International
License. <http://creativecommons.org/licenses/by/4.0/>.

Original work by OpenRegulatory available at
<https://github.com/openregulatory/templates>
-->

# Radiotherapy AI's QMS and TechDoc

Radiotherapy AI's Quality Management System and Technical Documentation. Built
on top of [GitHub](https://github.com/RadiotherapyAI/rai) and `git`,
[OpenRegulatory templates](https://github.com/openregulatory/templates), and
[Jupyter Book](https://jupyterbook.org/).

All source for the Medical Device, the Quality Management System, and the
Technical Documentation are available at
<https://github.com/RadiotherapyAI/rai>.

## Disclaimer while QMS and TechDocs are under initial development

This Quality Management System and this Technical Documentation are currently
under active development and there is likely to be both mistakes and omissions.
The creation of these documents is being shared publicly out in the open in the
hope that the development of these documents is able to help other SaMD
companies create and regulate their products and help their patients.

## Device

These documents corresponds to version {{device_version}} of the
{{device_name}} software. Currently this software is pre-release, and both the
software and this document is expected to change before it is available for
clinical use. Please reference the version of these documents that is supplied
to you with the software itself.

### Product Details

- **Manufacturer Name**: {{device_manufacturer}}
- **Manufacturer's Address**: 17 Grampian Place Tatton NSW 2650 Australia
- **Software as a Medical Device Identification**: {{device_name}} {{device_version}}

### Difference to the open source version

This device corresponds to the software downloadable directly from
<https://radiotherapy.ai/> (Regulated Medical Device). It does **not**
correspond to the software downloadable from
<https://github.com/RadiotherapyAI/rai> (Open Source Unregulated
Software).

The Open Source Unregulated Software is provided in the hope that it might be
useful but WITHOUT ANY WARRANTY. It is **not** intended for clinical use, and
is instead intended for research use only.

The Regulated Medical Device described by this documentation corresponds only
to the product that is able to be downloaded from <https://radiotherapy.ai/>.
This is the product that is intended to be able to be used for clinical use
according to the intended purpose described within this documentation.

### Workflow overview

Radiotherapy AI's contour recommendations product is deployed on-site as a
DICOM server. It is designed to sit between your centre's CT scanner and your
treatment planning system.

When patients undergo their simulation, images are auto-sent through to
Radiotherapy AI's DICOM and inference server, contours are auto-generated, and
then the results are then automatically sent through to your treatment planning
system.
