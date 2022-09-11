<!--
This work is licensed under the Creative Commons Attribution 4.0 International
License:

    <http://creativecommons.org/licenses/by/4.0/>

Templates copyright OpenRegulatory. Originals available at:

    <https://openregulatory.com/templates/>

General content copyright Radiotherapy AI.
-->

# Failure Mode and Effects Analysis (FMEA): Risk Table

| ISO 14971:2019 Section | Document Section                                   |
| ---------------------- | -------------------------------------------------- |
| 5.2                    | (all; entries about reasonably foreseeable misuse) |
| 5.4                    | 3                                                  |
| 5.5                    | 3, 4                                               |
| 6                      | 3                                                  |
| 7.1                    | 4                                                  |
| 7.2                    | 4                                                  |
| 7.3                    | 4                                                  |
| 7.5                    | 4                                                  |

| IEC 62366-1:2015 Section | Title                                                          | Document Section |
| ------------------------ | -------------------------------------------------------------- | ---------------- |
| 4.1.2                    | Risk Control as it relates to User Interface design            | 4                |
| 5.3                      | Identify known or foreseeable Hazards and Hazardous Situations | 1,3              |

This is a Failure Mode and Effects Analysis ([FMEA][wikipedia-fmea]) of the
device. It is separated into multiple sections:

- **Failure Modes** lists everything which can go wrong
- **Hazards and Analysis** lists everything (harms) which can subsequently
  happen, including an analysis of probability and severity
- The list of **Risk Control Measures** which contains all control measures
  which were implemented for risk reduction, either reducing probability or
  severity, or both.

## 1. Preliminary Hazards Analysis (PHA)

```{csv-table} Preliminary Hazards Analysis
---
file: preliminary-hazards-analysis.csv
widths: 5 20 20 10
---
```

## 2. Failure Modes

```{csv-table} Failure Modes
---
file: failure-modes.csv
widths: 5 20 5
---
```

## 3. Hazards and Analysis

```{csv-table} Hazards, Hazardous Situations, and Harm
---
file: hazard-to-harm.csv
widths: 3 10 3 20 3 10
---
```

```{csv-table} Analysis without risk controls
---
file: analysis-without-risk-controls.csv
---
```

```{csv-table} Analysis with external risk controls
---
file: analysis-with-external-controls.csv
---
```

```{csv-table} Analysis with external and internal risk controls
---
file: analysis-with-all-controls.csv
---
```

## 4. Risk Control Measures

```{csv-table} Risk Control Measures
---
file: risk-control-measures.csv
widths: 3 30 10 5 5
---
```

[wikipedia-fmea]: https://en.wikipedia.org/wiki/Failure_mode_and_effects_analysis
