<!--
Copyright (C) 2022 Radiotherapy AI Holdings Pty Ltd
Copyright (C) 2021-2022 OpenRegulatory (OpenReg GmbH)
This work is licensed under the Creative Commons Attribution 4.0 International
License. <http://creativecommons.org/licenses/by/4.0/>.

Original work by OpenRegulatory available at
<https://github.com/openregulatory/templates>
-->

# Change Evaluation List

| Regulation / Guidance                                             | Document Section |
| ----------------------------------------------------------------- | ---------------- |
| Medical Device Directive, Annex II<br>Section 3.4 and Section 4.4 | All              |
| Medical Device Regulation, Annex IX<br>Chapter II Section 4.10    | All              |
| MDCG Guidance Document 2020-03                                    | All              |
| EK-Med 3.9 B31                                                    | All              |

## Summary:

This list is used to document the evaluation of all regular change requests according to the company's change
management process.

## Evaluation of Product Changes

> Disclaimer for Use #1: You may want to separate your lists for product and organizational changes, as you
> should release a new list for every product version. This is to separately identify all changes related to
> that specific version. Each product version list should ideally be attached to the respective technical
> documentation file.

> Disclaimer for Use #2: If any of the below mentioned categories are answered with YES, this indicates that
> your change must be classified as significant.

> Disclaimer for Use #3: In the example content filled into the table below, "PCR" stands for "Product Change
> Request" and "OCR" stands for "Organization Change Request".

**Please note:**

- YES in the first two categories (intended use / essential requirements / GSPR) always leads to a significant
  change.
- If the device is modified (a) to correct an error, for which there is a safety risk to the patient if the
  error is not corrected or (b) as part of field safety corrective actions for an incident, the change is
  discussed with the Notified Body to determine the significance of the change. If no Notified Body was
  involved in the conformity assessment process of the device, the change is treated as a significant change.

| Evaluation Categories                                                                                                                                                                                                                      |                                                                              |                                                                |       |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------- | -------------------------------------------------------------- | ----- |
| **Change Request ID**                                                                                                                                                                                                                      | #PCR01                                                                       | #PCR02                                                         | (...) |
| **Change Request Description**                                                                                                                                                                                                             | Performance update of machine learning algorithm model                       | Additional integrability of device with new clinical IT-system |       |
| **Overall Evaluation Outcome**                                                                                                                                                                                                             | **Not significant**                                                          | **Significant**                                                |       |
| Does the change alter specifications provided in the Intended Use?<br>(Chart A of MDCG 2020-03, e.g. new user or patient population)                                                                                                       | No                                                                           | No                                                             |       |
| Does the change affect conformity with the Essential Requirements (MDD) / General Safety and Performance Requirements (MDR)?<br>(EK-Med 3.9 B31, Section 5.1)                                                                              | No                                                                           | No                                                             |       |
| Does change implementation require further clinical or usability data to support safety and performance?<br>(Chart B of MDCG 2020-03)                                                                                                      | No, but internal validation showed that performance on same metrics improved | Yes                                                            |       |
| Do new risks require risk control measures or are existing risks negatively affected?<br>(Chart B of MDCG 2020-03)                                                                                                                         | No                                                                           | Yes                                                            |       |
| Does the change alter built-in control mechanisms or alarms? (Chart B of MDCG 2020-03)                                                                                                                                                     | No                                                                           | No                                                             |       |
| Does the change modify an operating principle or sources of energy?<br>(Chart B of MDCG 2020-03)                                                                                                                                           | No                                                                           | No                                                             |       |
| Does the change introduce a new or major change of the operating system or of any component?<br>(Chart C of MDCG 2020-03, e.g. major SOUP update)                                                                                          | No                                                                           | No                                                             |       |
| Does the change introduce a new or modified architecture or database structure, change of an algorithm? (Chart C of MDCG 2020-03, e.g. changes to prediction principle of an algorithm model)                                              | No, same prediction model                                                    | No                                                             |       |
| Does the change replace previously required user input by a closed-loop algorithm?<br>(Chart C of MDCG 2020-03)                                                                                                                            | No                                                                           | No                                                             |       |
| Does the change introduce a new diagnostic or therapeutic feature, or new channel of interoperability?<br>(Chart C of MDCG 2020-03)                                                                                                        | No                                                                           | Yes, new channel of interoperability                           |       |
| Does the change introduce a new user interface or presentation of data? (Chart C of MDCG 2020-03)                                                                                                                                          | No                                                                           | No                                                             |       |
| Does change implementation involve changes in critical suppliers?<br>(Chart D of MDCG 2020-03)                                                                                                                                             | No                                                                           | No                                                             |       |
| Does the change impact the way medical data is read or interpreted by the user, such that the treatment or diagnosis of the patient may be altered when compared to the previous version of the software?<br>(EK-Med 3.9 B31, Section 5.4) | Yes, but only improved accuracy in supported diagnosis                       | No                                                             |       |

