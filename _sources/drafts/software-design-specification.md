---
id: SDS-001
revision: 1
title: Software Design Specification
---

# Software Design Specification

## Purpose

This document describes _how_ Radiotherapy AI Contour Recommendations shall fulfil the requirements
described in the software requirements specification. It discusses the
computation hardware the software will be expected run on, the software
system's architecture, functional specifications associated with each software
requirement, and user interface mockups.

It is written primarily for engineers working on Radiotherapy AI Contour Recommendations, who have the
source code available, in addition to this document.

[[The legacy Software option of 62304:4.4 is not in use here.]]

[[FDA-CPSSCMD:sds]]

## Scope

This document applies to Radiotherapy AI Contour Recommendations release `v0.1.16`.

## Definitions

The **Food and Drug Administration (FDA)** is a United State government agency
responsible for protecting the public health by ensuring the safety, efficacy,
and security of human and veterinary drugs, biological products, and medical
devices.

The **Health Insurance Portability and Accountability Act** (HIPAA) is a United
States law designed to provide privacy standards to protect patients' medical
records and other health information provided to health plans, doctors,
hospitals and other healthcare providers.

**Protected Health Information** (PHI) means individually identifiable
information that is created by Radiotherapy AI Contour Recommendations and relates to the past,
present, or future physical or mental health or condition of any individual,
the provision of health care to an individual, or the past, present, or future
payment for the provision of health care to an individual.

**UI** is an acronym for user interface.

## Software Description

[[FDA-CPSSCMD:software-description]]

TODO: Fill in the software description. Usually it should the programming
language, hardware platform, operating system (if applicable), and any SOUP.

## Architecture Design Chart

TODO: Add a block diagram showing a detailed depiction of functional units and
software items. You may also want to include state diagrams as well as flow
charts [[FDA-CPSSCMD:architecture-design-chart]]

## Software Items

### Software Item A

### Software Item B

## SOUP Software Items

This section enumerates the SOUP software items present within Radiotherapy AI Contour Recommendations.



### Example Camera SDK

**Manufacturer:**

Basler AG

**Version:**

`5.3.1`



### FFTW

**Manufacturer:**

SOUP was developed collaboratively by the free open-source software community, and does not have a manufacturer in the traditional sense.

**Version:**

`3.3.5`



## Functional Specifications



### Patient privacy is retained

_Requirement ID:_ r-1-1

_Requirement:_ When patient data is submitted to the cloud infrastructure it shall be de-identified.



_Functional Specifications:_
Utilising the DICOM standard to flag header items that are deemed
non-identifying, then utilising symmetric Fernet encryption with a client
side key to encrypt all remaining header items. Utilise a well maintained
cryptography library that is held to a high standard by the community.

Provide a means to block certain DICOM file types that are not regularly
used within Radiotherapy but do sometimes have patient information burnt
into the pixel values of the image. This is to protect against an
accidental bulk DICOM send causing burnt in patient information to being
uploaded into the cloud.


### Patient data stays within the organisation's legislative jurisdiction

_Requirement ID:_ r-1-2

_Requirement:_ All storage and computation on the de-identified patient data has to be undergone within the organisation's legislative jurisdiction.



_Functional Specifications:_
The globally hosted API only handles API access credentials, the "global
API". This then hands the client over to the API hosted within the
organisation's legislative jurisdiction, "local API". Both of these APIs
utilise global load balancers meaning that information sent to these APIs
can have their TLS traffic unpacked on Google's servers anywhere in the
world. However, the information sent through to the APIs are only UIDs,
URLs, API access credentials, and other non patient-information. No
encrypted patient information, or tomographic scans are ever sent to the
APIs.

To submit the de-identified patient scans for storage and model inference
the client software provides an organisation access token as well as the
UID for upload to the local API. The organisation access token is unique to
the locally hosted DICOM server. The UID is the SOP Instance UID within the
DICOM header. The local API then designates a storage location within the
cloud storage infrastructure and responds to the user's client with an
upload URL. This upload URL uploads directly to the storage location within
the local jurisdiction. The data itself is not sent to the API.

All inference is undergone on computational hardware within the local
jurisdiction.

All results are returned to the customer's DICOM server via the local API
via download URLs that directly download the patient's results from the
local jurisdiction's cloud storage to the server installed locally. The
results themselves are not send via the API.


### Contour quality

_Requirement ID:_ r-2

