# Instructions for use

This document corresponds to version `0.1.16` of the Radiotherapy AI's Contour
Recommendation software. Currently this software is pre-release, and both the
software and this document is expected to change before it is available for
clinical use. Please reference the version of this document that is supplied to
you with the software itself.

## Details

- **Manufacturer**: Radiotherapy AI PTY LTD
- **Software as a Medical Device Identification**: Radiotherapy AI Contour Recommendations `v0.1.16`

## Overview

Radiotherapy AI's contour recommendations product is deployed onsite as a DICOM
server. It is designed to sit between your centre's CT scanner and your
treatment planning system.

When patients undergo their simulation images are auto-sent through to
Radiotherapy AI's DICOM server. The patient identifying information within the
DICOM header is then encrypted with a client side encryption key, and then
these patient scans are then securely submitted to Google Cloud infrastructure
within Sydney to undergo contouring.

These contours are converted into an RT-DICOM Structure Set file and are then
sent back to the Radiotherapy AI DICOM server for subsequent forwarding through
to the centre's treatment planning system for refinement by the clinical
Radiation Oncologist or Radiation Therapist (the health practitioner) according
to the site's contouring protocols.

In practice, the health practitioner does not directly interact with
Radiotherapy AI's software. Instead, the results from Radiotherapy AI's
software is provided to your centre's treatment planning system for the health
practitioners subsequent refinement.

A digram outlining the dataflow pipeline is provided within
{numref}`Figure %s <pipeline>`:

```{figure} img/deployment-diagram.png
:name: pipeline

Outline of the data transmitted between the different systems in the pipeline.
```

The contouring algorithm that is applied to the CT scans is based off of
historical data that has been created for prior patient treatments while
following the clinical protocols. It is the intent of the contouring
recommendation algorithm to mimic those clinical protocols.

## Intended use

### User training and knowledge

The contours provided by the Radiotherapy AI Contour Recommendations software
are a recommendation only. When be used to support clinical radiotherapy
treatment these contours are to be provided to a RANZCR certified Radiation
Oncologist or an ASMIRT certified Radiation Therapist for subsequent refinement
according to that clinic's approved contouring protocols.

### Used in cases where there is already a clinically implemented contouring protocol

For each contour provided by the software to the user, the user needs to be
able to validate the contour against the clinically implemented contouring
protocol, and if needed, either refine the provided contour to come into
alignment with the protocol, or potentially completely redraw the contour.

Either a network file path or an intranet URL that references the corresponding
contouring protocols is to be provided by the customer organisation to
Radiotherapy AI so that within each DICOM ROI Description field this protocol
reference can be displayed. It is expected that the software that the user
utilises to validate/refine the contours provides a means for the user to
clearly view this imported DICOM field.

