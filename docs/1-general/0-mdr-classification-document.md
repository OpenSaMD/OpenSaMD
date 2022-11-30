<!--
Copyright (C) 2022 Radiotherapy AI Holdings Pty Ltd
Copyright (C) 2021-2022 OpenRegulatory (OpenReg GmbH)
This work is licensed under the Creative Commons Attribution 4.0 International
License. <http://creativecommons.org/licenses/by/4.0/>.

Original work by OpenRegulatory available at
<https://github.com/openregulatory/templates>
-->

# MDR Classification Document

## Mapping of Requirements

<!--
> NOTE: this template only serves for MDR purposes. Before May 2021, use Annex
> IX MDD instead of Annex VIII MDR. -->

| Medical Device Regulation (MDR) | Document Section |
| ------------------------------- | ---------------- |
| Annex VIII                      | (All)            |

## Summary

| Product:        | {{device_name}}           |
| --------------- | ------------------------- |
| Version:        | {{device_version}}        |
| Classification: | {{device_classification}} |
| Rule:           | Rule 9                    |

### Classifying rule

All active devices intended to emit ionizing radiation for therapeutic
purposes, **including devices which control or monitor such devices, or which**
**directly influence their performance, are classified as class IIb.**

## Chapter I: Applicable Definitions

<!--
> You will need to carefully check and fill out all rows below. Some rows are
> pre-filled for applicability under the assumption of a stand-alone software
> medical device. However, this is quite an essential document and you're
> better off checking twice. -->

### 1 Duration of Use

#### 1.1 Transient

Normally intended for continuous use for less than 60 minutes.

_Applicable:_ **No**

#### 1.2 Short term

Normally intended for continuous use for not more than 30 days.

_Applicable:_ **No**

#### 1.3 Long term

Normally intended for continuous use for more than 30 days.

_Applicable:_ **No**

### 2 Invasive and Active Devices

#### 2.1 Body orifice

Any natural opening in the body, as well as the external surface of the eyeball, or any permanent artificial opening, such as a stoma.

_Applicable:_ **No**

#### 2.2 Surgically invasive device

- An invasive device which penetrates inside the body through the surface of
  the body, including through mucous membranes of body orifices with the aid or
  in the context of a surgical operation; and
- a device which produces penetration other than through a body orifice.

_Applicable:_ **No**

#### 2.3 Reusable surgical instrument

An instrument intended for surgical use in cutting, drilling, sawing,
scratching, scraping, clamping, retracting, clipping or similar procedures,
without a connection to an active device and which is intended by the
manufacturer to be reused after appropriate procedures such as cleaning,
disinfection and sterilization have been carried out.

_Applicable:_ **No**

#### 2.4 Active therapeutic device

Any active device used, whether alone or in combination with other devices, to
support, modify, replace or restore biological functions or structures with a
view to treatment or alleviation of an illness, injury or disability.

_Applicable:_ **Yes**

#### 2.5 Active device intended for diagnosis and monitoring

Any active device used, whether alone or in combination with other devices, to
supply information for detecting, diagnosing, monitoring or treating physio
logical conditions, states of health, illnesses or congenital deformities.

_Applicable:_ **Yes**

#### 2.6 Central circulatory system

The following blood vessels:

Arteriae pulmonales, aorta ascendens, arcus aortae, aorta descendens to the
bifurcatio aortae, arteriae coronariae, arteria carotis communis, arteria
carotis externa, arteria carotis interna, arteriae cerebrales, truncus
brachiocephalicus, venae cordis, venae pulmonales, vena cava superior and vena
cava inferior.

_Applicable:_ **No**

#### 2.7 Central nervous system

The brain, meninges and spinal cord.

_Applicable:_ **No**

#### 2.8 Injured skin or mucous membrane

An area of skin or a mucous membrane presenting a pathological change or change
following disease or a wound.

_Applicable:_ **No**

## Chapter II: Implementing Rules

### 3.1

Application of the classification rules shall be governed by the intended
purpose of the devices.

_Applicable:_ **Yes**

### 3.2

If the device in question is intended to be used in combination with another
device, the classification rules shall apply separately to each of the devices.
Accessories for a medical device and for a product listed in Annex XVI MDR
shall be classified in their own right separately from the device with which
they are used.

_Applicable:_ **Yes**

### 3.3

