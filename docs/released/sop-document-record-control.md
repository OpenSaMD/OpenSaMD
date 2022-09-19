<!--
This work is licensed under the Creative Commons Attribution 4.0 International
License:

    <http://creativecommons.org/licenses/by/4.0/>

Templates copyright OpenRegulatory. Originals available at:

    <https://openregulatory.com/templates/>

General content copyright Radiotherapy AI.
-->

# SOP Document and Record Control

| ISO 13485:2016 Section | Document Section |
| ---------------------- | ---------------- |
| 4.2.4                  | (All)            |
| 4.2.5                  | (All)            |

## Summary

This SOP describes how documents and records are handled. The goal is to
understand how documents are typically structured and in what states they can
be as they move from draft to release. It's similarly important to always have
the most recent document available at the specified location while ensuring
that changes to documents can be traced.

## General Considerations

**Documents** are expected to change over time, whereas **records** are created
once and not altered significantly afterwards.

All documents are written in English.

### Document and Record Labeling

Documents are nested and named according to this schema:

`[systems and/or processes]/[template]/[type]-[name]`

The choice of nesting given by `[systems and/or processes]` is dependent on
whether or not there are multiple documents associated with a given system and
process. For example, this document which is a part quality management system,
and is the document that defines the document and record control process could
be either nested under the `qms` or nested under `qms/document-record-control`.
If there are multiple documents or records associated with
`document-record-control` then the latter option is preferable. If there is
just this document, then a standalone directory is unnecessary.

`[template]` is an optional nesting. For a given form template, the records
associated with that template are nested accordingly.

Document `[type]` is only sometimes relevant and refers to the cases where the
document is either a template with the abbreviation of `tmpl` or if the
document is a standard operating procedure (abbreviation of `sop`).

Some documents are closely tied to a range of attachments and figures. In this
case the document itself is a directory that contains the raw plain text as
well as any of the required attachments.

The document drafting, review, approval and release are managed with the `git`
version control system and the online `GitHub` interface. This is in-line with
the same process undergone to review the company's regulated software.

A draft document exists within a separate `git` branch. Once it undergoes
review and approval it is able to be merged into the `main` branch which is
displayed online at https://docs.radiotherapy.ai. Whenever a new product
release is undergone an offline copy of the user documentation is provided with
the product at release.

Archived documents are deleted from the `main` branch, but are accessible by
browsing the `git` version history.

### Retention Periods

QMS documents and records shall be stored for at least 10 years after their
archival date.

Technical Documentation shall be stored for at least 10 years after the
lifecycle of the respective device has ended.

### Review Periods

We review our QMS documents typically once per year to ensure they remain up to
date.

Our core and safety processes as defined in the quality management manual must
be reviewed at minimum once per year.

All other processes and associated documents can be reviewed every three years
once they have been reviewed before without any findings.

In case of audit findings or related corrective action, it is up to the
discretion of the QMO to apply shorter review periods (e.g. 6 months).

### QMS Document List

We keep an overview list of all QMS documents, including document type, release
date, next review date and respective process owners.

## Process Steps

### Handling of Documents

#### 1. Creation of Documents

All documents are saved in the Quality Management System (QMS) which is housed
within the git repository at <https://github.com/RadiotherapyAI/RadiotherapyAI>.
These documents are viewable at <https://docs.radiotherapy.ai>.

New draft documents can be created by anyone within a separate
`git` branch. Naming and location of documents follows the general
considerations of this SOP (see above). Standard Operating Procedures (SOP)
should specify a process owner responsible to typically update, review and
release all associated documents.

This creation activity undergone is then committed and pushed to the online git
repository.

| Participants    |
| --------------- |
| Any contributor |

| Input   | Output               |
| ------- | -------------------- |
| Content | New Document (draft) |

#### 2. Documents Ready for Review

Once a document is ready for review, its author opens a pull request within
GitHub and the author selects the appropriate reviewers and approvers within
the GitHub interface.

| Participants    |
| --------------- |
| Any contributor |

| Input            | Output                  |
| ---------------- | ----------------------- |
| Document (draft) | Document (under review) |

#### 3. Review of Documents

