<!--
Copyright (C) 2022 Radiotherapy AI Holdings Pty Ltd
Copyright (C) 2021-2022 OpenRegulatory (OpenReg GmbH)
This work is licensed under the Creative Commons Attribution 4.0 International
License. <http://creativecommons.org/licenses/by/4.0/>.

Original work by OpenRegulatory available at
<https://github.com/openregulatory/templates>
-->

# List of Hazard-Related Use Scenarios

## Mapping of Standard Requirements to Document Sections

| IEC 62366-1:2015 Section | Title                                                            | Document Section |
| ------------------------ | ---------------------------------------------------------------- | ---------------- |
| 5.4                      | Identify and describe Hazard-Related Use Scenarios               | 1                |
| 5.5                      | Select the Hazard-Related Use Scenarios for Summative Evaluation | 1                |

## Summary

The goal of the list of Hazard-Related Use Scenarios is to gather all Use Scenarios which could be associated
with a Hazard, e.g., if a user doesn't understand a certain feature of the app (bad design leading to poor
usability), then a Hazard could be encountered which could subsequently lead to a Hazardous Situation.

## 1. Hazard-Related Use Scenarios

> Fill out this list with Use Scenarios which could be Hazard-related. A good rule of thumb is to have 3-10
> scenarios, based on the risk profile of your software.
>
> Also, note that you should prefer to create a spreadsheet for this table (e.g., in Google Sheets) as putting a
> table in a document will surely lead to chaos. But then again, there's always a certain level of chaos in
> regulatory documentation.

| ID  | User Group | Description        | App State / Environment                               | Tasks                                                         | Acceptance Criteria                 |
| --- | ---------- | ------------------ | ----------------------------------------------------- | ------------------------------------------------------------- | ----------------------------------- |
| 1   | Physician  | Assess COVID score | 1) App is installed<br>2) App displays patient result | Understand COVID score and initiate further medical treatment | COVID score is understood correctly |