Software, which drives a device or influences the use of a device, shall fall
within the same class as the device. If the software is independent of any
other device, it shall be classified in its own right.

_Applicable:_ **Yes**

### 3.4

If the device is not intended to be used solely or principally in a specific
part of the body, it shall be considered and classified on the basis of the
most critical specified use.

_Applicable:_ **Yes**

### 3.5

If several rules, or if, within the same rule, several sub-rules, apply to the
same device based on the device's intended purpose, the strictest rule and
sub-rule resulting in the higher classification shall apply.

_Applicable:_ **Yes**

### 3.6

In calculating the duration referred to in Section 1, continuous use shall mean:

- the entire duration of use of the same device without regard to temporary
  interruption of use during a procedure or temporary removal for purposes such
  as cleaning or disinfection of the device. Whether the interruption of use or
  the removal is temporary shall be established in relation to the duration of
  the use prior to and after the period when the use is interrupted or the
  device removed; and
- the accumulated use of a device that is intended by the manufacturer to be
  replaced immediately with another of the same type.

_Applicable:_ **No**

### 3.7

A device is considered to allow direct diagnosis when it provides the diagnosis
of the disease or condition in question by itself or when it provides decisive
information for the diagnosis.

_Applicable:_ **No**

## Chapter III: Classification Rules

### 4 Non-Invasive Devices

#### 4.1 Rule 1

All non-invasive devices are classified as class I, unless one of the rules set
out hereinafter applies.

_Applicable:_ **No**

#### 4.2 Rule 2

All non-invasive devices intended for channelling or storing blood, body
liquids, cells or tissues, liquids or gases for the purpose of eventual
infusion, administration or introduction into the body are classified as class
IIa:

- if they may be connected to a class IIa, class IIb or class III
  active device; or
- if they are intended for use for channelling or storing blood or other body
  liquids or for storing organs, parts of organs or body cells and tissues,
  except for blood bags; blood bags are classified as class IIb.

In all other cases, such devices are classified as class I.

_Applicable:_ **No**

#### 4.3 Rule 3

All non-invasive devices intended for modifying the biological or chemical
composition of human tissues or cells, blood, other body liquids or other
liquids intended for implantation or administration into the body are
classified as class IIb, unless the treatment for which the device is used
consists of filtration, centrifugation or exchanges of gas, heat, in which case
they are classified as class IIa.

All non-invasive devices consisting of a substance or a mixture of substances
intended to be used in vitro in direct contact with human cells, tissues or
organs taken from the human body or used in vitro with human embryos before
their implantation or administration into the body are classified as class III.

_Applicable:_ **No**

#### 4.4 Rule 4

All non-invasive devices which come into contact with injured skin or mucous
membrane are classified as:

- class I if they are intended to be used as a mechanical barrier, for
  compression or for absorption of exudates;
- class IIb if they are intended to be used principally for injuries to skin
  which have breached the dermis or mucous membrane and can only heal by
  secondary intent;
- class IIa if they are principally intended to manage the micro-environment of
  injured skin or mucous membrane; and
- class IIa in all other cases.

This rule applies also to the invasive devices that come into contact with
injured mucous membrane.

_Applicable:_ **No**

### 5 Invasive Devices

#### 5.1 Rule 5

All invasive devices with respect to body orifices, other than surgically
invasive devices, which are not intended for connection to an active device or
which are intended for connection to a class I active device are classified as:

- class I if they are intended for transient use;
- class IIa if they are intended for short-term use, except if they are used in
  the oral cavity as far as the pharynx, in an ear canal up to the ear drum or
  in the nasal cavity, in which case they are classified as class I; and
- class IIb if they are intended for long-term use, except if they are used in
  the oral cavity as far as the pharynx, in an ear canal up to the ear drum or
  in the nasal cavity and are not liable to be absorbed by the mucous membrane,
  in which case they are classified as class IIa.

All invasive devices with respect to body orifices, other than surgically
invasive devices, intended for connection to a class IIa, class IIb or class
III active device, are classified as class IIa.

_Applicable:_ **No**

#### 5.2 Rule 6

All surgically invasive devices intended for transient use are classified as
class IIa unless they:

- are intended specifically to control, diagnose, monitor or correct a defect
  of the heart or of the central circulatory system through direct contact with
  those parts of the body, in which case they are classified as class III;