The respective reviewer(s) and approver(s) review the document. If changes are
required, they can create comments, suggest changes, or directly add their own
changes either utilising the GitHub interface or a local `git` install. If they
approve of the changes then they leave their approval within the GitHub
interface.

| Participants                                                |
| ----------------------------------------------------------- |
| Process owner and/or designated reviewer(s) and approver(s) |

| Input                   | Output                       |
| ----------------------- | ---------------------------- |
| Document (under review) | Document (review successful) |

#### 4. Release of Documents

The release of documents is undergone by merging a pull request into the `main`
branch. When a file has a process owner, that user is designated within the
`CODEOWNERS` file. Any PR that involves a process owner's file must include
that process owner's approval. This is enforced through `GitHub`'s `main`
branch protection setting of "Require review from Code Owners".

The QMO (and, if applicable, the Process Owner) decide if employee training is
required as a result of a release. In general, training for minor
changes/corrections is not necessary.

| Participants       |
| ------------------ |
| QMO, Process Owner |

| Input                        | Output              |
| ---------------------------- | ------------------- |
| Document (review successful) | Document (released) |

#### 5. Changes to Documents

When changes need to be made to a document, any employee with knowledge about
the document and those changes can perform them. To achieve this a git branch
is created where editing of the document is undergone for subsequent PR and
review.

After finishing the edit the process moves to the **Document Ready for Review**
stage (step 2), following the same steps as above.

A QMS change can trigger a substantial change. Before release, it shall be
checked whether it may impact the organization's process landscape and hence,
overall organizational conformity with regulatory requirements. The QMO is
responsible to evaluate such potentially major changes as part of the Change
Evaluation List (reference change management process).

| Participants                                                |
| ----------------------------------------------------------- |
| QMO (change management), any contributor (document changes) |

| Input               | Output                                |
| ------------------- | ------------------------------------- |
| Document (released) | Modified document within Pull Request |

#### 6. Archiving of Documents

Documents get archived if they become obsolete or a newer released version
becomes available. For that, a PR is created where the document itself is
deleted from the `main` branch. This PR follows the same process as above for
an edit. Given the Process Owner is designated as owning that file through the
`CODEOWNERS` file, their review will be required before its deletion.

Due to all files being stored within the `git` version control system, although
it is deleted within the `main` branch, it is still accessible through the
`git` history. We observe retention periods as outlined in this SOP.

| Participants                                           |
| ------------------------------------------------------ |
| Any contributor (initiation), Process Owner (approval) |

| Input               | Output              |
| ------------------- | ------------------- |
| Document (released) | Document (archived) |

### Handling of Records

#### 1. Creation of Records

We create records as required by our processes. If available, we use templates
and checklists for the creation of records. Naming conventions as outlined for
documents do not apply. Records should include an author name and the date of
creation.

| Participants    |
| --------------- |
| Any contributor |

| Input                                      | Output     |
| ------------------------------------------ | ---------- |
| Content, Template Document (if applicable) | New Record |

#### 2. Review and Release of Records

Unless specified differently in a template or SOP, records do not typically
require a review and release process.

| Participants                           |
| -------------------------------------- |
| Designated reviewer(s) and approver(s) |

| Input                 | Output                     |
| --------------------- | -------------------------- |
| Record (under review) | Record (review successful) |

#### 3. Storage of Records

Records are not necessarily stored in our QMS folder. They also may reside in
other applications as specified per respective processes. This is where records
are typically stored:

- _GitHub (Issues, Pull Requests)_

#### 4. Changes to Records

Records are not significantly altered after creation / release. Where
significant changes are required, we rather create a new record and archive the
old one. Non-substantial changes (e.g. spelling mistakes) are considered
corrections only, assessed and added on a case-by-case basis.

| Participants    |
| --------------- |
| Any contributor |

| Input             | Output           |
| ----------------- | ---------------- |
| Record (released) | Record (updated) |

#### 5. Archiving of Records

Records are archived if they become obsolete or a new released version becomes
available. For that, the process owner moves the records to a respective
archiving location. We observe retention periods as outlined in this SOP.

| Participants  |
| ------------- |
| Process Owner |

| Input             | Output            |
| ----------------- | ----------------- |
| Record (released) | Record (archived) |