_Requirement:_ The contour quality is sufficient such that a clinician or radiotherapist are able to refine the contours as opposed to throwing them away and starting again. This is quantified by having the Dice, Surface Dice, and Hausdorff metrics be similar to inter-observer variance between health practitioners.



_Functional Specifications:_
This is achieved through utilising a regularised UNet deep learning model.
Validation that this contour quality is up to standard is continuously
validated for every patient through an automated reporting tool as well as
the capacity to further drill down through the results within the provided
dashboard. When model results and refinements sufficiently differ a new
model can be produced, validated, and deployed.


### Timeliness and robustness

_Requirement ID:_ r-3

_Requirement:_ The software is able to produce results promptly and reliably. Turn around times should be reliably on the order of 1-5 minutes.



_Functional Specifications:_
Multiple GPUs will be utilised in parallel within the cloud infrastructure
to run the computation.


### Seamless integration into workflow

_Requirement ID:_ r-4

_Requirement:_ The software shall seamlessly integrate into the current organisation's workflows. No manual steps shall be needed for the data to be sent from the organisation's imaging device using the standard DICOM export and to have it arrive within the planning system with all of the extra utility expected by the organisation within a DICOM structure file.



_Functional Specifications:_
The machine learning models will be trained such that the same model can be
utilised for all treatment sites and imaging modalities. This means that no
manual tagging or selection of treatment region is required.

The software will be set up as a DICOM server that can be installed on as
many systems and in as many locations as desired without any extra cost.
These DICOM servers receive DICOM compliant imaging and send through to the
TPS DICOM compliant structure files.

Items such as contour colours, names, and material codes (aka. eclipse
codes) will be included within these DICOM structure files and will be able
to be easily configured within the configuration dashboard.

Users can configure a single or multiple export locations. Export locations
can be DICOM targets or filesystems (local or networked).


### Continuous validation of appropriate model refinement

_Requirement ID:_ r-5-1

_Requirement:_ Every patient where contours are refined shall be able to be used continuously to validate whether the results are being appropriately refined and hence being used according to the software's intended purpose



_Functional Specifications:_
The provided dashboard and automated validation framework provided within
the software will be able to be able to detect if no or minimal refinements
are being undergone. Or if there are outliers in the amount of refining
occurring.


### Continuous validation of the model meeting requirements

_Requirement ID:_ r-5-2

_Requirement:_ Every patient where contours are refined shall be able to be used continuously to validate whether the refinements being undergone are overly onerous, indicating that potentially the current model is not, or is no longer meeting requirements.



_Functional Specifications:_
The provided dashboard and automated validation framework provided within
the software will be able to be able to detect if there are significant
refinements consistently being undergone.


### Bulk historical validation for new models

_Requirement ID:_ r-5-3

_Requirement:_ When a new model is available there will be a means for bulk submission and validation of historical data to validate whether or not the new model is fit for purpose and subsequent deployment.
It shall be clear which historical data was utilised to train the model and which data was specifically held out from the model so as to appropriately inform the wider generalisability of the model.



_Functional Specifications:_
Before patient data is has its identifying information encrypted for
submission to the cloud an SHA224 hash is taken of the birth date, and then
just the first byte of that hash, representing a number between 0 and 15 is
then stored within the DICOM file. This number between 0 and 15 represents
that DICOM files data grouping. Models will only be trained on a subset of
those groupings, and then all DICOM files with that grouping will be
classified as potential training data. This will be approximately 3/4 of
the data. Approximately 1/8th of the data groups will be utilised to provide
feedback on the models capacity to generalise during model development.
The remaining 1/8th of the data will be designated as hold-out data, for
use by the clinic to receive an un-biased measure of the model's
performance.

So as to not dis-incentivise validation work, when patient data has already
been previously submitted and it is used for these bulk historical
validation tasks, those inference calculations will not be counted against
the organisation's paid quota.


### Validation notification system

_Requirement ID:_ r-5-4

_Requirement:_ Provide a means to set up automated notifications, alerts, and reports to a designated email address.



_Functional Specifications:_
For all validation items within the validation dashboard require a means
for the user to set up alert thresholds and automated validation and
commissioning reports.


### Improve the models based directly on the organisation's usage

_Requirement ID:_ r-6

_Requirement:_ The models utilised shall be able to be updated using the clinic's refinements. So that contour quality continuously improves and keeps up with current clinical practice.
The software shall be able to promptly facilitate whenever the clinic desires a new contour type, or adjustment of the trained contouring protocols.



