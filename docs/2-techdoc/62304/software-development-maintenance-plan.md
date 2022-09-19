<!--
This work is licensed under the Creative Commons Attribution 4.0 International
License:

    <http://creativecommons.org/licenses/by/4.0/>

Templates copyright OpenRegulatory. Originals available at:

    <https://openregulatory.com/templates/>

General content copyright Radiotherapy AI.
-->

# Software Development and Maintenance Plan

This document summarizes development and maintenance activities for
{{device_name}} {{device_version}}.

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

- Risk management activities incl. SOUP risks:
  [](./sop-integrated-software-development)
- Problem resolution: [](./sop-software-problem-resolution)
- Software development incl. deliverables, traceability, regular update of
  software development plan: [](./sop-integrated-software-development)
- Change management: [](./sop-change-management)
- SOUP List
- SOP Usability Engineering

## 2. Required Resources

### 2.1 Team

| Role                                              | Count | Names       |
| ------------------------------------------------- | ----- | ----------- |
| CEO, Developer, Data Scientist, Medical Physicist | 1     | Simon Biggs |

### 2.2 Software

<!-- Describe your device's software safety class according to IEC 62304 and your
reasoning behind the classification. -->

While the software system can contribute to hazardous situations, none of those
result in unacceptable risk after consideration of risk control measures
external to the software system. Therefore, the software system is classified
as software safety class A. The (external) risk control measures include:

- The contour data is provided to an independent software treatment planning
  system where that independent software is utilised for refinement and
  approval.
- Contour refinement is undergone by a relevant qualified health practitioner.
- The subsequent refined contours are then reviewed by at least one other
  independent relevant qualified health practitioner. Generally however the
  whole plan, including the contours, goes through multiple independent
  reviewers before being utilised for treatment.

#### Programming Languages

<!-- > List the languages you’ll be using, including compiler and language versions. -->

| System                          | Name   | Version |
| ------------------------------- | ------ | ------- |
| Local DICOM server and ML model | Python | 3.9     |

#### Development Software

<!-- > List software used to support development, e.g., IDEs. -->

| Name   | Version |
| ------ | ------- |
| VSCode | >= 1.64 |

### 2.3 System Requirement / Target Runtime

<!-- > List your target runtime(s). -->

| System                          | Name    | Version |
| ------------------------------- | ------- | ------- |
| Local DICOM server and ML model | CPython | 3.9     |

<!-- > Specify system requirements, e.g., the minimum specifications of the server /
> compute instance you'll be running your software on -->

Minimum system requirements:

- Consumer grade CPU
- 4 GB of RAM
- 100 GB SSD storage

Additional recommended system requirements:

- A CUDA enabled NVIDIA GPU

## 3 Design Phases

<!-- > The 13485 requires you to specify "Design Phases". Here are some suggestions
> which you could use. -->

The design phases and the corresponding review and verification requirements
are detailed within [](../released/sop-integrated-software-development.md).

## 4 Avoiding Common Software Defects Based on Selected Programming Technology

<!-- > Discuss how your selected programming technology may introduce risks and how
> you plan to avoid them. With modern, dynamically-typed languages, an obvious
> risk is that you encounter runtime exceptions. So you could argue that your
> test coverage is great and compensates for that. You could also link to your
> risk analysis here if you analyse those risks further. -->

Python is a dynamically typed language, however, modern Python enables strict
type checking using Microsoft's PyRight and PyLance tools. These type checkers
are activated and run on strict mode. These are activated within the
development environment and within the continuous integration suite.

## 5 Configuration Management and Version Control

<!-- > Describe which version control software you're using (probably git, like all
> human beings on this planet right now, except enterprise developers). Also
> describe your branching model, i.e., how your developers create branches
> during development, how you name them and how you merge them (pull requests?
> merge commits? squash before?). Your code review will be described in the
> next section.
>
> Importantly, describe which things (code, build files, etc.) are put in
> version control. Describe how you name versions and how you tag them. Your
> goal should be that you can retrieve an old version and build it. Why?
> Something with a newer version may go wrong (harm patients) and you may need
> to roll back. -->

`git` is used as version control software. All source code and build files are
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

<!-- > Describe your policy on what should be documented while you develop software.
> Maybe you want to require your developers to document all methods which are
> private. Maybe you want to keep an up-to-date software architecture diagram
> in the repository, etc. -->

All public functions will be documented through doc strings or comments.

## 7 Verification Activities

<!-- > Describe verification activities, e.g. code review. -->

For each commit there is a pre-commit check which verifies that:

- All code adheres to the black style guide
- Imports are appropriately organised
- Jupyter notebook outputs are not committed
- TOML files are valid

For each pull request, there are automated checks within GitHub actions which
check the items described within [](software-tests).

Either manual testing is undergone or new automated tests are written to verify
that the current code changes fulfil the software requirements.

All PRs are to undergo code review before merging.

(software-tests)=

## 8 Software System Test Activities

<!-- > Describe software system test activities. This could be continuous
> integration which is triggered by opening a pull request (e.g. Travis CI,
> Circle CI). Describe what is tested and how that automated system works. -->

For every pull request the following automated GitHub actions based system
tests are undergone:

- Python unit and integration testing suites with pytest
- Python linting with pylint
- Python pyright type checker

## 9 Validation Activities

Validation is carried out as formative and summative usability evaluation as
described in the software development process. A usability evaluation file
(plan, protocol and report) will be prepared.

## 10 Maintenance Activities

<!-- > Describe how often you check SOUP issue trackers and how you document them. -->

SOUP issue trackers are checked at least once every 6 months. The verification
date is updated in the SOUP list accordingly.
