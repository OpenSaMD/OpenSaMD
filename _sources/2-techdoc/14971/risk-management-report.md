<!--
Copyright (C) 2022 Radiotherapy AI Holdings Pty Ltd
Copyright (C) 2021-2022 OpenRegulatory (OpenReg GmbH)
This work is licensed under the Creative Commons Attribution 4.0 International
License. <http://creativecommons.org/licenses/by/4.0/>.

Original work by OpenRegulatory available at
<https://github.com/openregulatory/templates>
-->

# Risk Management Report

The Risk Management Report contains the output and summary of risk management
activities. The general planning and methods are described in the Risk
Management plan, while the actual risks are listed and analysed in the Risk
Table.

The process and stages of risk analysis are described in the SOP Integrated
Software Development.

## Mapping of Standard Requirements to Document Sections

| ISO 14971:2019 Section                | Document Section             |
| ------------------------------------- | ---------------------------- |
| 4.5 Risk management file              | (all)                        |
| 7.4 Benefit-risk analysis             | 6                            |
| 7.6 Completeness of risk control      | (by review of this document) |
| 8 Evaluation of overall residual risk | 3, 5                         |
| 9 Risk management review              | (all)                        |

## 1. Relevant Processes and Documents

- [](../62304/sop-integrated-software-development)
- [](./risk-management-plan)
- [](./risk-acceptance-matrix)
- [](./risk-table-fmea/index)

## 2. Risk Analysis

<!-- > The general idea about this section is that you simply summarize the amount
> of stuff you added to your Risk Table (a separate document). -->

### 2.1 Preliminary Hazards Analysis

`8` hazards were identified based on the Intended Use and Usability Tests. They
were further analysed in the Risk Table.

### 2.2 Failure Modes

`3` failure modes of software systems were identified. They were further analysed
in the Risk Table.

### 2.3 Failure Mode and Effects Analysis (FMEA)

All preliminary hazards and potential failure modes of the software were
analysed. In total, 8 were identified. The hazardous situation(s) and harm(s)
which they could lead to were analysed, including intermediate probabilities
(p1 and p2).

## 3. Risk Control Measures

Risks were reduced as far as possible (AFAP). If a risk was classified as
"unacceptable" based on the Risk Table, Risk Control Measures were implemented.

The following categories of Risk Control Measures were implemented in priority
as listed below:

1. Inherent safety by design
2. Protective measures
3. Information for safety

In total, `4` external risk control measures were implemented and `2` internal
risk control measures were implemented.

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

<!-- > If you don't have unacceptable risks (more likely), use this section: -->

After Risk Control Measures, no unacceptable risks remained. The software
therefore fulfils the specifications of the defined risk policy and is safe. A
Benefit-Risk Assessment is not required.

<!-- > If you still have unacceptable risks, use this section:

After Risk Control Measures, *\<no. of unacceptable risks\>* unacceptable risks
remained. They will be further assessed in the Benefit-Risk Assessment below. -->

<!-- > Optionally, mention here your device's software safety classification
> according to IEC 62304, resulting from the worst possible risks found above. -->

While the software system can contribute to hazardous situations, none of those
result in unacceptable risk after consideration of risk control measures
external to the software system. Therefore, the software system is classified
as software safety class A.

<!-- ## 6. Benefit-Risk Assessment

> Only use this whole section (Risk-Benefit Assessment) if you have
> unacceptable risks.

The *\<no. of unacceptable risks\>* remaining unacceptable risks are compared
to the benefits resulting from the Clinical Evaluation Report.

The benefits are as follows:

*\<Copy-paste benefits from Clinical Evaluation\>*

> Add a conclusion on whether the benefits outweigh the risks

Weighing the benefits against the risks, we conclude that...

## 7. Overall Residual Risk

> Take a look at your risk mitigating measures and assess whether the
> combination of them could lead to a risk that has not been taken care of yet,
> e.g., if one mitigation serves two or more risks at once.

The overall residual risk is estimated to have a probability of *\<probability
of residual risk\>* and a severity of *\<severity of residual risk\>*.
According to the Risk Acceptance Matrix the overall residual risk is assessed
as *\<acceptable\>*. -->
