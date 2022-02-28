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

Documents are named according to this schema:

`[ASSOCIATED PROCESS]-[TYPE]-[NAME]`

Where `associated process` can be abbreviated and `type` refers to an
abbreviation of the document type (see below). `Name` refers to the actual file
name. An example would be:

`swd-sop-integrated-software-development`

Some documents are closely tied to a range of attachments and figures. In this
case the document itself is a directory that contains the raw plain text as
well as any of the required attachments. For the purpose of this QMS these
directories represent a single self contained document.

For draft, released, or archived documents this respective record labelling is
determined by its file location within the documentation tree. For archived
documents we add the archived date as a suffix to the document name.

For example:

- A draft document would be `draft/swd-sop-integrated-software-development`
- A released document would be
  `released/swd-sop-integrated-software-development`
- And an archived document with the archival date would be
  `archived/swd-sop-integrated-software-development-2021-02-24`

When a document is undergoing review it exists within a GitHub pull request. An
under review document stays within the `draft` directory, undergoing the
required iterations and feedback until it is approved, at which point it can be
moved into the `released` directory.

Product records are ideally labelled with a device number and device version;
for instance:

`pr1-v1.2-esw-swdp-software-development-plan`

### Document Type Abbreviations

| Abbreviation | Description                                        |
| ------------ | -------------------------------------------------- |
| AM           | Attachment                                         |
| LIS          | List                                               |
| SD           | Supporting Documentation                           |
| SOP          | Standard Operating Procedure (Process Description) |
| TPL          | Template                                           |

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

All documents are saved in the Quality Management System (QMS) which is a
housed within the following git repository on GitHub and is viewable at
<https://docs.radiotherapy.ai>.

New documents can be created by anyone in the company in the
`src/documents/drafts` folder. Naming of documents follows the general
considerations of this SOP (see above). Standard Operating Procedures (SOP)
should specify a process owner responsible to typically update, review and
release all associated documents.

When initially creating the document a table containing a record of the
creation activity is provided at the bottom. For example:

| Activity | Date       | Role | Name        | Initials |
| -------- | ---------- | ---- | ----------- | -------- |
| Creation | 2021-02-24 | CEO  | Simon Biggs | SB       |

This creation activity undergone is then committed to the git repository using
a signed commit. This commit signing requirement is enforced by requiring
signed commits within the `main` branch protection rule for all pull requests
into the `main` branch.

| Participants               |
| -------------------------- |
| Any employee or contractor |

| Input   | Output               |
| ------- | -------------------- |
| Content | New Document (draft) |

#### 2. Documents Ready for Review

Once a document is ready for review, its author opens a pull request within
GitHub and the author selects the appropriate reviewers and approvers within
the GitHub interface.

The author also adds in the respective reviewer and approver items within the
record at the bottom of the document ready for the reviewers to initial the
documents.

| Activity | Date       | Role                  | Name             | Initials |
| -------- | ---------- | --------------------- | ---------------- | -------- |
| Creation | 2021-02-24 | CEO                   | Simon Biggs      | SB       |
| Review   | 2021-02-24 | Regulatory Consultant | Dr. Oliver Eidel |          |
| Approval | 2021-02-24 | CEO                   | Simon Biggs      |          |

The reviewer may initial the document either using the online GitHub interface
where commits are signed and verified. Or utilise git locally with signed
commits.

| Participants               |
| -------------------------- |
| Any employee or contractor |

| Input            | Output                  |
| ---------------- | ----------------------- |
| Document (draft) | Document (under review) |

#### 3. Review of Documents

The respective reviewer(s) and approver(s) review the document. If changes are
required, they can create comments, suggest changes, or directly add their own
changes either utilising the GitHub interface or a local git install. If the
review is successful, they sign their initials at the bottom of the document
and commit this to the repository with a signed and verified commit.

PRs are allowed to be merged even if the document isn't approved, or the review
was only partial, or not at all. As long as the document stays within the
`drafts` directory.

One workflow for signing documents using the online GitHub workflow is first
creating an inline review as in {numref}`Figure %s <start-inline-review>`:

```{figure} start-inline-review.png
:name: start-inline-review

Click the blue plus below the activity row in order to begin an in-line GitHub
PR review.
```

Then utilise the add a suggestion button to allow editing that line within the
review as in {numref}`Figure %s <add-a-suggestion>`:

```{figure} add-a-suggestion.png
:name: add-a-suggestion

Create a suggestion
```

Then write in your initials followed by pressing `Add single comment` as in
{numref}`Figure %s <write-in-initials>`:

