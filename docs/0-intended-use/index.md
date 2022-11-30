<!--
Copyright (C) 2022 Radiotherapy AI Holdings Pty Ltd
Copyright (C) 2021-2022 OpenRegulatory (OpenReg GmbH)
This work is licensed under the Creative Commons Attribution 4.0 International
License. <http://creativecommons.org/licenses/by/4.0/>.

Original work by OpenRegulatory available at
<https://github.com/openregulatory/templates>
-->

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

## {{device_name}} Intended Use

<!-- > Describe the core medical functionality of your device and how it treats,
> diagnoses or alleviates a disease. Keep it high-level so that this
> description is true for as long as possible even when the device is updated. -->

A Software as a Medical Device platform that supports patient treatment within
the following use cases:

- Clinical decision support within radiotherapy via automated contouring of
  both target and avoidance structures within the treatment planning workflow.
- Patient alignment and setup support during radiotherapy treatments via
  patient surface guidance.
- Treatment machine gating via patient surface tracking.
- Alignment of radiotherapy simulation images into breathing phases to support
  the treatment workflow.

{{device_name}} intends to be a platform that supports the safe and effective
translation of open source research into Clinical Software as Medical Devices.
As such, it is expected that future regulatory submissions will include
expansions on the above intended use where the surrounding documentation is
also updated accordingly.

## Individual Components

The {{device_name}} is split into separate components. Each component has its
own documentation that covers the following items:

- Intended medical indication
- Contraindications
- Patient population
- User profile
- Use Environment including software/hardware
- Operating principle

The documents for these individual components are the following:

- [](autocontouring.md)
- [](sgrt.md)

## Part of the Body / Type of Tissue Interacted With

The device is stand-alone software. It does not come in contact with tissue or
bodily fluids.

## Variants / Accessories

<!-- > Describe variants and/or accessories of/to this device, if applicable. For
> typical stand-alone software of startups, this shouldn't be applicable. -->

This is stand-alone software and this is not applicable.
