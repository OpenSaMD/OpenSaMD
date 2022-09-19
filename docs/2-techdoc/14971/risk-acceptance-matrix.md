<!--
This work is licensed under the Creative Commons Attribution 4.0 International
License:

    <http://creativecommons.org/licenses/by/4.0/>

Templates copyright OpenRegulatory. Originals available at:

    <https://openregulatory.com/templates/>

General content copyright Radiotherapy AI.
-->

# Failure Mode and Effects Analysis (FMEA): Risk Acceptance Matrix

This document defines under which circumstances risk are acceptable. It defines
probabilities and severities and each probability-severity combination is
either acceptable or not, as shown in the risk acceptance matrix at the bottom.

## Risk Policy

Radiotherapy AI's products should not cause more harm than undergoing the
process manually without AI assistance.

## Severity

| Severity       | Definition and Examples                                                  |
| -------------- | ------------------------------------------------------------------------ |
| S1: Negligible | Delay of treatment or clinically non-relevant protocol deviation         |
| S2: Minor      | Minor radiotherapy protocol deviation, non-patient identifying data leak |
| S3: Major      | Major radiotherapy protocol deviation, or patient identifying data leak  |
| S4: Critical   | Reportable radiotherapy mistreatment and/or incident                     |
| S5: Death      |                                                                          |

## Probability

| Probability           | Upper Limit | Lower Limit | Estimated Maximum Event Count |
| --------------------- | ----------- | ----------- | ----------------------------- |
| P6: Almost certain    | 1           | 10^-2       | 10000000                      |
| P5: Likely            | 10^-2       | 10^-4       | 100000                        |
| P4: Possible          | 10^-4       | 10^-6       | 1000                          |
| P3: Unlikely          | 10^-6       | 10^-8       | 10                            |
| P2: Rare              | 10^-8       | 10^-10      | 0                             |
| P1: Almost impossible | 10^-10      | 0           | 0                             |

## Risk Acceptance Matrix

| Probability           | S1: Negligible   | S2: Minor        | S3: Major        | S4: Critical     | S5: Death        | Estimated Maximum Event Count |
| --------------------- | ---------------- | ---------------- | ---------------- | ---------------- | ---------------- | ----------------------------- |
| P6: Almost certain    | **unacceptable** | **unacceptable** | **unacceptable** | **unacceptable** | **unacceptable** | 10000000                      |
| P5: Likely            | acceptable       | **unacceptable** | **unacceptable** | **unacceptable** | **unacceptable** | 100000                        |
| P4: Possible          | acceptable       | acceptable       | **unacceptable** | **unacceptable** | **unacceptable** | 1000                          |
| P3: Unlikely          | acceptable       | acceptable       | acceptable       | **unacceptable** | **unacceptable** | 10                            |
| P2: Rare              | acceptable       | acceptable       | acceptable       | acceptable       | **unacceptable** | 0                             |
| P1: Almost impossible | acceptable       | acceptable       | acceptable       | acceptable       | acceptable       | 0                             |
