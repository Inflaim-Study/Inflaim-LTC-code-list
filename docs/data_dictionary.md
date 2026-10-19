# Column definitions

Code identifiers are text. Blank fields represent unavailable or inapplicable values, not zero.

## Condition list

| Column | Meaning |
|---|---|
| `condition_id` | Fixed project identifier |
| `condition_name` | Current condition name |
| `abbreviation` | Project abbreviation |
| `inflammatory_condition` | `Y` = inflammatory; `N` = not classified as inflammatory in the published framework |
| `icd10_range` | Summary condition grouping; not an instruction to include all codes in a range |
| `folder_name` | Folder containing the condition's two files |

`conditions.json` contains the same fields and values.

## Primary care

Each row contains one condition–code mapping. All primary care files contain:

| Column | Meaning |
|---|---|
| `condition_id`, `condition_name` | Link to the condition list |
| `MedCodeId` | CPRD Aurum medical code identifier; blank when the mapping is unverified |
| `SnomedCTConceptId` | SNOMED CT concept identifier |
| `SnomedCTDescriptionId` | SNOMED CT description identifier |
| `OriginalReadCode` | Original code field in the supplied mapping |
| `CleansedReadCode` | Cleansed Read field, where supplied |
| `Term` | Clinical term |

## HES

Each row represents one selected condition–code record.

| Column | Meaning |
|---|---|
| `condition_id`, `condition_name` | Link to the condition list |
| `icd10_block` | Grouping label supplied with the original HES file; not a verified uniform WHO block field |
| `icd10_code` | Dotted code supplied in the source |
| `hes_code` | Corresponding HES representation without the decimal point |
| `description` | Description supplied with the code |

## Combined file

`combined/all_codelists.csv` contains all 8,860 records from the two complete lists. It adds `abbreviation` and `data_source` (`primary_care` or `hes`) and retains source-specific fields. Fields from the other source are blank. It does not create pairs of equivalent primary care and HES codes.

## Supporting files

| File | Contents |
|---|---|
| `metadata/condition_counts.csv` | Counts by condition and coding field |
| `metadata/condition_aliases.csv` | Previous names and abbreviations |
| `metadata/condition_code_review.csv` | Code-membership review decisions and mapping limitations |
| `metadata/sources.csv` | Condition-level source summary, including unresolved attribution where applicable |
| `metadata/source_files/` | Supporting source references |
| `metadata/summary.json` | Current data counts and structural-check scope |