_Functional Specifications:_
Within the continuous validation framework defined above, whenever
structures are refined within the clinic this data is sent back to the
DICOM server.

The model training has been built from the ground up to support training
based on standard clinical data. As such, these refinements are able to
provide targetted feedback to the model training to achieve targetted
improvements.


### Simple distributed configuration

_Requirement ID:_ r-7

_Requirement:_ Any user with access to the organisation's configuration dashboard should be able to easily and remotely bulk configure any DICOM server installed for that organisation. This includes DICOM servers that are installed within separate legislative jurisdictions.



_Functional Specifications:_
Each user is assigned to the relevant organisation. And each organisation
has designated legislative jurisdictions. Upon installation of a DICOM
server it is configured to be within one of the organisation's legislative
jurisdictions.

Upon installation of each DICOM server that server is given a customisable
name to help the user identify which server that is, the hostname of the
computer it is installed on, and what legislative jurisdiction it has been
locked into.

When a user wants to update a configuration item, such as a contour name,
material code, or DICOM send location, this will be able to be done through
the configuration dashboard. Any DICOM server will be able to be configured
through this dashboard from any of the organisation's locations.

This dashboard can also be utilised to schedule DICOM servers to run a
software update.


### Simple installation and minimal system requirements

_Requirement ID:_ r-8

_Requirement:_ The DICOM server shall install simply and quickly. It shall be able to install on a standard Windows 10 machine with minimal systems specifications. Installation alongside other software shall cause no issue.



_Functional Specifications:_
Vendor end-to-end testing of the software is undergone on a Windows 10
machine with minimal requirements. This is 4 GB of RAM, 4 CPU cores and
a 128 GB SSD hard drive without a dedicated GPU.

All intensive computation is undergone in the cloud.

The most complicated part of the installation is transferring the
organisation's encryption key. The organisation is to have a client side
encryption key that is generated on the organisation's machine and shared
between all DICOM servers that are within the same legislative
jurisdiction. The software shall provide a means to backup this encryption
key and transfer it to new DICOM servers for installation.

The primary system requirements end up being the network upload speed
required for reliable and prompt results. It is recommended that the server
can reliably achieve upload speeds of at least 20 Mbits / s.


### Provide clear reference to the basis of the contour recommendation

_Requirement ID:_ r-9

_Requirement:_ Shall clearly reference the basis of the contour recommendations, by including a reference to the organisation's contouring protocols. This is so that these protocols can be easily and readily independently reviewed by the health practitioner. Their judgement can then be utilised whether or not the contour recommendations appropriately align with the written protocol.
This is as per the requirement of the TGA for exempt clinical decision support software.



_Functional Specifications:_
A file path or URL that references each of the organisation's contouring
protocols is attached to the DICOM ROI Description field. It is then up to
the corresponding TPS to appropriately display this description field to
the user for their reference.


### Structure DICOM files are not pre-approved

_Requirement ID:_ r-10

_Requirement:_ The software shall only send unapproved structure files to the TPS.



_Functional Specifications:_
All generated DICOM files that are sent to the planning system are
explicitly set to be not approved within the DICOM header.


### Able to opt to only upload data

_Requirement ID:_ r-11

_Requirement:_ Provide a DICOM target which allows for the option for only data uploading.



_Functional Specifications:_
Provide two DICOM targets, one DICOM target for upload only, the other
DICOM target for running inference.

Potentially provide other DICOM targets to be configurable to achieve
other tasks.


## User Interface Mockups

TODO:

If you have user interface mockups, this is a good place to put them. One
strategy is to include a sub-section for each screen, along with its own image
file. Here are some examples:

### Screen One (PNG)

Use something like: `![Screen One](./images/uimockups/example-ui-mockup-001.png)`

Which produces:

![Screen One](./images/uimockups/example-ui-mockup-001.png)

### Screen Two (JPG)

Use something like: `![Screen Two](./images/uimockups/example-ui-mockup-002.jpg)`

Which produces:

![Screen Two](./images/uimockups/example-ui-mockup-002.jpg)

### Screen Three (PNG Online)

Use something like: `![Screen Three](https://github.com/innolitics/rdm/raw/a29fed650e55b376157cebe8843b087209a0b92a/rdm/init_files/images/uimockups/example-ui-mockup-001.png)`

Which produces:

![Screen Three](https://github.com/innolitics/rdm/raw/a29fed650e55b376157cebe8843b087209a0b92a/rdm/init_files/images/uimockups/example-ui-mockup-001.png)

ENDTODO
