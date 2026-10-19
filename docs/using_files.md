# Importing files

Read identifiers as text to retain long values and punctuation. Exclude blank values from the chosen identifier column before matching to patient records.

SNOMED CT concept 45157009 has a blank MedCodeId because its CPRD Aurum mapping has not been verified.

## R

```r
pc <- readr::read_csv("primary_care.csv", col_types = readr::cols(.default = "c"))
```

## Python

```python
import pandas as pd
pc = pd.read_csv("primary_care.csv", dtype=str, keep_default_na=False)
```

## Stata

```stata
import delimited "primary_care.csv", stringcols(_all) encoding(utf-8) clear
```

## Excel

Use Data → From Text/CSV and set code columns to Text before loading. Opening a CSV directly can round long numeric identifiers. Keep the unchanged source file for reference.

See [methods](methods.md) for matching and analysis decisions.