- are reusable surgical instruments, in which case they are classified as class
  I;
- are intended specifically for use in direct contact with the heart or central
  circulatory system or the central nervous system, in which case they are
  classified as class III;
- are intended to supply energy in the form of ionising radiation in which case
  they are classified as class IIb;
- have a biological effect or are wholly or mainly absorbed in which case they
  are classified as class IIb; or
- are intended to administer medicinal products by means of a delivery system,
  if such administration of a medicinal product is done in a manner that is
  potentially hazardous taking account of the mode of application, in which
  case they are classified as class IIb.

_Applicable:_ **No**

#### 5.3 Rule 7

All surgically invasive devices intended for short-term use are classified as
class IIa unless they:

- are intended specifically to control, diagnose, monitor or correct a defect
  of the heart or of the central circulatory system through direct contact with
  those parts of the body, in which case they are classified as class III;

- are intended specifically for use in direct contact with the heart or central
  circulatory system or the central nervous system, in which case they are
  classified as class III;
- are intended to supply energy in the form of ionizing radiation in which case
  they are classified as class IIb;
- have a biological effect or are wholly or mainly absorbed in which case they
  are classified as class III;
- are intended to undergo chemical change in the body in which case they are
  classified as class IIb, except if the devices are placed in the teeth; or
- are intended to administer medicines, in which case they are classified as
  class IIb.

_Applicable:_ **No**

#### 5.4 Rule 8

All implantable devices and long-term surgically invasive devices are
classified as class IIb unless they:

- are intended to be placed in the teeth, in which case they are classified as
  class IIa;
- are intended to be used in direct contact with the heart, the central
  circulatory system or the central nervous system, in which case they are
  classified as class III;
- have a biological effect or are wholly or mainly absorbed, in which case they
  are classified as class III;
- are intended to undergo chemical change in the body in which case they are
  classified as class III, except if the devices are placed in the teeth;
- are intended to administer medicinal products, in which case they are
  classified as class III;
- are active implantable devices or their accessories, in which cases they are
  classified as class III;
- are breast implants or surgical meshes, in which cases they are classified as
  class III;
- are total or partial joint replacements, in which case they are classified as
  class III, with the exception of ancillary components such as screws, wedges,
  plates and instruments; or
- are spinal disc replacement implants or are implantable devices that come
  into contact with the spinal column, in which case they are classified as
  class III with the exception of components such as screws, wedges, plates and
  instruments.

_Applicable:_ **No**

### 6 Active Devices

#### 6.1 Rule 9

All active therapeutic devices intended to administer or exchange energy are
classified as class IIa unless their characteristics are such that they may
administer energy to or exchange energy with the human body in a potentially
hazardous way, taking account of the nature, the density and site of
application of the energy, in which case they are classified as class IIb.

All active devices intended to control or monitor the performance of active
therapeutic class IIb devices, or intended directly to influence the
performance of such devices are classified as class IIb.

All active devices intended to emit ionizing radiation for therapeutic
purposes, including devices which control or monitor such devices, or which
directly influence their performance, are classified as class IIb.

All active devices that are intended for controlling, monitoring or directly
influencing the performance of active implantable devices are classified as
class III.

_Applicable:_ **Yes**

#### 6.2 Rule 10

Active devices intended for diagnosis and monitoring are classified as class
IIa:

- if they are intended to supply energy which will be absorbed by the human
  body, except for devices intended to illuminate the patient's body, in the
  visible spectrum, in which case they are classified as class I;
- if they are intended to image in vivo distribution of radiopharmaceuticals;
  or
- if they are intended to allow direct diagnosis or monitoring of vital
  physiological processes, unless they are specifically intended for monitoring
  of vital physiological parameters and the nature of variations of those
  parameters is such that it could result in immediate danger to the patient,
  for instance variations in cardiac performance, respiration, activity of the
  central nervous system, or they are intended for diagnosis in clinical
  situations where the patient is in immediate danger, in which cases they are
  classified as class IIb.

Active devices intended to emit ionizing radiation and intended for diagnostic
or therapeutic radiology, including interventional radiology devices and
devices which control or monitor such devices, or which directly influence
their performance, are classified as class IIb.

_Applicable:_ **No**

#### 6.3 Rule 11

