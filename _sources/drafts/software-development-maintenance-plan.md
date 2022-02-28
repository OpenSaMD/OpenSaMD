# Software Development and Maintenance Plan

This document summarizes development and maintenance activities for
Radiotherapy AI Contour Recommendations `v0.1.17`.

## Mapping of Standard Requirements to Document Sections

| ISO 13485:2016 Section                | Document Section |
| ------------------------------------- | ---------------- |
| 7.3.2 Design and Development Planning | 1, 2, 3, 7       |

| Classes | IEC 62304:2006 Section                                                     | Document Section |
| ------- | -------------------------------------------------------------------------- | ---------------- |
| A, B, C | 4.4.2 Risk Management Activities                                           | 1                |
| A, B, C | 5.1.1 a) (Processes)                                                       | 1                |
| A, B, C | 5.1.1 b) (Deliverables)                                                    | 1                |
| A, B, C | 5.1.1 c) (Traceability)                                                    | 1                |
| A, B, C | 5.1.1 d) (Configuration and Change Management)                             | 1, 5             |
| A, B, C | 5.1.1 e) (Problem Resolution)                                              | 1                |
| A, B, C | 5.1.2 Keep Software Development Plan Updated                               | 1                |
| A, B, C | 5.1.3 Software Development Plan Reference to System Design and Development | 2                |
| C       | 5.1.4 Software Development Standards, Methods and Tools Planning           |                  |
| B, C    | 5.1.5 Software Integration and Integration Test Planning                   | 3, 8             |
| A, B, C | 5.1.6 Software Verification Planning                                       | 7                |
| A, B, C | 5.1.7 Software Risk Management Planning                                    | 1                |
| A, B, C | 5.1.8 Documentation Planning                                               | 6                |
| A, B, C | 5.1.9 Software Configuration Management Planning                           | 5                |
| B, C    | 5.1.10 Supporting Items to be Controlled                                   | 5                |
| B, C    | 5.1.11 Software Configuration Item Control Before Verification             | 5                |
| B, C    | 5.1.12 Identification and Avoidance of Common Software Defects             | 4                |
| A, B, C | 6.1 Software Maintenance Plan.                                             | 9                |

## 1 Relevant Processes and Documents

Please see the relevant processes for the following activities:

- Risk management activities incl. SOUP risks: SOP Integrated Software Development
- Problem resolution: SOP Problem Resolution
- Software development incl. deliverables, traceability, regular update of software development plan: SOP
  Integrated Software Development
- Change management: SOP Change Management
- SOUP List
- SOP Usability Engineering

## 2. Required Resources

### 2.1 Team

| Role                                                         | Count | Names       |
| ------------------------------------------------------------ | ----- | ----------- |
| CEO, Full-stack developer, Data Scientist, Medical Physicist | 1     | Simon Biggs |

### 2.2 Software

<!--
  TODO: Describe your device's software safety class according to IEC 62304 and
  your reasoning behind the classification.
-->

#### Programming Languages

<!--
  TODO: Propagate these values into the data *.yml directory, inheriting from
  yarn.lock for TypeScript and pyproject for Python.
-->

| System                     | Name       | Version |
| -------------------------- | ---------- | ------- |
| Cloud container instances  | Python     | 3.9     |
| Local DICOM and app server | Python     | 3.9     |
| Local frontend dashboard   | TypeScript | 4.3     |

#### Development Software

| Name   | Version |
| ------ | ------- |
| VSCode | >= 1.64 |

### 2.3 System Requirement / Target Runtime

| System                     | Name     | Version |
| -------------------------- | -------- | ------- |
| Cloud container instances  | CPython  | 3.9     |
| Local DICOM and app server | CPython  | 3.9     |
| Local frontend dashboard   | Electron | 15.0    |

Minimum system requirements for local systems:

- Consumer grade single-core CPU
- 2 GB of RAM
- 1 MBit/s up- and downlink
- 20GB SSD storage

<!--
  TODO: Consider pulling these values from the kubernetes definition files.
-->

Minimum system requirements for `convert` cloud container:

- Server-grade single-core CPU
- 10 GB of RAM
- 1 GBit/s up- and downlink
- 20GB SSD storage

Minimum system requirements for `predict` cloud container:

- Server-grade single-core CPU
- NVIDIA GPU with 16 GB of VRAM
- 12 GB of RAM
- 1 GBit/s up- and downlink
- 20GB SSD storage

Minimum system requirements for `api` cloud container:

- Server-grade single-core CPU
- 512 MiB of RAM
- 1 GBit/s up- and downlink
- 20GB SSD storage

## 3 Design Phases

<!-- TODO: Read ISO i3485 (or is it 62304)? To see what is meant by design phases here -->

> The 13485 requires you to specify "Design Phases". Here are some suggestions which you could use.

| Title          | Date | Description |
| -------------- | ---- | ----------- |
| Specification  |      |             |
| Implementation |      |             |
| Testing        |      |             |
| Validation     |      |             |
| Release        |      |             |

## 4 Avoiding Common Software Defects Based on Selected Programming Technology

<!-- TODO -->

> Discuss how your selected programming technology may introduce risks and how you plan to avoid them. With
> modern, dynamically-typed languages, an obvious risk is that you encounter runtime exceptions. So you could
> argue that your test coverage is great and compensates for that. You could also link to your risk analysis
> here if you analyse those risks further.

## 5 Configuration Management and Version Control

git is used as version control software. All source code and build files are
committed to version control

When implementing software requirements, developers create a new branch
starting at `main`. During development, developers may create intermediate
commits on this development branch.

When implementation is completed, a new merge commit to `main` is created.

**This is also the activity which constitutes integration of software units.**

For each release, the goal is to be able to uniquely identify it and retrieve
all relevant files (code, configuration files like build scripts, SOUPs, etc.)
at any time in the future.

When a new software version is released, its commit is tagged in git. The tag
is constructed by adhering to semver ([semver.org](https://semver.org)) 2.0.0
which results in a version of format MAJOR.MINOR.PATCH, e.g. 1.0.0.

## 6 Documentation Activities

All public functions will be documented through doc strings or comments.

## 7 Verification Activities

<!-- TODO: Add in code review here when the software development team is > 1 -->

For each commit there is a pre-commit check which verifies that:

- All code ad-hears to the black style guide
- Imports are appropriately organised
- Jupyter notebook outputs are not committed
- TOML files are valid

For each pull request, there are automated checks within GitHub actions which
check the items described within **8 Software System Test Activities**.

Either manual testing is undergone or new automated tests are written to verify
that the current code changes fulfil the software requirements.

## 8 Software System Test Activities

For every pull request the following automated GitHub actions based system
tests are undergone:

- Python and Typescript unit and integration testing suites pass
- Python and Typescript linting passes
- Typescript type checker passes
- Python mypy type checker passes

## 9 Maintenance Activities

SOUP issue trackers are checked at least once every 6 months. The verification
date is updated in the SOUP list accordingly.
