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

This repository contains the final curated medical codelists and a reference file detailing their development source, organized as follows:

1.  **`Inflaim_Conditions_CodeList.csv`**: This is the master codelist file, located in the **root** of the repository. It contains the final, curated mappings for all 63 LTCs across all included coding systems in a single, comprehensive file.  This is a primary file intended for direct use in cohort identification for multiple conditions simultaneously.
2.  **`Inflaim_LTCs__mapping_reference.csv`**: This file, also located in the **root** of the repository, lists the 63 Long-Term Conditions and provides a reference for the source or methodology used to develop their respective codelists. This file serves as a provenance record for the codelists provided.
3.  **`CodeLists/`**: This directory, located in the **root** of the repository, contains the curated codes broken down per condition and per coding system. Inside the `CodeLists/` directory, you will find four subdirectories:
    * **`all_colde_csv/`**: Contains 63 CSV files, one for each condition (e.g., `Diabetes.csv`), where each file lists all the curated codes for that specific condition across all included coding systems combined. *(Note: User provided spelling 'all_colde_csv')*
    * **`Medcode/`**: Contains 63 CSV files, one for each condition (e.g., `Diabetes_Medcode.csv`), listing only the curated CPRD Aurum MedCodes for that condition.
    * **`Readcode/`**: Contains 63 CSV files, one for each condition (e.g., `Diabetes_Readcode.csv`), listing only the curated Read Code Version 2 (CTV2) codes for that condition.
    * **`SnomedCT/`**: Contains 63 CSV files, one for each condition (e.g., `Diabetes_SnomedCT.csv`), listing only the curated SNOMED CT codes for that condition.

## Accompanying Publication

A detailed manuscript describing the methodology used to generate and clinically validate the Inflaim LTC codelists is in preparation. The supporting code will be released concurrently with this publication.

## Repository Structure

```plaintext
├── CodeLists/                                    # Directory containing condition-specific code files
│   ├── all_colde_csv/                            # Contains [ConditionName].csv for each condition (all systems)
│   │   ├── [ConditionName1].csv                 # E.g., Asthma.csv
│   │   └── ...                                 # Files for all 63 conditions
│   ├── Medcode/                                # Contains [ConditionName]_Medcode.csv for each condition
│   │   ├── [ConditionName1]_Medcode.csv         # E.g., Diabetes_Medcode.csv
│   │   └── ...
│   ├── Readcode/                               # Contains [ConditionName]_Readcode.csv for each condition
│   │   ├── [ConditionName1]_Readcode.csv       # E.g., Diabetes_Readcode.csv
│   │   └── ...
│   └── SnomedCT/                               # Contains [ConditionName]_SnomedCT.csv for each condition
│       ├── [ConditionName1]_SnomedCT.csv       # E.g., Diabetes_SnomedCT.csv
│       └── ...
├── Inflaim_Conditions_CodeList_YYYYMMDD.csv # Master curated codelist (all conditions, all systems) - at root
├── Inflaim_LTCs__mapping_reference.csv       # Codelist source/methodology reference (all conditions) - at root
├── README.md                                 # This README file - at root