# Inflaim Project: LTC Codelist Repository

**Version:** 1.0  
**Date:** 2025-04-02

## Overview

This repository contains the generated, curated, multi-system medical codelists for the 63 Long-Term Conditions (LTCs) defined for the Inflaim research project. These codelists are designed to support epidemiological analyses and research within the Inflaim project by providing standardized definitions of conditions recorded in UK primary care datasets.

The codelists harmonise terms from several key clinical coding systems:

-   **Read Code Version 2 (CTV2)**
-   **SNOMED CT (UK Clinical Extension & International Edition)**
-   **ICD-10**
-   **CPRD Aurum MedCodes**

These curated code sets facilitate consistent patient identification and precise cohort definition, particularly within UK primary care datasets like CPRD Aurum. They were developed through a process combining established literature review with targeted mapping and clinical validation, aiming for comprehensiveness and clinical relevance across all 63 target conditions.

**Note:** This repository currently provides the initial version of the curated codelists and a reference file detailing their origin. The full details of the development methodology, including the supporting code used for their generation, will be made publicly available alongside our forthcoming publication.

## Repository Contents

This repository contains the final curated medical codelists and a reference file detailing their development source.

1.  **`Inflaim_LTCs__mapping_reference.csv`**: This file lists the 63 Long-Term Conditions and provides a reference for the source or methodology used to develop their respective codelists. For conditions whose codelist was adopted from existing literature, this file references the original publication or source. For conditions where the codelist was developed using the project's semi-automated methodology, this is indicated. This file serves as a provenance record for the codelists provided.

2.  **`Inflaim_Conditions_CodeList.csv`**: This is the master codelist file containing the final, curated mappings for all 62 LTCs across Read V2, SNOMED CT, ICD-10, and CPRD MedCodes in a single file. 

3.  **`Inflaim_codes/`**: This directory contains condition-specific CSV files, organised by condition name and coding system (e.g., separate subdirectories for Read codes, SNOMED CT, and ICD-10). These files offer the same information as the master codelist but separated for easier access to specific subsets.


## Accompanying Publication

A detailed manuscript describing the methodology used to generate and clinically validate the Inflaim LTC codelists is in preparation. The supporting code will be released concurrently with this publication.

## Repository Structure

```plaintext
├── data/
│   └── output/
│       ├── Inflaim_Conditions_CodeList_YYYYMMDD.csv # Master curated codelist
│       ├── Inflaim_LTCs__mapping_reference.csv       # Codelist source/methodology reference
│       └── Inflaim_codes/                         # Condition-specific codelist files
│           ├── [ConditionName]/
│           │   ├── Read/[ConditionName]_Read.csv
│           │   ├── SNOMED/[ConditionName]_SNOMED.csv
│           │   └── ICD10/[ConditionName]_ICD10.csv
│           └── ...
├── README.md