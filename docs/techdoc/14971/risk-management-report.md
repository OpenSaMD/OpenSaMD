<!--
This work is licensed under the Creative Commons Attribution 4.0 International
License:

    <http://creativecommons.org/licenses/by/4.0/>

Templates copyright OpenRegulatory. Originals available at:

    <https://openregulatory.com/templates/>

General content copyright Radiotherapy AI.
-->

# Risk Management Report

The Risk Management Report contains the output and summary of risk management activities. The general planning
and methods are described in the Risk Management plan, while the actual risks are listed and analyzed in the
Risk Table.

The process and stages of risk analysis are described in the SOP Integrated Software Development.

## Mapping of Standard Requirements to Document Sections

| ISO 14971:2019 Section                | Document Section             |
| ------------------------------------- | ---------------------------- |
| 4.5 Risk management file              | (all)                        |
| 7.4 Benefit-risk analysis             | 6                            |
| 7.6 Completeness of risk control      | (by review of this document) |
| 8 Evaluation of overall residual risk | 3, 5                         |
| 9 Risk management review              | (all)                        |

## 1. Relevant Processes and Documents

- [](../released/sop-integrated-software-development)
- [](../drafts/risk-management-plan)
- [](../drafts/risk-acceptance-matrix)
- [](../drafts/risk-table-fmea/index)

## 2. Risk Analysis

### 2.1 Preliminary Hazards Analysis

8 hazards were identified based on the Intended Use and Usability Tests. They
were further analysed in the Risk Table.

### 2.2 Failure Modes

3 failure modes of software systems were identified. They were further analysed
in the Risk Table.

### 2.3 Failure Mode and Effects Analysis (FMEA)

All preliminary hazards and potential failure modes of the software were
analysed. In total, 8 were identified. The hazardous situation(s) and harm(s)
which they could lead to were analysed, including intermediate probabilities
(p1 and p2).

## 3. Risk Control Measures

Risks were reduces as low as reasonably possible (ALARP). If a risk was
classified as "unacceptable" based on the Risk Table, Risk Control Measures
were implemented. Potential categories of Internal Risk Control Measures are
"inherent safety by design", "protective measures" and "information for
safety". Potential categories for External Risk Control Measures are
"hardware", "independent software system", and "health care procedures". In
total, 4 were implemented. Two of these were external protective measures that
were identified. No hazardous situation resulted in unacceptable risk after the
consideration of the two external risk control measures.

Two remaining internal risk control measures were implemented following the
ALARP principle.

## 4. Risk Matrix

After implementation and verification of all Risk Control Measures, the count
of risks in the Risk Acceptance Matrix was as follows:

| Probability           | S1: Negligible      | S2: Minor           | S3: Major           | S4: Critical        | S5: Death           | Estimated Maximum Event Count |
| --------------------- | ------------------- | ------------------- | ------------------- | ------------------- | ------------------- | ----------------------------- |
| P6: Almost certain    | **unacceptable**: 0 | **unacceptable**: 0 | **unacceptable**: 0 | **unacceptable**: 0 | **unacceptable**: 0 | 10000000                      |
| P5: Likely            | acceptable: 0       | **unacceptable**: 0 | **unacceptable**: 0 | **unacceptable**: 0 | **unacceptable**: 0 | 100000                        |
| P4: Possible          | acceptable: 1       | acceptable: 0       | **unacceptable**: 0 | **unacceptable**: 0 | **unacceptable**: 0 | 1000                          |
| P3: Unlikely          | acceptable: 0       | acceptable: 1       | acceptable: 0       | **unacceptable**: 0 | **unacceptable**: 0 | 10                            |
| P2: Rare              | acceptable: 0       | acceptable: 0       | acceptable: 0       | acceptable: 0       | **unacceptable**: 0 | 0                             |
| P1: Almost impossible | acceptable: 0       | acceptable: 1       | acceptable: 1       | acceptable: 1       | acceptable: 3       | 0                             |

## 5. Summary of Risks and Unacceptable Risks

After Risk Control Measures, no unacceptable risks remained. The software
therefore fulfils the specifications of the defined risk policy and is safe. A
Benefit-Risk Assessment is not required.

While the software system can contribute to hazardous situations, none of those
result in unacceptable risk after consideration of risk control measures
external to the software system. Therefore, the software system is classified
as software safety class A.
