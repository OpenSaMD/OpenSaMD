<!--
Copyright (C) 2022 Radiotherapy AI Holdings Pty Ltd
Copyright (C) 2021-2022 OpenRegulatory (OpenReg GmbH)
This work is licensed under the Creative Commons Attribution 4.0 International
License. <http://creativecommons.org/licenses/by/4.0/>.

Original work by OpenRegulatory available at
<https://github.com/openregulatory/templates>
-->

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
{{device_manufacturer}}.

### Role of Company

{{device_manufacturer}} is a manufacturer of Medical Devices.

### Applicable Standards

| Standard                                             | Why Applicable?                                                    |
| ---------------------------------------------------- | ------------------------------------------------------------------ |
| Therapeutic Goods Act 1989                           | The Act for all Medical Devices Manufacturers in Australia         |
| Therapeutic Goods (Medical Devices) Regulations 2002 | The regulations for all Medical Devices Manufacturers in Australia |
| MDR (2017/745/                                       | Regulation for all Medical Device Manufacturers in the EU          |
| ISO 13485:2016                                       | QMS utilised to meet the TGA essential principles                  |
| ISO 14971:2019                                       | Risk management for medical devices                                |
| IEC 62304:2006                                       | Software development for medical devices                           |
| IEC 62366-1:2015                                     | Usability evaluation for medical devices                           |

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

<!-- > Describe what your company is about, specifically, its mission and things
> which are important for it. Maybe you're developing software for patients
> with a certain disease and your goal is to improve their lives. -->

{{device_manufacturer}} aims to use AI to save lives within radiotherapy. To
achieve this it has the goals to reduce treatment errors and improve treatment
efficacy while helping more patients be treated through efficiency gains.

### Quality Objectives

<!-- > Whatever policy you outlined above, now you need to make it measurable by
> defining objectives which can be tracked. Those objectives should not (only)
> refer to the quality of your devices but the quality of your QMS and the
> overall work of your organization. > Typical examples are: hiring excellence
> in staff, providing best-of-class device performance, high standards of
> customer satisfaction, etc. In a next step (see short-term goals), those are
> narrowed down to concrete measures like for example the monthly number of
> user complaints. -->

It is the objective of {{device_manufacturer}} to provide best-of-class device
performance while obtaining high standards of customer satisfaction.

Device performance is governed by the underlying algorithm as well as the
overall software quality.

When tracking the quality of the AI autocontouring software its results are
compared to health practitioner ground truth contours over a range of datasets
that have not been used for model training. These comparisons are undergone
utilising the following metrics:

- Hausdorff
- Surface and Volumetric Dice
- Four point health practitioner approval scale

Software quality is tracked through the following objectives:

- Minimisation of reported defects
- Software uptime
- Software maintainability

Customer satisfaction is tracked through user feedback. Various objectives
based on achieving customer satisfaction are:

- Timely support
- Software performance
- Ease of use and installation

### Short-Term Goals

<!-- > How does your team track its goals? Your auditors want to see how your
> quality objectives translate into your daily work. You should formulate
> strategic goals for your company that are somewhat related to your quality
> goals and which are tracked at least on an annual basis. Do you already have
> a goal-oriented system in place to track your team's work? Even better: align
> business and quality goals and describe your system here. -->

Software development goal tracking is managed through the GitHub issue system.
See <https://github.com/RadiotherapyAI/rai/issues>.

## 3. Roles

<!-- > Describe the roles of the people in your company. Typically this is done by
> drawing an organigram (you could use draw.io for that). Or, you just use a
> table like below. -->

| Role(s)               | People           |
| --------------------- | ---------------- |
| CEO                   | Simon Biggs      |
| QMO                   | Simon Biggs      |
| PRRC                  | Simon Biggs      |
| CTO                   | Simon Biggs      |
| Advisor               | Stuart Swerdloff |
| Regulatory Consultant | Dr Oliver Eidel  |
| Regulatory Consultant | Pierre Lonchampt |

All C-level roles are referred to as the Management. Management is generally
responsible to define responsibilities and authorities, to define and
communicate Quality Policy and Goals and to ensure that the whole organization
is oriented towards them.

<!-- > See ISO 13485, para. 5.1, para. 5.5.1 -->

The Quality Management Officer (QMO) is responsible to:

- ensure that processes needed for the company's quality management system are
  documented
- report to top management on the effectiveness of the quality management
  system and any need for improvement
- ensure the promotion of awareness of applicable regulatory requirements and
  QMS requirements throughout the organization.

<!-- > See ISO 13485, para. 5.1, para. 5.5.2 -->

Person Responsible for Regulatory Compliance (PRRC) Responsibilities of the
PRRC are in accordance with Art. 15 MDR as follows:

- Ensure (review / release) the conformity of the devices is appropriately
  checked in accordance with the QMS before a device is released (also see Art.
  10 Para. 9 MDR)
- Ensure (review / release) that the technical documentation and the EU
  declaration of conformity are drawn up and kept up-to-date for all medical
  devices (also see Art. 10 Para. 4 and Art. 6 MDR)
- Ensure (review / release) that obligations for post-market surveillance are
  complied with in accordance with Art. 10 Para. 10 MDR
- Ensure (review / release) that the reporting obligations of Articles 87 to 91
  MDR are fulfilled (FSCA / incidents, also see Art. 10 Para. 13 MDR)
- Ensure that, in the case of investigational devices, the statement referred
  to in Section 4.1 of Chapter II of Annex XV MDR is issued.

The PRRC shall not be subjected to Management instructions while carrying out
his/her responsibilities specified above. His/her tasks may be delegated to
other roles as long as it is ensured that final responsibility stays with the
PRRC. She or he has the power and authority to represent the company in the
scope of his/her responsibilities, e.g. in communicating with state
authorities.

Required qualification for this role:

- Fluent in English language
- Knowledge of the role and responsibilities of a 'Person Responsible for
  Regulatory Compliance' according to Art. 15 MDR
- Higher education degree in law, medicine, pharmacology or engineering OR:
  four years of professional experience in the fields of quality management and
  regulatory affairs
- At minimum one year of professional experience in the fields of quality
  management and regulatory affairs

## 4. Processes

<!-- > List all your SOPs here. This list is currently incomplete as many SOPs are
> company-specific. You will have to complete it yourself - good luck! -->

<!-- TODO: Automate this -->

| SOP                                                        | Process Category |
| ---------------------------------------------------------- | ---------------- |
| [](./capa/0-sop)                                           | Core             |
| [](./document-and-record-control/0-sop)                    | Core             |
| [](../2-techdoc/62304/sop-integrated-software-development) | Core             |
| [](./post-market-surveillance/0-sop)                       | Support          |
| [](./software-validation/0-sop)                            | Support          |
| [](./management-review/0-sop)                              |                  |
| [](./sop-product-certification-and-registration)           |                  |
| [](./purchasing/0-sop)                                     |                  |
| [](./sop-update-of-regulations)                            |                  |
| [](./human-resources/0-sop)                                |                  |
| [](../2-techdoc/62304/sop-change-management)               |                  |
| [](../2-techdoc/62304/sop-deployment)                      |                  |
| [](./sop-feedback-management)                              |                  |
| [](./vigilance/0-sop)                                      |                  |
| [](./sop-internal-audit)                                   |                  |
| [](../2-techdoc/62304/sop-software-problem-resolution)     |                  |
