---
id: SDS-001
revision: 1
title: Software Design Specification
---

# Software Design Specification

## Purpose

This document describes _how_ DEVICE shall fulfill the requirements described in the software requirements specification. It discusses the computation hardware the software will be expected run on, the software system's architecture, functional specifications associated with each software requirement, and user interface mockups.

It is written primarily for engineers working on DEVICE, who have the source code available, in addition to this document.

[[The legacy Software option of 62304:4.4 is not in use here.]]

[[FDA-CPSSCMD:sds]]

## Scope

This document applies to DEVICE release v0.1.0.

## Definitions

The **Food and Drug Administration (FDA)** is a United State government agency responsible for protecting the public health by ensuring the safety, efficacy, and security of human and veterinary drugs, biological products, and medical devices.

The **Health Insurance Portability and Accountability Act** (HIPAA) is a United States law designed to provide privacy standards to protect patients' medical records and other health information provided to health plans, doctors, hospitals and other healthcare providers.

**Protected Health Information** (PHI) means individually identifiable information that is created by DEVICE and relates to the past, present, or future physical or mental health or condition of any individual, the provision of health care to an individual, or the past, present, or future payment for the provision of health care to an individual.

**UI** is an acronym for user interface.

## Software Description

[[FDA-CPSSCMD:software-description]]

TODO: Fill in the software description. Usually it should the programming language, hardware platform, operating system (if applicable), and any SOUP.

## Architecture Design Chart

TODO: Add a block diagram showing a detailed depiction of functional units and software items. You may also want to include state diagrams as well as flow charts [[FDA-CPSSCMD:architecture-design-chart]]

## Software Items

### Software Item A

### Software Item B

## SOUP Software Items

This section enumerates the SOUP software items present within DEVICE.



### Example Camera SDK

**Manufacturer:**

Basler AG

**Version:**

`5.3.1`

**Functional and Performance Requirements:**

To allow us to configure, control, and retrieve images from our cameras.


**Hardware & Software Requirements:**

Linux kernel version 3.x or higher


**Known Anomalies:**


No anomalies found that would result in incorrect behaviour for DEVICE leading to a hazardous situation.

**Open Anomaly List (Reference Only):**

`https://example.url/pointing/to/issue/list`


### FFTW

**Manufacturer:**

SOUP was developed collaboratively by the free open-source software community, and does not have a manufacturer in the traditional sense.

**Version:**

`3.3.5`

**Functional and Performance Requirements:**

To calculate the Fast Fourier Transform.


**Hardware & Software Requirements:**

No noteworthy software or hardware requirements.

**Known Anomalies:**


No anomalies found that would result in incorrect behaviour for DEVICE leading to a hazardous situation.

**Open Anomaly List (Reference Only):**

`https://github.com/FFTW/fftw3/issues`


## Functional Specifications



### First Example Requirement

_Requirement ID:_ r-1

_Requirement:_ A brief description of the requirement; should use the world "shall".  If the software is a "software only device", then no "system_requirements" are necessary---you can remove these keys completely.  They are only necessary for medical devices with a hardware component.


_Functional Specifications:_
The specification should describe *how* the requirement is met.  Thus, the requirement is the *what* and the specification is the *how*.

Specifications are written using github-flavored markdown.


### Second Example Requirement

_Requirement ID:_ r-2

_Requirement:_ Requirements describe what the software needs to do, and not how.


_Functional Specifications:_
Another specification goes here.


### Third Example Requirement Nested Id First Item

_Requirement ID:_ r-3-1

_Requirement:_ Requirements should be verifiable (e.g., testable).


### Fourth Example Requirement Nested Id Second Item

_Requirement ID:_ r-3-2

_Requirement:_ Requirements can be written using markdown.


## User Interface Mockups

TODO:

If you have user interface mockups, this is a good place to put them. One strategy is to include a sub-section for each screen, along with its own image file. Here are some examples:

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
