# Quality Manual, Policy and Objectives

| ISO 13485:2016 Section | Document Section |
| ---------------------- | ---------------- |
| 4.1.1                  | 1.               |
| 4.1.2                  | 4.               |
| 4.2.1 b)               | (All)            |
| 4.2.2                  | (All)            |
| 5.3                    | 2.               |
| 5.4.1                  | 2.               |

## Summary

The Quality Manual describes the scope of the Quality Management System, its
documented procedures and a description of their interactions.

## 1. Scope

The QMS described in this Quality Manual applies to all products of
{{device.manufacturer}}.

### Role of Company

{{device.manufacturer}} is a manufacturer of Medical Devices.

### Applicable Standards

| Standard         | Why Applicable?                                   |
| ---------------- | ------------------------------------------------- |
| ISO 13485:2016   | QMS utilised to meet the TGA essential principles |
| ISO 14971:2019   | Risk management for medical devices               |
| IEC 62304:2006   | Software development for medical devices          |
| IEC 62366-1:2015 | Usability evaluation for medical devices          |

### Exclusions

The following sections of ISO 13485:2016 will be excluded due to the product
being stand-alone software:

- 6.4.2 Contamination control
- 7.5.2 Cleanliness of product
- 7.5.5 Particular requirements for sterile medical devices
- 7.5.7 Particular requirements for validation of processes for sterilization
  and sterile barrier systems
- 7.5.9.2 Particular requirements for implantable medical devices

## 2. Quality Policy & Objectives

### Quality Policy

{{device.manufacturer}} aims to make AI assisted radiotherapy cancer treatments
accessible to all. With the goals to reduce treatment errors while improving
overall treatment efficacy and efficiency.

### Quality Objectives

When tracking the quality of the AI autocontouring software its
results are compared to health practitioner ground truth contours. These
comparisons are undergone utilising the following metrics:

- Hausdorff
- Surface and Volumetric Dice
- Four point health practitioner approval scale

## 3. Roles

| Role(s)                               | People       |
| ------------------------------------- | ------------ |
| CEO, QMO, CTO, CPO, Software Engineer | Simon Biggs  |
| Regulatory Consultant                 | Oliver Eidel |

All C-level roles are referred to as the Management. Management is generally
responsible to define responsibilities and authorities, to define and
communicate Quality Policy and Goals and to ensure that the whole organization
is oriented towards them.

> See ISO 13485, para. 5.1, para. 5.5.1

The Quality Management Officer (QMO) is responsible to:

- ensure that processes needed for the company’s quality management system are
  documented
- report to top management on the effectiveness of the quality management
  system and any need for improvement
- ensure the promotion of awareness of applicable regulatory requirements and
  QMS requirements throughout the organization.

> See ISO 13485, para. 5.1, para. 5.5.2

## 4. Processes

| SOP                                  | Process Category |
| ------------------------------------ | ---------------- |
| SOP Corrective and Preventive Action | Core             |
| SOP Document and Record Control      | Core             |
| SOP Integrated Software Development  | Core             |
| SOP Post-Market Surveillance         | Support          |
| SOP Software Validation              | Support          |

<!-- TODO: Look into filling in the above table based on the contents of a 'SOP' directory -->

## Document Approval

| Activity | Date       | Role                  | Name             | Initials |
| -------- | ---------- | --------------------- | ---------------- | -------- |
| Creation | 2022-02-28 | CEO                   | Simon Biggs      | SB       |
| Review   | 2022-0 | Regulatory Consultant | Dr. Oliver Eidel |        |
| Approval | 2022-0 | CEO                   | Simon Biggs      |        |