Software intended to provide information which is used to take decisions with
diagnosis or therapeutic purposes is classified as class IIa, except if such
decisions have an impact that may cause:

- death or an irreversible deterioration of a person's state of health, in
  which case it is in class III; or
- a serious deterioration of a person's state of health or a surgical
  intervention, in which case it is classified as class IIb.

Software intended to monitor physiological processes is classified as class
IIa, except if it is intended for monitoring of vital physiological parameters,
where the nature of variations of those parameters is such that it could result
in immediate danger to the patient, in which case it is classified as class
IIb. All other software is classified as class I.

_Applicable:_ **No**

#### 6.4 Rule 12

All active devices intended to administer and/or remove medicinal products,
body liquids or other substances to or from the body are classified as class
IIa, unless this is done in a manner that is potentially hazardous, taking
account of the nature of the substances involved, of the part of the body
concerned and of the mode of application in which case they are classified as
class IIb.

_Applicable:_ **No**

#### 6.5 Rule 13

All other active devices are classified as class I.

_Applicable:_ **No**

### 7 Special Rules

#### 7.1 Rule 14

All devices incorporating, as an integral part, a substance which, if used
separately, can be considered to be a medicinal product, as defined in point 2
of Article 1 of Directive 2001/83/EC, including a medicinal product derived
from human blood or human plasma, as defined in point 10 of Article 1 of that
Directive, and that has an action ancillary to that of the devices, are
classified as class III.

_Applicable:_ **No**

#### 7.2 Rule 15

All devices used for contraception or prevention of the transmission of
sexually transmitted diseases are classified as class IIb, unless they are
implantable or long term invasive devices, in which case they are classified as
class III.

_Applicable:_ **No**

#### 7.3 Rule 16

All devices intended specifically to be used for disinfecting, cleaning,
rinsing or, where appropriate, hydrating contact lenses are classified as class
IIb.

All devices intended specifically to be used for disinfecting or sterilising
medical devices are classified as class IIa, unless they are disinfecting
solutions or washer-disinfectors intended specifically to be used for
disinfecting invasive devices, as the end point of processing, in which case
they are classified as class IIb.

This rule does not apply to devices that are intended to clean devices other
than contact lenses by means of physical action only.

_Applicable:_ **No**

#### 7.4 Rule 17

Devices specifically intended for recording of diagnostic images generated by
X-ray radiation are classified as class IIa.

_Applicable:_ **No**

#### 7.5 Rule 18

All devices manufactured utilizing tissues or cells of human or animal origin,
or their derivatives, which are non-viable or rendered non-viable, are
classified as class III, unless such devices are manufactured utilizing tissues
or cells of animal origin, or their derivatives, which are non-viable or
rendered non-viable and are devices intended to come into contact with intact
skin only.

_Applicable:_ **No**

#### 7.6 Rule 19

All devices incorporating or consisting of nanomaterial are classified as:

- class III if they present a high or medium potential for internal exposure;
- class IIb if they present a low potential for internal exposure; and
- class IIa if they present a negligible potential for internal exposure.

_Applicable:_ **No**

#### 7.7 Rule 20

All invasive devices with respect to body orifices, other than surgically
invasive devices, which are intended to administer medicinal products by
inhalation are classified as class IIa, unless their mode of action has an
essential impact on the efficacy and safety of the administered medicinal
product or they are intended to treat life-threatening conditions, in which
case they are classified as class IIb.

_Applicable:_ **No**

#### 7.8 Rule 21

Devices that are composed of substances or of combinations of substances that
are intended to be introduced into the human body via a body orifice or applied
to the skin and that are absorbed by or locally dispersed in the human body are
classified as:

- class III if they, or their products of metabolism, are systemically absorbed
  by the human body in order to achieve the intended purpose;
- class III if they achieve their intended purpose in the stomach or lower
  gastrointestinal tract and they, or their products of metabolism, are
  systemically absorbed by the human body;
- class IIa if they are applied to the skin or if they are applied in the nasal
  or oral cavity as far as the pharynx, and achieve their intended purpose on
  those cavities; and
- class IIb in all other cases.

_Applicable:_ **No**

#### 7.9 Rule 22

Active therapeutic devices with an integrated or incorporated diagnostic
function which significantly determines the patient management by the device,
such as closed loop systems or automated external defibrillators, are
classified as class III.

_Applicable:_ **No**
