# Methods and use

The condition framework and primary care codelist development are described in [Asfaw et al., BMC Research Notes (2026), 19:53](https://doi.org/10.1186/s13104-025-07626-0).

## Primary care

The primary care master contains 7,218 condition–code records and 7,216 distinct MedCodeIds. CPRD Aurum medical code identifiers, SNOMED CT concept identifiers and SNOMED CT description identifiers are separate fields. Read code fields and clinical terms are also provided.

There are 1,126 blank `CleansedReadCode` values. A blank means that no value is available in that field; it does not establish whether an equivalent Read code exists. Check the source dictionary before assigning a replacement.

## Hospital records

The HES master contains 1,641 condition–code records and 1,637 distinct codes. It provides dotted ICD-10 codes and the corresponding representation without the decimal point.

The `icd10_block` field contains source grouping labels and annotations. These are not a uniform ICD-10 block hierarchy and should not be expanded into additional codes. Use the individual code records listed for each condition.

The HES codelists remain under review. The primary care publication does not establish their validation status.

## Conditions

The condition list provides a fixed identifier, name, abbreviation, inflammatory classification and folder name for each condition. It classifies 17 conditions as inflammatory and 43 as not classified as inflammatory in the published framework. Alternative names are recorded in `metadata/condition_aliases.csv`.

Other interstitial pulmonary diseases is the J84 category. Fibrosing alveolitis falls within J84.1, a subset of J84. A condition label alone does not establish that a codelist covers every diagnosis in the category. See the [NHS ICD-10 classification](https://classbrowser.nhs.uk/ICD-10-5TH-Edition/vol1/block-j80-j84.htm) and `metadata/condition_code_review.csv` for the outstanding code review.

## Matching codes

Import identifiers as text. Use the identifier represented in the target dataset:

| Dataset or coding system | Matching column |
|---|---|
| CPRD Aurum medical codes | `MedCodeId` |
| SNOMED CT concepts | `SnomedCTConceptId` |
| Read-coded records | The appropriate Read code field, checked against the source dictionary |
| HES diagnoses | `hes_code`, or `icd10_code` if dotted codes are used |

Do not match SNOMED CT concepts using the description identifier. Confirm Read code representations against the source dictionary rather than assuming a truncation rule.

Match the selected HES codes exactly after confirming the dataset's representation. Expanding a prefix or range would define a different selection and requires separate justification.

Terminology editions and dictionary releases are not recorded in these files. HES diagnosis positions, lookback periods, repeat-event requirements and treatment of historical or resolved diagnoses must be specified for each analysis.

Some codes occur under more than one condition. These are listed in `metadata/overlapping_codes.csv`. Specify how these memberships will be handled when counting conditions per person.

## Maintaining the files

Edit the condition list, the two master CSVs and the relevant source references. Generate the condition files, combined file and summary files with:

```bash
python scripts/build_exports.py
```

Check the generated files without changing them with:

```bash
python scripts/build_exports.py --check
```

The same check runs through GitHub Actions. It checks file structure and consistency; clinical review is a separate process. Keep condition identifiers fixed when editing names or sorting records.