This is to be inline with the following requirement for exempt clinical
decision support software (CDSS) [as per the TGA](https://www.tga.gov.au/sites/default/files/clinical-decision-support-software.pdf):

> Exempted CDSS devices must clearly reference the basis of the
> recommendations, including the source(s) of information used (e.g. specific
> clinical guideline, hospital procedure) so that the information can be
> independently reviewed by the user. The user may rely on their own judgement
> and reach a recommendation without primarily relying on the software
> function.

### Provides a recommendation only and is not intended to replace clinical judgement

The software provides unapproved DICOM-RT Structure set files. These are then
sent through to a contour drawing, refining and approval system, either a TPS
or a dedicated contouring software system.

The health practitioner, either a Radiation Oncologist or a Radiation
Therapist, is to use their clinical judgement to decide whether or not
refinement is appropriate before approval and whether or not approval is
appropriate at all. This clinical judgement is to be informed by the
department's published contouring protocols to which the software's recommended
contours can be directly compared.

The software is not to be used in situations where the software provides
recommendations that cannot be corroborated with current published clinical
protocols.

It is by this intended use that criteria 2 and 3 for CDSS to be considered
exempt is met:

> **Criteria 2**: It is intended only for the purpose of providing or
> supporting a recommendation to a health professional about prevention,
> diagnosis, curing or alleviating a disease, ailment, defect or injury.

> **Criteria 3**: It is not intended to replace the clinical judgement of a
> health professional in relation to making a clinical diagnosis or decision
> about the treatment of patients

### Limited by case validation of the deployed model

It is intended that the usage of the model be limited to cases where the model
has been validated for the combination of:

- Contours based on the clinically utilised protocol
- Patient population demographics such as age group, sex, race and disease
  state
- Imaging region
- Patient orientation
- Imaging device
- Imaging modality
- Imaging parameters such as energy, resolution, reconstruction kernels, MRI
  sequences
- Scenario induced imaging artifacts such as metal spinal implants, dental
  work, metal hips

The recommended way to validate that the model appropriately handles the above
cases is to collect a representative clinical dataset of the above for model
validation, and if necessary a further independent dataset for model
refinement.

For new models this representative sample can be utilised in unison with the
provided tools to readily undergo bulk validation and investigation.

For more information on commissioning and ongoing quality assurance of AI
models in radiotherapy see the following article:

> Liesbeth, V., Michaël, C., Anna, M. D., Charlotte, L. B., Wouter, C., & Dirk,
> V. (2020).
> [Overview of artificial intelligence-based applications in radiotherapy: Recommendations for implementation and quality assurance.](https://doi.org/10.1016/j.radonc.2020.09.008)
> Radiotherapy and Oncology.

### To be utilised within the framework of standard DICOM input and output

The software is intended to receive DICOM files that conform to the DICOM
standard. The software that it provides results to is intended to receive and
appropriately handle standards compliant DICOM structure files. It is not
intended to directly interface with another medical device except via this
standard DICOM input output (either file based or DICOM network protocol based).

It is by this intended use that criteria 1 for CDSS to be considered exempt is
met:

> **Criteria 1**: It is not intended to directly process or analyse a medical
> image or a signal from another medical device (including an in vitro
> diagnostic device).

### Pseudonymisation key for patient header information

Identifying patient header information is pseudonymised so that reversal is
only achievable via a key that is never sent to the Radiotherapy AI cloud
server. This key is stored within the Windows Credential manager vault within
the operating system where the local Radiotherapy AI DICOM server is installed.

This key is to be treated with the same level of protection as the patient
information it is encrypting. The Windows Credential vault is encrypted by the
OS using the Windows account login password. It is expected that both
access to that account and its account password meets requirements appropriate
to the protection of identifying patient information.

### Validation of pseudonymisation undergone with a representative sample

The Radiotherapy AI DICOM server can be configured to not send files to the
cloud but to instead send the pseudonymised data either to file, or to another
piece of software via a DICOM send. This utility is to be used after
installation, and after any upgrades to the DICOM server that adjust the
pseudonymisation to verify that the appropriate header items within the DICOM
file have been appropriately de-identified by the installed server.

### Not to receive DICOM images that have identifying patient information burned into the pixel data

Only identifying patient information that is stored within the standards
compliant DICOM header is pseudonymised before sending to the cloud sever.

The DICOM software can be configured to only send through certain DICOM file
types. By default this is CT, MRI and RT-DICOM specific files. This is to help
prevent bulk DICOM sends containing other DICOM types that sometimes have burnt
in pixel data included having those extra images included in the
pseudonymisation + upload.

### Be installed on a server with appropriate network and internet bandwidth

In order to receive DICOM structure results in a timely fashion the provided
network and internet bandwidth, in particular the upload bandwidth, needs to
meet the requirements of the clinic. For a 200 slice CT scan at 512 kB per
slice the resulting 100 MB dataset needs to be able to be uploaded to the cloud
server for the model to create the contours. A 1 Gbit/s upload (top tier fibre
NBN) will upload this data in ~1 second. A 20 Mbit/s upload connection (copper
NBN) will upload this data in ~1 minute. A 1 Mbit/s upload connection (ADSL2+)
will upload this data in ~15 minutes.

Hospital and network traffic can cause upload bottlenecks. Enterprise routers
can be configured using "Quality of Service" so as to prioritise uploads from
specific servers.

### Prompt access to notifications, warnings and alerts

Through the dashboard interface users can designate warning and alert
thresholds for a range of relevant scenarios. The software itself may also
present warnings and alerts. The email address of the user account used to
access the software needs to be able to be readily accessed so that these
configurable alerts and warnings can provide the appropriate notification.

## Appendix

### Essential principles that still need to be covered

13.1 Information to be provided with medical devices –
general
(1) The following information must be provided with a
medical device:

(c) information explaining how to use the device safely,
having regard to the training and knowledge of potential
users of the device.
(2) In particular:
(a) the information required by clause 13.3 must be
provided with a medical device; and
(b) if instructions for use of the device are required
under subclause 13.4, the information mentioned in
subclause 13.4(3) must be provided in those
instructions.
(3) The information:
(a) must be provided in English; and
(b) may also be provided in any other language.
(4) The format, content and location of the information must
be appropriate for the device and its intended purpose.
(5) Any number, letter, symbol, or letter or number in a
symbol, used in the information must be legible and at
least 1 millimetre high.
(6) If a symbol or identification colour that is not included in
a medical device standard is used in the information
provided with the device, or in the instructions for use of
the device, the meaning of the symbol or identification
colour must be explained in the information provided
with the device or the instructions for use of the device

13.3 Information to be provided with medical devices –
particular requirements
The information mentioned below must be provided with a
medical device.
(1) The manufacturer’s name, or trade name, and address
(2) The intended purpose of the device, the intended user
of the device, and the kind of patient on whom the
device is intended to be used where these are not
obvious
(3) Sufficient information to enable a user to identify the
device, or if relevant, the contents of packaging
(4) Any particular handling or storage requirements
applying to the device
(5) Any warnings, restrictions on use, or precautions that
should be taken, in relation to the use of the device
(6) Any special operating instructions for the use of the
device
(7) If applicable, an indication that the device is intended for
a single use only
(8) If applicable, an indication that the device has been
custom-made for a particular individual or health
professional and is intended for use only by that
individual or health professional
(9) If applicable, an indication that:
(a) if the device is a medical device other than an IVD
medical device – the device is intended for pre-
market clinical investigation; or
(b) if the device is an IVD medical device – the device is
intended for performance evaluation only
(10) For a sterile device, the word “STERILE” and
information about the method that was used to sterilise
the device
(11) The batch code, lot number or serial number of the
device.
(12) If applicable, a statement of the date (expressed in a
way that clearly identifies the month and year) up to
when the device can be safely used
(13) If the information provided with the device does not
include the information mentioned in item 12 – a
statement of the date of manufacture of the device (this
may be included in the batch code, lot number or serial
number of the device provided the date is clearly
identifiable)
(14) If applicable, the words “for export only”
Note: In addition to the information mentioned above,
regulation 10.2 requires certain information to be
provided with a medical device

13.4 Instructions for use
(1) Instructions for the use of a medical device must be
provided with the device.
(2) However, instructions for use of a medical device need
not be provided with the device, or may be abbreviated,
if:
(a) the device is a Class I medical device, a Class IIa
medical device or a Class 1 IVD medical device;
and
(b) the device can be used safely for its intended
purpose without instructions.
(3) Instructions for the use of a medical device must include
information mentioned below that is applicable to the
device.
(1) The manufacturer’s name, or trade name, and
address
(2) The intended purpose of the device, the intended
user of the device, and the kind of patient on whom
the device is intended to be used
(3) Information about any risk arising because of other
equipment likely to be present when the device is
being used for its intended purpose (for example,
electrical interference from electro-surgical devices
or magnetic field interference from magnetic
resonance images)
(4) Information about the intended performance of the
device and any undesirable side effects caused by
use of the device
(5) Any contraindications, warnings, restrictions on use,
or precautions that may apply in relation to use of
the device
(6) Sufficient information to enable a user to identify the
device, or if relevant, the contents of the packaging
(7) Any particular handling or storage requirements
applying to the device
(8) If applicable, an indication that the device is
intended for a single use only
(9) If applicable, an indication that the device has been
custom-made for a particular individual or health
professional and is intended for use only by that
individual or health professional
(10) If applicable, an indication that:
(a) if the device is a medical device other than an
IVD medical device – the device is intended for
pre-market clinical investigation; or
(b) if the device is an IVD medical device – the
device is intended for performance evaluation
only
(11) For a sterile device, the word “STERILE” and
information about the method that was used to
sterilise the device
(12) For a device that is intended by the manufacturer
to be supplied in a sterile state:
(a) an indication that the device is sterile; and
(b) information about what to do if sterile
packaging is damaged and;
(c) if appropriate, instructions for resterilisation of
the device.
(13) For a medical device that is intended by the
manufacturer to be sterilised before use –
instructions for cleaning and sterilising the device
which, if followed, will ensure that the device
continues to comply with the applicable provisions
of the essential principles
(14) Any special operating instructions for the use of the
device
(15) Information to enable the use to verify whether the
device is properly installed and whether it can be
operated safely and correctly, including details of
calibration (if any) needed to ensure that the device
operates properly and safely during its intended life
(16) Information about the nature and frequency of regular
and preventative maintenance of the device, including
information about the replacement of consumable
components of the device during its intended life
(17) Information about any treatment or handling needed
before the device can be used
(18) For a device that is intended by the manufacturer to be
installed with, or connected to, another medical device or
other equipment so that the device can operate as
required for its intended purpose – sufficient information
about the device to enable the user to identify the
appropriate other medical device or equipment that will
ensure a safe combination.
(19) For an implantable device – information about any risks
associated with its implantation
(20) For a reusable device:
(a) information about the appropriate processes to allow
reuse of the device (including information about cleaning,
disinfection, packaging, and, if appropriate, resterilisation
of the device); and
(b) an indication of the number of times the device may be
safely reused.
(21) For a medical device that is intended by the
manufacturer to emit radiation for medical purposes –
details of the nature, type, intensity and distribution of the
radiation emitted
(22) Information about precautions that should be taken by a
patient and the user if the performance of the device
changes
(23) Information about precautions that should be taken by a
patient and the user if it is reasonably foreseeable that
use of the device will result in the patient or user being
exposed to adverse environmental conditions
(24) Adequate information about any medicinal product
that the device is designed to administer, including
and limitations on the substances that may be
administered using the device
(25) Information about any medicine (including any
stable derivative of human blood or blood plasma)
that is incorporated, or intended to be incorporated,
into the device as an integral part of the device.
(25A) For a medical device, other than an IVD medical
device, information about any tissues, tissue
derivatives, cells or substances of animal origin that
have been rendered non-viable, or tissues, cells or
substances of microbial or recombinant origin that
are included in the device
(26) Information about precautions that should be taken
by a patient and the user if there are special or
unusual risks associated with the disposal of the
device
(27) Information about the degree of accuracy claimed
if the device has a measuring function
(28) Information about any particular facilities required
for use of the device or any particular training or
qualifications required by the user of the device.
(29) For an IVD medical device, information (including,
to the extent practicable, drawings and diagrams)
about the following:
(a) the scientific principle (the ‘test principle’) on
which the performance of the IVD medical
device relies;
(b) specimen type, collection, handling and
preparation;
(c) reagent description and any limitations (for
example, use with a dedicated instrument
only);
(d) assay procedure including calculations and
interpretation of results;
(e) interfering substances and their effect on the
performance of the assay;
(f) analytical performance characteristics, such as
sensitivity, specificity, accuracy and precision;
(g) clinical performance characteristics, such as
sensitivity and specificity;
(h) reference intervals, if appropriate;
(i) any precautions to be taken in relation to
substances or materials that present a risk of
infection
(30) For an adaptable medical device, instructions for
assembling or adapting the device which, if followed,
will ensure that the device continues to comply with the
applicable provisions of the essential principles
(31) For a medical device production system, instructions
for the process to be followed in producing the medical
device the system is intended to produce which, if followed,
will ensure that the device so produced will comply with the
applicable provisions of the essential principles

13B. Software – version numbers and build numbers

(1) For a medical device that is software, or that
incorporates software, the current version number and
current build number of the software must be
accessible by, and identifiable to, users of the device.
(2) The current version number and current build number of
the software:
(a) must be in English; and
(b) may also be in any other language
