# Introduction

These documents corresponds to version `v0.1.16` of the
Radiotherapy AI Contour Recommendations software. Currently this software is pre-release, and both the
software and this document is expected to change before it is available for
clinical use. Please reference the version of these documents that is supplied
to you with the software itself.

## Product Details

- **Manufacturer Name**: Radiotherapy AI Pty Ltd
- **Manufacturer's Address**: 17 Grampian Place Tatton NSW 2650 Australia
- **Software as a Medical Device Identification**: Radiotherapy AI Contour Recommendations `v0.1.16`

## Overview

Radiotherapy AI's contour recommendations product is deployed onsite as a DICOM
server. It is designed to sit between your centre's CT scanner and your
treatment planning system.

When patients undergo their simulation images are auto-sent through to
Radiotherapy AI's DICOM server. The patient identifying information within the
DICOM header is then encrypted with a client side encryption key, and then
these patient scans are then securely submitted to Google Cloud infrastructure
within Sydney to undergo contouring.

These contours are converted into an RT-DICOM Structure Set file and are then
sent back to the Radiotherapy AI DICOM server for subsequent forwarding through
to the centre's treatment planning system for refinement by the clinical
Radiation Oncologist or Radiation Therapist (the health practitioner) according
to the site's contouring protocols.

In practice, the health practitioner does not directly interact with
Radiotherapy AI's software. Instead, the results from Radiotherapy AI's
software is provided to your centre's treatment planning system for the health
practitioner's subsequent refinement.

A digram outlining the dataflow pipeline is provided within
{numref}`Figure %s <pipeline>`:

```{figure} img/deployment-diagram.png
:name: pipeline

Outline of the data transmitted between the different systems in the pipeline.
```

The contouring algorithm that is applied to the CT scans is based off of
historical treatment contouring data.