```{figure} write-in-initials.png
:name: write-in-initials

Write in your initials
```

Lastly, press `Commit suggestion` followed by writing in an informative commit
message and then pressing `Commit changes` as in {numref}`Figure %s <commit-suggestion>`:

```{figure} commit-suggestion.png
:name: commit-suggestion

Commit the suggestion to the PR. This will use a GitHub signed and verified
commit that is associated to your GitHub user.
```

| Participants                                                |
| ----------------------------------------------------------- |
| Process owner and/or designated reviewer(s) and approver(s) |

| Input                   | Output                       |
| ----------------------- | ---------------------------- |
| Document (under review) | Document (review successful) |

#### 4. Release of Documents

The Process Owner moves the document to the "released" folder and assigns "-a"
to the document name as outlined by the general considerations for document
naming.

A pull request that changes any document within the `released` folder is
restricted so that it must be explicitly reviewed by employees who have been
approved for merging into the release directory within the `main` branch by the
`Process Owner`. These permission levels are defined within the `CODEOWNERS`
file at the root of the repository.

This `CODEOWNERS` file is enforced within GitHub by utilising a branch
protection rule on the `main` branch as well as requiring a review from Code
Owners.

The QMO (and, if applicable, the `Process Owner`) decide if employee training
is required. In general, training for minor changes/corrections is not
necessary.

Prior to release the reviewer(s) and approver(s) initial the table at the
bottom of the document and as before these initials are to be committed as a
signed commit.

Here is an example review and approval table:

| Activity | Date       | Role                  | Name             | Initials |
| -------- | ---------- | --------------------- | ---------------- | -------- |
| Creation | 2021-02-24 | CEO                   | Simon Biggs      | SB       |
| Review   | 2021-02-24 | Regulatory Consultant | Dr. Oliver Eidel | OE       |
| Approval | 2021-02-24 | CEO                   | Simon Biggs      | SB       |

---

| Participants       |
| ------------------ |
| QMO, Process Owner |

| Input                        | Output              |
| ---------------------------- | ------------------- |
| Document (review successful) | Document (released) |

#### 5. Changes to Documents

If changes need to be made to a document, any employee with knowledge about the
document and those changes can perform them. For that, the currently-released
document is copied to the `drafts` folder and edited by the employee. After
finishing the edit, it moves to the **Document Ready for Review** stage (step
2), following the same steps as above.

A QMS change can trigger a substantial change. Before release, it shall be
checked whether it may impact the organization's process landscape and hence,
overall organizational conformity with regulatory requirements. The QMO is
responsible to evaluate such potentially major changes as part of the Change
Evaluation List (reference change management process).

| Participants                                                           |
| ---------------------------------------------------------------------- |
| QMO (change management), any employee or contractor (document changes) |

| Input               | Output                |
| ------------------- | --------------------- |
| Document (released) | Document Copy (draft) |

#### 6. Archiving of Documents

Documents get archived if they become obsolete or a newer released version
becomes available. For that, the `Process Owner` moves the document to the
`archive` folder and assigns a respective archiving date following the general
considerations for document naming in this SOP. We observe retention periods as
outlined in this SOP.

| Participants  |
| ------------- |
| Process Owner |

| Input               | Output              |
| ------------------- | ------------------- |
| Document (released) | Document (archived) |

### Handling of Records

#### 1. Creation of Records

We create records as required by our processes. If available, we use templates
and checklists for the creation of records. Naming conventions as outlined for
documents do not apply. Records should include an author name and the date of
creation.

| Participants               |
| -------------------------- |
| Any employee or contractor |

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

| Participants               |
| -------------------------- |
| Any employee or contractor |

| Input             | Output           |
| ----------------- | ---------------- |
| Record (released) | Record (updated) |

#### 5. Archiving of Records

Records are archived if they become obsolete or a new released version becomes
available. For that, the process owner moves the records to a respective
archiving location. If possible, we follow the general considerations for
document names and add the archiving date to the record name. We observe
retention periods as outlined in this SOP.

| Participants  |
| ------------- |
| Process Owner |

| Input             | Output            |
| ----------------- | ----------------- |
| Record (released) | Record (archived) |

## Document Approval

| Activity | Date       | Role                  | Name             | Initials |
| -------- | ---------- | --------------------- | ---------------- | -------- |
| Creation | 2021-02-24 | CEO                   | Simon Biggs      | SB       |
| Review   | 2021-02-24 | Regulatory Consultant | Dr. Oliver Eidel | OE       |
| Approval | 2021-02-28 | CEO                   | Simon Biggs      | SB       |
