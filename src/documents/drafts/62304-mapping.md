<!--
This work is licensed under the Creative Commons Attribution 4.0 International
License:

    <http://creativecommons.org/licenses/by/4.0/>

Templates copyright OpenRegulatory. Originals available at:

    <https://openregulatory.com/templates/>

General content copyright Radiotherapy AI.
-->

# IEC 62304:2006 Mapping of Requirements to Documents

This table maps all requirements of the IEC 62304:2006 (by section) to the relevant documents.

| Classes   | Section | Title                                                                  | Fulfilled in Document                                                                                          |
| --------- | ------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| (General) | 4.1     | Quality management system                                              | [](../released/quality-manual-policy-objectives)                                                                                     |
|           | 4.2     | Risk management                                                        | [](../released/sop-integrated-software-development)                                                            |
|           | 4.3     | Software Safety Classification                                         | [](../drafts/risk-management-report)                                                                                         |
|           | 4.4     | Legacy Software                                                        | (Not applicable)                                                                                               |
| A, B, C   | 5.1.1   | Software development plan                                              | [](../drafts/software-development-maintenance-plan)                                                            |
| A, B, C   | 5.1.2   | Keep software development plan update                                  | [](../released/sop-integrated-software-development)                                                            |
| A, B, C   | 5.1.3   | Software development plan reference to system design and development   | [](../drafts/software-development-maintenance-plan)                                                            |
| C         | 5.1.4   | Software development standards, methods and tool planning              | [](../drafts/software-development-maintenance-plan)                                                            |
| B, C      | 5.1.5   | Software integration and integration test planning                     | [](../drafts/software-development-maintenance-plan)                                                            |
| A, B, C   | 5.1.6   | Software verification planning                                         | [](../drafts/software-development-maintenance-plan)                                                            |
| A, B, C   | 5.1.7   | Software risk management planning                                      | [](../drafts/software-development-maintenance-plan)                                                            |
| A, B, C   | 5.1.8   | Documentation planning                                                 | [](../drafts/software-development-maintenance-plan)                                                            |
| A, B, C   | 5.1.9   | Software configuration management planning                             | [](../drafts/software-development-maintenance-plan)                                                            |
| B, C      | 5.1.10  | Supporting items to be controlled                                      | [](../drafts/software-development-maintenance-plan)                                                            |
| B, C      | 5.1.11  | Software configuration item control before verification                | [](../drafts/software-development-maintenance-plan)                                                            |
| B, C      | 5.1.12  | Identification and avoidance of common software defects                | [](../drafts/software-development-maintenance-plan)                                                            |
| A, B, C   | 5.2.1   | Define and document software requirements from system requirements     | [](../released/sop-integrated-software-development); Software Requirements List                                |
| A, B, C   | 5.2.2   | Software requirements content                                          | Software Requirements List                                                                                     |
| B, C      | 5.2.3   | Include risk control measures in software requirements                 | Software Requirements List                                                                                     |
| A, B, C   | 5.2.4   | Re-evaluate medical device risk analysis                               | [](../released/sop-integrated-software-development)                                                            |
| A, B, C   | 5.2.5   | Update requirements                                                    | [](../released/sop-integrated-software-development)                                                            |
| A, B, C   | 5.2.6   | Verify software requirements                                           | [](../released/sop-integrated-software-development); Checklist Software Requirements                           |
| B, C      | 5.3.1   | Transform software requirements into an architecture                   | [](../released/sop-integrated-software-development); (Software architecture diagrams, interface documentation) |
| B, C      | 5.3.2   | Develop an architecture for the interfaces of software items           | [](../released/sop-integrated-software-development); (Software architecture diagrams, interface documentation) |
| B, C      | 5.3.3   | Specify functional and performance requirements of SOUP item           | SOUP list                                                                                                      |
| B, C      | 5.3.4   | Specify system hardware and software required by SOUP item             | SOUP list                                                                                                      |
| C         | 5.3.5   | Identify segregation necessary for risk control                        | [](../released/sop-integrated-software-development)                                                            |
| B, C      | 5.3.6   | Verify software architecture                                           | [](../released/sop-integrated-software-development); Checklist Software Architecture                           |
| B, C      | 5.4.1   | Subdivide software into software units                                 | [](../released/sop-integrated-software-development); (Software architecture diagrams)                          |
| C         | 5.4.2   | Develop detailed design for each software unit                         | [](../released/sop-integrated-software-development)                                                            |
| C         | 5.4.3   | Develop detailed design for interfaces                                 | [](../released/sop-integrated-software-development)                                                            |
| C         | 5.4.4   | Verify detailed design                                                 | [](../released/sop-integrated-software-development)                                                            |
| A, B, C   | 5.5.1   | Implement each software unit                                           | [](../released/sop-integrated-software-development); (GitHub Pull Requests / GitLab Merge Requests)            |
| B, C      | 5.5.2   | Establish software unit verification process                           | [](../released/sop-integrated-software-development)                                                            |
| B, C      | 5.5.3   | Software unit acceptance criteria                                      | [](../released/sop-integrated-software-development)                                                            |
| C         | 5.5.4   | Additional software unit acceptance criteria                           | [](../released/sop-integrated-software-development)                                                            |
| B, C      | 5.5.5   | Software unit verification                                             | [](../released/sop-integrated-software-development); (CI/CD in GitHub Pull Requests / GitLab Merge Requests)   |
| B, C      | 5.6.1   | Integrate software units                                               | [](../released/sop-integrated-software-development); (Merge in GitHub / GitLab)                                |
| B, C      | 5.6.2   | Verify software integration                                            | [](../released/sop-integrated-software-development); (Merge in GitHub / GitLab)                                |
| B, C      | 5.6.3   | Software integration testing                                           | [](../released/sop-integrated-software-development); (Merge in GitHub / GitLab, CI/CD)                         |
| B, C      | 5.6.4   | Software integration testing content                                   | [](../released/sop-integrated-software-development); (CI/CD in GitHub Pull Requests / GitLab Merge Requests)   |
| B, C      | 5.6.5   | Evaluate software integration test procedures                          | [](../released/sop-integrated-software-development)                                                            |
| B, C      | 5.6.6   | Conduct regression tests                                               | [](../released/sop-integrated-software-development); (CI/CD in GitHub Pull Requests / GitLab Merge Requests)   |
| B, C      | 5.6.7   | Integration test record contents                                       | [](../released/sop-integrated-software-development); (CI/CD in GitHub Pull Requests / GitLab Merge Requests)   |
| B, C      | 5.6.8   | Use software problem resolution process                                | [](../released/sop-software-problem-resolution)                                                                                |
| A, B, C   | 5.7.3   | Retest after changes                                                   | [](../released/sop-integrated-software-development)                                                            |
| A, B, C   | 5.7.4   | Evaluate software system testing                                       | [](../released/sop-integrated-software-development); Software System Test Plan                                 |
| A, B, C   | 5.7.5   | Software system test record contents                                   | [](../released/sop-integrated-software-development); Software System Test Protocol                             |
| A, B, C   | 5.8.1   | Ensure software verification is complete                               | [](../released/sop-integrated-software-development); Checklist Software Release                                |
| A, B, C   | 5.8.2   | Document known residual anomalies                                      | [](../released/sop-integrated-software-development); (Release notes / changelog)                               |
| B, C      | 5.8.3   | Evaluate known residual anomalies                                      | [](../drafts/risk-table-fmea/index); (Release notes / changelog)                                                                        |
| A, B, C   | 5.8.4   | Document released versions                                             | [](../released/sop-integrated-software-development); (Release notes / changelog)                               |
| B, C      | 5.8.5   | Document how released software was created                             | [](../released/sop-integrated-software-development); (Release notes / changelog)                               |
| B, C      | 5.8.6   | Ensure activities and tasks are complete                               | [](../released/sop-integrated-software-development); Checklist Software Release                                |
| A, B, C   | 5.8.7   | Archive software                                                       | [](../released/sop-integrated-software-development); (Tagged commit in git)                                    |
| A, B, C   | 5.8.8   | Assure reliable delivery of released software                          | [](../released/sop-integrated-software-development)                                                            |
| A, B, C   | 6.1     | Establish software maintenance plan                                    | [](../drafts/software-development-maintenance-plan)                                                            |
| A, B, C   | 6.2.1.1 | Monitor feedback                                                       |                                                                                                                |
| A, B, C   | 6.2.1.2 | Document and evaluate feedback                                         |                                                                                                                |
| A, B, C   | 6.2.1.3 | Evaluate problem report's affects on safety                            | [](../released/sop-software-problem-resolution)                                                                                         |
| A, B, C   | 6.2.2   | Use software problem resolution process                                | [](../released/sop-software-problem-resolution)                                                                                         |
| A, B, C   | 6.2.3   | Analyse change requests                                                | [](../released/sop-change-management)                                                                                          |
| A, B, C   | 6.2.4   | Change request approval                                                | [](../released/sop-change-management)                                                                                          |
| A, B, C   | 6.2.5   | Communicate to users and regulators                                    | [](../released/sop-change-management)                                                                                          |
| A, B, C   | 6.3.1   | Use established process to implement modification                      | [](../released/sop-change-management)                                                                                          |
| A, B, C   | 6.3.2   | Re-release modified software system                                    | [](../released/sop-change-management)                                                                                          |
| B, C      | 7.1.1   | Identify software items that could contribute to a hazardous situation | [](../released/sop-integrated-software-development)                                                            |
| B, C      | 7.1.2   | Identify potential causes of contribution to a hazardous situation     | [](../released/sop-integrated-software-development)                                                            |
| B, C      | 7.1.3   | Evaluate published SOUP anomaly lists                                  | [](../released/sop-integrated-software-development)                                                            |
| B, C      | 7.1.4   | Document potential causes                                              | [](../released/sop-integrated-software-development)                                                            |
| B, C      | 7.2.1   | Define risk control measures                                           | [](../released/sop-integrated-software-development)                                                            |
| B, C      | 7.2.2   | Risk control measures implemented in software                          | [](../released/sop-integrated-software-development)                                                            |
| B, C      | 7.3.1   | Verify risk control measures                                           | [](../released/sop-integrated-software-development)                                                            |
|           | 7.3.2   | (Not used)                                                             |                                                                                                                |
| B, C      | 7.3.3   | Document traceability                                                  | [](../released/sop-integrated-software-development); Software Requirements List                                |
| A, B, C   | 7.4.1   | Analyse changes to medical device software with respect to safety      | [](../released/sop-change-management)                                                                                          |
| B, C      | 7.4.2   | Analyse impact of software changes on existing risk control measures   | [](../released/sop-change-management)                                                                                          |
| B, C      | 7.4.3   | Perform risk management activities based on analyses                   | [](../released/sop-change-management)                                                                                          |
| A, B, C   | 8.1.1   | Establish means to identify configuration items                        | [](../drafts/software-development-maintenance-plan)                                                            |
| A, B, C   | 8.1.2   | Identify SOUP                                                          | [](../released/sop-integrated-software-development)                                                            |
| A, B, C   | 8.1.3   | Identify system configuration documentation                            | [](../released/sop-integrated-software-development)                                                            |
| A, B, C   | 8.2.1   | Approve change requests                                                | [](../released/sop-change-management)                                                                                          |
| A, B, C   | 8.2.2   | Implement changes                                                      | [](../released/sop-change-management)                                                                                          |
| A, B, C   | 8.2.3   | Verify changes                                                         | [](../released/sop-change-management)                                                                                          |
| A, B, C   | 8.2.4   | Provide means for traceability of change                               | [](../released/sop-change-management)                                                                                          |
| A, B, C   | 8.3     | Configuration status accounting                                        | [](../drafts/software-development-maintenance-plan)                                                            |
| A, B, C   | 9.1     | Prepare problem reports                                                | [](../released/sop-software-problem-resolution)                                                                                |
| A, B, C   | 9.2     | Investigate the problem                                                | [](../released/sop-software-problem-resolution)                                                                                |
| A, B, C   | 9.3     | Advise relevant parties                                                | [](../released/sop-software-problem-resolution); SOP Incident Reporting                                                        |
| A, B, C   | 9.4     | Use change control process                                             | [](../released/sop-change-management)                                                                                          |
| A, B, C   | 9.5     | Maintain records                                                       | [](../released/sop-software-problem-resolution)                                                                                |
| A, B, C   | 9.6     | Analyse problems for trends                                            | [](../released/sop-software-problem-resolution)                                                                                |
| A, B, C   | 9.7     | Verify software problem resolution                                     | [](../released/sop-software-problem-resolution)                                                                                |
| A, B, C   | 9.8     | Test documentation contents                                            | [](../released/sop-integrated-software-development)                                                            |
