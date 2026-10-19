# InflAIM long-term condition codelists

Codelists for 60 long-term conditions used in the InflAIM research programme, covering UK primary care and hospital records. The condition framework classifies 17 conditions as inflammatory.

Primary care files contain CPRD Aurum MedCodeIds, SNOMED CT identifiers and Read v2 code fields. Hospital Episode Statistics (HES) files contain ICD-10 codes for the same conditions.

The primary care codelist development is described in the [published paper](https://doi.org/10.1186/s13104-025-07626-0). The HES codelists are under review and may change.

## Files

| File or folder | Contents |
|---|---|
| [conditions.csv](conditions.csv) | Condition names, IDs, abbreviations and inflammatory classification |
| [conditions.json](conditions.json) | The same condition list in JSON format |
| [primary_care.csv](primary_care.csv) | Primary care codes for all conditions |
| [hes_icd10.csv](hes_icd10.csv) | HES ICD-10 codes for all conditions |
| [combined/all_codelists.csv](combined/all_codelists.csv) | Primary care and HES records together, identified by data source |
| [codelists/](codelists/) | Separate primary care and HES files for each condition |
| [metadata/](metadata/) | Sources, alternative condition names, code counts and review records |

Each condition folder contains `primary_care.csv` and `hes_icd10.csv`. For example, see the [diabetes files](codelists/diabetes/).

## Using the files

1. Download the combined file, a complete primary care or HES list, or the files for an individual condition.
2. Import code identifiers as **text** to preserve long numbers and punctuation.
3. Match against the appropriate code column for your dataset. HES files provide dotted ICD-10 codes, such as `E27.2`, and codes without the decimal point, such as `E272`.
4. Record the repository release or commit used in your analysis.

The `condition_id` field links records to the condition list. In `conditions.csv`, `inflammatory_condition` is `Y` for inflammatory conditions and `N` for conditions not classified as inflammatory in the published framework.

See the [column definitions](docs/data_dictionary.md), [import examples](docs/using_files.md) and [methods and matching guidance](docs/methods.md). Use the selected code records rather than assuming that every code within a listed ICD-10 range is included.

## Sources and methods

The condition framework and primary care codelists were developed through literature review, clinical review, and patient and public involvement. The published paper describes the process and the source resources, including CALIBER, the HDR UK Phenotype Library and MULTIPLY.

Condition-level references are listed in [metadata/sources.csv](metadata/sources.csv). Supporting reference files are in [metadata/source_files/](metadata/source_files/).

## Citation

Asfaw D, Davies C, Kulinskaya E, et al. **Harmonising definitions of multiple long term conditions for inflammation research: a co-production approach.** *BMC Research Notes*. 2026;19:53.

[DOI: 10.1186/s13104-025-07626-0](https://doi.org/10.1186/s13104-025-07626-0) | [Full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC12888286/)

Please cite the paper when using the condition framework or primary care codelists, and state the repository release or commit used.

## Funding

This work was supported by the National Institute for Health and Care Research (NIHR), grant NIHR205461. The views expressed are those of the authors and not necessarily those of the NIHR or the Department of Health and Social Care.

## Reuse

See the [reuse notes](docs/reuse.md) for the current licensing status and source terms.

## Questions and corrections

Maintained by the [InflAIM Study team](https://github.com/Inflaim-Study). Please [open an issue](https://github.com/Inflaim-Study/Inflaim-LTC-code-list/issues) to report an error or suggest a correction. Include the condition, code, filename and repository release or commit.