## Evaluation of Organizational Changes

Please note: YES in the first two categories (essential requirements / GSPR) always leads to a significant
change.

| Evaluation Categories                                                                                                                                                                                                                                                                                                        |                                    |                                                                        |       |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- | ---------------------------------------------------------------------- | ----- |
| **Change Request ID**                                                                                                                                                                                                                                                                                                        | #OCR1                              | #OCR2                                                                  | (...) |
| **Change Request Description**                                                                                                                                                                                                                                                                                               | Change of Company Business Address | Adding a new compliance process to comply with anti-bribery provisions |       |
| **Overall Evaluation Outcome**                                                                                                                                                                                                                                                                                               | **Significant**                    | **Not significant**                                                    |       |
| Does the change affect QMS conformity with the Essential Requirements (MDD) / General Safety and Performance Requirements (MDR)? (EK-Med 3.9 B31, Section 5.2)                                                                                                                                                               | No                                 | No                                                                     |       |
| Does the change affect product conformity with the Essential Requirements (MDD) / General Safety and Performance Requirements (MDR) or the approved type / design?<br>(EK-Med 3.9 B31, Section 5.2)                                                                                                                          | No                                 | No                                                                     |       |
| Does the change relate to manufacturing processes, technologies, facility or equipment in a way that could impact product safety and performance? (EK-Med 3.9 B31, Section 5.2)                                                                                                                                              | No                                 | No                                                                     |       |
| Does the change affect the location of the company's activities?<br>(EK-Med 3.9 B31, Section 5.2)                                                                                                                                                                                                                            | Yes                                | No                                                                     |       |
| Does change implementation involve changes in critical suppliers?<br>(Chart D of MDCG 2020-03; EK-Med 3.9 B31, Section 5.2)                                                                                                                                                                                                  | No                                 | No                                                                     |       |
| Does the change affect the arrangements implemented to achieve continued compliance of the QMS with the relevant harmonized standards and/or MDD/MDR requirements (e.g. design verification, design validation, organizational structure, process interaction, quality control procedures)?<br>(EK-Med 3.9 B31, Section 5.2) | No                                 | No                                                                     |       |

> Based on the linked guidance documents, examples for non-significant changes are:
>
> - a software change that only introduces non-therapeutic and/or non-diagnostic features such as printing,
>   faxing, improved image clarity, reporting format or additional language support
> - a software change that only modifies the appearance of the user interface with negligible risk of
>   impacting the diagnosis or therapy delivered to the patient
> - a software change only intended to correct an inadvertent logic error that does not pose a safety risk and
>   brings the system back into specification
> - a software change that consists only of tightening of design specifications within specified tolerances
>   and where there is no creation of new features
> - changes to labelling to include additional languages required in other regulatory jurisdictions
> - minor changes to clarify the existing wording of warnings and precautions. However, in the case where
>   these changes add or remove a contraindication, or remove a warning or precaution, the Notified Body shall
>   be involved.

> Based on the linked guidance documents, examples for significant changes are:
>
> - an alteration in software that modifies an algorithm impacting the diagnosis or the therapy delivered
> - introduction or removal of a new alarm function from the software such that a response to the new
>   configuration may change the treatment of the patient in comparison to the previous version of the
>   software
> - medical data is presented in a new format, new dimension or new measuring unit.
