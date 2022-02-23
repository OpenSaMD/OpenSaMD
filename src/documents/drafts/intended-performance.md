# Intended performance

Performance on a given set of validation/test/hold-out data is a useful
indicator of what can be expected for the performance of the software. However
it is not a guarantee. Therefore, as detailed within the {doc}`intended-use`
document, it is intended that the recommended contours be refined by the health
practitioner before clinical use.

## Overview

To provide an example of the level of results intended by this software this
document details the results from the head and neck model named
`lifehouse-0.2.0`. It represents the results from the model that was frozen on
15/10/2021. Its checkpoint label is `20211015-104758/0000`.

In practice, before utilisation clinically within your centre the model is to
be validated and potentially refined using retrospective treatment data from
your centre. This is detailed within the {doc}`intended-use` document.

## Data overview

This model was built from the combination of standard clinical data from Chris
O’Brien Lifehouse as well as the DeepMind open access dataset
(<https://github.com/deepmind/tcia-ct-scan-dataset>). Both the Chris O’Brien
Lifehouse data and the DeepMind data were split into "Training”, "Validation",
and "Hold-out" groups. Training data was used to train the model, validation
data was used to iterate on the software development and define when a
particular contour was ready, hold-out data was used only to report the final
results with the aim to provide unbiased reporting.

Chris O’Brien Lifehouse validation and hold-out datasets were utilised for
empirical visual investigation of the resulting DICOM files. DeepMind
validation and hold-out datasets were used for metric based comparisons.

## Number of patient scans utilised per dataset

### Chris O’Brien LifeHouse (Australian scans and protocols)

|                        | Training | Validation | Hold out |
| ---------------------- | -------- | ---------- | -------- |
| Brain                  | 18       | 4          | 4        |
| Spinal Cord            | 151      | 18         | 23       |
| Mandible               | 136      | 13         | 18       |
| Larynx                 | 131      | 13         | 19       |
| Brainstem              | 146      | 18         | 20       |
| Parotid Left           | 143      | 14         | 21       |
| Parotid Right          | 142      | 14         | 21       |
| Trachea                | 118      | 11         | 16       |
| Submandibular Left     | 87       | 11         | 14       |
| Submandibular Right    | 83       | 12         | 13       |
| Oesophagus             | 87       | 10         | 14       |
| Pharyngeal Constrictor | 26       | 1          | 6        |
| Orbit Left             | 63       | 12         | 10       |
| Orbit Right            | 63       | 12         | 10       |
| Optic Nerve Left       | 48       | 10         | 10       |
| Optic Nerve Right      | 48       | 10         | 10       |
| Lens Left              | 64       | 12         | 10       |
| Lens Right             | 64       | 12         | 10       |

### DeepMind (USA scans, UK contour protocols)

|                        | Training | Validation | Hold out |
| ---------------------- | -------- | ---------- | -------- |
| Brain                  | 24       | 5          | 6        |
| Spinal Cord            | 24       | 5          | 6        |
| Mandible               | 24       | 5          | 6        |
| Larynx                 | 0        | 0          | 0        |
| Brainstem              | 24       | 5          | 6        |
| Parotid Left           | 24       | 5          | 6        |
| Parotid Right          | 24       | 5          | 6        |
| Trachea                | 0        | 0          | 0        |
| Submandibular Left     | 24       | 5          | 6        |
| Submandibular Right    | 24       | 5          | 6        |
| Oesophagus             | 0        | 0          | 0        |
| Pharyngeal Constrictor | 0        | 0          | 0        |
| Orbit Left             | 24       | 5          | 6        |
| Orbit Right            | 24       | 5          | 6        |
| Optic Nerve Left       | 24       | 5          | 6        |
| Optic Nerve Right      | 24       | 5          | 6        |
| Lens Left              | 24       | 5          | 6        |
| Lens Right             | 24       | 5          | 6        |

## Empirical investigation

Results on a set of clinical hold-out data were provided to Chris O’Brien
Lifehouse within the DICOM file format for direct comparison to the original
contours. Upon empirical investigation the contours were deemed adequate and
approximately on-par with the other commercial solutions that were compared to.

Notably this on-par result was achieved by utilising a relatively small dataset
built from the combination of standard clinical data and an open access
dataset. The competition software suites were utilising large meticulously
curated datasets.

## Metrics based results

For the metrics based results given here only the structures which exist within
the DeepMind dataset will be considered.

Below is detailed the box-plot comparisons for both the validation and hold-out
datasets utilising both the Dice and the Hausdorff (95%) metrics. These are
then compared to a commercial vendor via results published within the
literature {cite:ps}`wong2020comparing`.

### Structures deemed ready

From investigation of the validation dataset all of the DeepMind structures
except the submandibulars were deemed to meet the requirements for use. For
each of those structures deemed ready, the results are presented herein.

### Results compared to commercial software in the current literature

All of the following metrics are calculated in 3D. The DeepMind dataset has
slice thicknesses of 2.5 mm, as such, disagreement of where a certain structure
starts/ends superiorly/inferiorly on a given slice results in ~multiples of 2.5
mm values for the Hausdorff distance.

The following figures compare the `lifehouse-0.2.0` model detailed within this
validation report to results found within the literature
{cite:ps}`wong2020comparing`. Of note, there was post-processing undergone
within the literature results to force the inferior borders of the brainstem
and spinal cord to match each other. No such post processing was undergone
within the results from the `lifehouse-0.2.0` model.

```{figure} img/val/optic-nerves-dice.png
:name: optic-nerves-dice

The Dice score comparison for the optic nerves.
```

```{figure} img/val/optic-nerves-hausdorff.png
:name: optic-nerves-hausdorff

The Hausdorff comparison for the optic nerves.
```

```{figure} img/val/parotids-dice.png
:name: parotids-dice

The Dice score comparison for the parotids.
```

```{figure} img/val/parotids-hausdorff.png
:name: parotids-hausdorff

The Hausdorff comparison for the parotids.
```

```{figure} img/val/orbits-dice.png
:name: orbits-dice

The Dice score comparison for the orbits.
```

```{figure} img/val/orbits-hausdorff.png
:name: orbits-hausdorff

The Hausdorff comparison for the orbits.
```

```{figure} img/val/spinal-cord-dice.png
:name: spinal-cord-dice

The Dice score comparison for the spinal cord.
```

```{figure} img/val/spinal-cord-hausdorff.png
:name: spinal-cord-hausdorff

The Hausdorff comparison for the spinal cord.
```

```{figure} img/val/brainstem-dice.png
:name: brainstem-dice

The Dice score comparison for the brainstem.
```

```{figure} img/val/brainstem-hausdorff.png
:name: brainstem-hausdorff

The Hausdorff comparison for the brainstem.
```

```{figure} img/val/brain-and-mandible.png
:name: brain-and-mandible

The Dice score and Hausdorff results for the brain and mandible.
```

```{figure} img/val/lenses.png
:name: lenses

The Dice score and Hausdorff results for the lenses.
```

## Conclusion

As an initial model the `lifehouse-0.2.0` model is competitive with current
commercial offerings while only being built with a relatively small dataset
which is the combination of a standard clinical dataset and an open access
dataset.

## References

```{bibliography}
:filter: docname in docnames
```
