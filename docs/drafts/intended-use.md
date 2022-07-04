# Intended Use

## Mapping of Requirements to Document Sections

| MDR Class | MDR Section                   | Document Section |
| --------- | ----------------------------- | ---------------- |
| (All)     | Annex II, 1.1 a) - d), h), i) | (All)            |

| ISO 14971:2019 Section | Document Section |
| ---------------------- | ---------------- |
| 5.2                    | (All)            |

| IEC 62366-1:2015 Section | Document Section |
| ------------------------ | ---------------- |
| 5.1                      | (All)            |

## Product

- Name: {{device_name}}
- Version: {{device_version}}
- Basic UDI-DI: N/A

## Intended Medical Indication

Utilised as clinical decision support software within the radiotherapy
treatment workflow. Provides anatomical contours utilised by health
practitioners to create a radiotherapy treatment plan to assist in cancer
treatment or other radiotherapy treatments.

<!-- > Describe the condition(s) and/or disease(s) to be screened, monitored, treated, diagnosed, or prevented by
> your software. Importantly, also list exclusion criteria: Maybe patients with a certain diagnosis should not
> be using your device. -->

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

(case-validation)=
### Limited by case validation of the deployed model

It is intended that the usage of the model be limited to use within the
radiotherapy treatment workflow in cases where the model has been validated for
the combination of:

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

## Patient Population

The patient population is to be limited to where the model itself has undergone
validation. See section [](case-validation) for further details.

## User Profile

<!-- > Describe the typical user of the software. Some ideas could be: Qualifications, prior training (for your
> software), technical proficiency, time spent using the software. -->

### Used by those with appropriate training and knowledge

The contours provided by the Radiotherapy AI Contour Recommendations software
are a recommendation only. When being used to support clinical radiotherapy
treatment within Australia these contours are to be provided to a RANZCR
certified Radiation Oncologist or an ASMIRT certified Radiation Therapist for
subsequent refinement according to that clinic's approved contouring protocols.

### Refined by a relevant health professional and subsequently checked by an independent relevant health professional

It is intended that the software results be refined by a relevant health
professional and then be subsequently checked by a separate and independent
relevant health professional before the patient contours are utilised to create
the radiotherapy treatment plan.

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

## Use Environment Including Software/Hardware

<!-- > Describe the typical use environment. What sort of devices is this running on? Does the software only run on
> one device or on multiple devices? Is it loud and chaotic like in an emergency ward? How's the lighting?
>
> Also, add other software or hardware which is required by your device. Most commonly, apps require users to
> have a smartphone with a compatible operating system (iOS / Android). -->

The DICOM server software is installed on a local Windows OS with version >=
`10`. The results from the software are forwarded through to the treatment
planning or contour editing/refining application of choice. It is within the
environment of that other piece of software where the results from this product
are utilised by the health practitioner.

The data workflow of data for the deployment within the clinic is outlining
within the diagram in {numref}`Figure %s <intended-use:pipeline>`:

```{figure} img/deployment-diagram.png
:name: intended-use:pipeline

Outline of the data transmitted between the different systems in the pipeline.
```

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

## Operating Principle

<!-- > It's kind of a stretch to describe the "operating principle" of software. I guess this makes more sense for
> hardware devices. In any case, I'd just generally state what sort of input goes in and what output comes
> out, e.g. you could be processing images and returning diagnoses. -->

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

### Prompt access to notifications, warnings and alerts

Through the dashboard interface users can designate warning and alert
thresholds for a range of relevant scenarios. The software itself may also
present warnings and alerts. The email address of the user account used to
access the software needs to be able to be readily accessed so that these
configurable alerts and warnings can provide the appropriate notification.

## Part of the Body / Type of Tissue Interacted With

The device is stand-alone software. It receives input from the user and outputs
information. It doesn't come in contact with tissue or bodily fluids.
