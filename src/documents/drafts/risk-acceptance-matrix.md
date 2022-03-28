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

| Severity       | Definition and Examples                                       |
| -------------- | ------------------------------------------------------------- |
| S1: Negligible | Minor, reversible damage, e.g. delay of treatment             |
| S2: Marginal   | Minor, reversible damage with required medical intervention   |
| S3: Critical   | Major, irreversible damage with required medical intervention |

## Probability

| Probability  | Upper Limit | Lower Limit | Estimated Maximum Event Count |
| ------------ | ----------- | ----------- | ----------------------------- |
| P5: Certain  | 1           | 10^-2       | 10000000                      |
| P4: Likely   | 10^-2       | 10^-4       | 100000                        |
| P3: Possible | 10^-4       | 10^-6       | 1000                          |
| P2: Unlikely | 10^-6       | 10^-8       | 10                            |
| P1: Rare     | 10^-8       | 0           | 0                             |

## Risk Acceptance Matrix

| Probability  | S1: Negligible | S2: Marginal     | S3: Critical     | Estimated Maximum Event Count |
| ------------ | -------------- | ---------------- | ---------------- | ----------------------------- |
| P5: Certain  | acceptable     | **unacceptable** | **unacceptable** | 10000000                      |
| P4: Likely   | acceptable     | **unacceptable** | **unacceptable** | 100000                        |
| P3: Possible | acceptable     | acceptable       | **unacceptable** | 1000                          |
| P2: Unlikely | acceptable     | acceptable       | acceptable       | 10                            |
| P1: Rare     | acceptable     | acceptable       | acceptable       | 0                             |
