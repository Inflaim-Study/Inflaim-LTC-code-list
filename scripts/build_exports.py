#!/usr/bin/env python3
"""Build and check the InflAIM codelist downloads.

The three maintained files are:

    conditions.csv
    master/primary_care.csv
    master/hes_icd10.csv

Everything else (per-condition files, the combined file, conditions.json and the
summary files in metadata/) is generated from them by this script.

    python scripts/build_exports.py           # rebuild the generated files
    python scripts/build_exports.py --check   # check, without changing anything

The checks cover file structure and consistency only. They do not check whether a
code is clinically appropriate. Requires Python 3.8+ and the standard library only.
"""
from pathlib import Path
import argparse
import collections
import csv
import json
import re
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]

CONDITION_FIELDS = ['condition_id', 'condition_name', 'abbreviation',
                    'inflammatory_condition', 'icd10_range', 'folder_name']
PRIMARY_FIELDS = ['condition_id', 'condition_name', 'MedCodeId', 'SnomedCTConceptId',
                  'SnomedCTDescriptionId', 'OriginalReadCode', 'CleansedReadCode', 'Term']
HES_FIELDS = ['condition_id', 'condition_name', 'icd10_block', 'icd10_code', 'hes_code', 'description']
SOURCE_FIELDS = ['condition_id', 'condition_name', 'source', 'source_condition_names', 'source_link', 'notes']

# Code columns reported in metadata/overlapping_codes.csv
CODE_COLUMNS = [('primary_care', 'MedCodeId'), ('primary_care', 'SnomedCTConceptId'),
                ('primary_care', 'OriginalReadCode'), ('primary_care', 'CleansedReadCode'),
                ('hes', 'hes_code')]


class CheckFailed(Exception):
    pass


def require(condition, message):
    if not condition:
        raise CheckFailed(message)


def read_csv(path, expected_fields):
    require(path.is_file(), f'{path.relative_to(ROOT)} is missing.')
    with path.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        require(reader.fieldnames == expected_fields,
                f'{path.relative_to(ROOT)}: columns are {reader.fieldnames}, expected {expected_fields}.')
        rows = list(reader)
    for i, row in enumerate(rows, start=2):
        for key, value in row.items():
            require(value is not None and key is not None,
                    f'{path.relative_to(ROOT)} line {i}: wrong number of columns.')
            require(value == value.strip(),
                    f'{path.relative_to(ROOT)} line {i}: leading or trailing space in {key}.')
            require('Ã' not in value and '�' not in value,
                    f'{path.relative_to(ROOT)} line {i}: possible character-encoding error in {key}.')
    return rows


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def validate(conditions, primary, hes, sources):
    require(len(conditions) == 60, f'conditions.csv has {len(conditions)} conditions, expected 60.')
    for field in ('condition_id', 'condition_name', 'abbreviation', 'folder_name'):
        values = [c[field] for c in conditions]
        require(all(values), f'conditions.csv: empty {field}.')
        dupes = [v for v, n in collections.Counter(values).items() if n > 1]
        require(not dupes, f'conditions.csv: duplicate {field}: {dupes}.')
    for c in conditions:
        require(re.fullmatch(r'ltc_\d{3}', c['condition_id']), f"Bad condition_id {c['condition_id']!r}.")
        require(c['inflammatory_condition'] in ('Y', 'N'),
                f"{c['condition_id']}: inflammatory_condition must be Y or N.")
        require(re.fullmatch(r'[a-z0-9_]+', c['folder_name']), f"{c['condition_id']}: bad folder_name.")

    names = {c['condition_id']: c['condition_name'] for c in conditions}
    for label, rows in (('master/primary_care.csv', primary), ('master/hes_icd10.csv', hes),
                        ('metadata/sources.csv', sources)):
        for row in rows:
            require(names.get(row['condition_id']) == row['condition_name'],
                    f"{label}: {row['condition_id']} / {row['condition_name']!r} does not match conditions.csv.")
        missing = set(names) - {r['condition_id'] for r in rows}
        require(not missing, f'{label}: no rows for {sorted(missing)}.')
    require(len(sources) == len(conditions), 'metadata/sources.csv: expected one row per condition.')

    for row in primary:
        for key in ('MedCodeId', 'SnomedCTConceptId', 'SnomedCTDescriptionId'):
            require(row[key].isdigit(), f"primary care: {key} {row[key]!r} is not a whole number.")
        require(row['OriginalReadCode'] and row['Term'], f"primary care: missing value for {row['MedCodeId']}.")
    for row in hes:
        require(all(row.values()), f"HES: missing value for {row['icd10_code']!r}.")
        require(re.fullmatch(r'[A-Z]\d\d\.[0-9X]', row['icd10_code']),
                f"HES: unexpected ICD-10 format {row['icd10_code']!r}.")
        require(row['icd10_code'].replace('.', '') == row['hes_code'],
                f"HES: hes_code {row['hes_code']!r} does not match icd10_code {row['icd10_code']!r}.")
        # This field preserves the source grouping. Some condition-related
        # codes are in another chapter; containment is not a validity rule.

    for label, rows, key in (('primary care', primary, ('condition_id', 'MedCodeId')),
                             ('HES', hes, ('condition_id', 'hes_code'))):
        seen = collections.Counter(tuple(r[k] for k in key) for r in rows)
        dupes = [k for k, n in seen.items() if n > 1]
        require(not dupes, f'{label}: code listed twice for the same condition: {dupes[:5]}.')


def generate(destination):
    conditions = read_csv(ROOT / 'conditions.csv', CONDITION_FIELDS)
    primary = read_csv(ROOT / 'master' / 'primary_care.csv', PRIMARY_FIELDS)
    hes = read_csv(ROOT / 'master' / 'hes_icd10.csv', HES_FIELDS)
    sources = read_csv(ROOT / 'metadata' / 'sources.csv', SOURCE_FIELDS)
    validate(conditions, primary, hes, sources)

    by_id = {c['condition_id']: c for c in conditions}
    rows_by_source = {'primary_care': primary, 'hes': hes}

    # One folder per condition
    counts = []
    for c in conditions:
        p = [r for r in primary if r['condition_id'] == c['condition_id']]
        h = [r for r in hes if r['condition_id'] == c['condition_id']]
        folder = destination / 'codelists' / c['folder_name']
        write_csv(folder / 'primary_care.csv', PRIMARY_FIELDS, p)
        write_csv(folder / 'hes_icd10.csv', HES_FIELDS, h)
        counts.append({'condition_id': c['condition_id'], 'condition_name': c['condition_name'],
                       'abbreviation': c['abbreviation'], 'folder_name': c['folder_name'],
                       'n_medcodeids': len({r['MedCodeId'] for r in p}),
                       'n_snomed_concepts': len({r['SnomedCTConceptId'] for r in p}),
                       'n_hes_codes': len({r['hes_code'] for r in h})})
    write_csv(destination / 'metadata' / 'condition_counts.csv', list(counts[0]), counts)

    # Combined file
    fields = ['condition_id', 'condition_name', 'abbreviation', 'data_source'] + PRIMARY_FIELDS[2:] + HES_FIELDS[2:]
    combined = []
    for source, rows in rows_by_source.items():
        for row in rows:
            out = dict.fromkeys(fields, '')
            out.update(row)
            out.update(abbreviation=by_id[row['condition_id']]['abbreviation'], data_source=source)
            combined.append(out)
    write_csv(destination / 'combined' / 'all_codelists.csv', fields, combined)

    # Condition list as JSON
    write_json(destination / 'conditions.json', conditions)

    # Codes that appear in more than one condition
    overlaps, summary_codes = [], {}
    for source, column in CODE_COLUMNS:
        members = collections.defaultdict(set)
        for row in rows_by_source[source]:
            if row[column]:
                members[row[column]].add(row['condition_id'])
        shared = {code: ids for code, ids in members.items() if len(ids) > 1}
        summary_codes[column] = {'distinct_codes': len(members), 'codes_in_more_than_one_condition': len(shared)}
        for code in sorted(shared):
            for cid in sorted(shared[code]):
                overlaps.append({'code_column': column, 'code': code,
                                 'condition_id': cid, 'condition_name': by_id[cid]['condition_name']})
    write_csv(destination / 'metadata' / 'overlapping_codes.csv',
              ['code_column', 'code', 'condition_id', 'condition_name'], overlaps)

    summary = {
        'conditions': len(conditions),
        'inflammatory_conditions': sum(c['inflammatory_condition'] == 'Y' for c in conditions),
        'primary_care_rows': len(primary),
        'primary_care_rows_without_CleansedReadCode': sum(not r['CleansedReadCode'] for r in primary),
        'hes_rows': len(hes),
        'combined_rows': len(combined),
        'codes': summary_codes,
        'note': 'Structural checks only; codes have not been clinically re-validated by this script.',
    }
    write_json(destination / 'metadata' / 'summary.json', summary)
    return summary


def check():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        summary = generate(tmp)
        expected = {p.relative_to(tmp) for p in tmp.rglob('*') if p.is_file()}
        existing = {p.relative_to(ROOT) for p in (ROOT / 'codelists').rglob('*') if p.is_file()}
        stray = existing - {p for p in expected if p.parts[0] == 'codelists'}
        require(not stray, f'Files in codelists/ that the build does not produce: {sorted(map(str, stray))[:5]}.')
        for rel in sorted(expected):
            require((ROOT / rel).is_file(), f'{rel} is missing. Run: python scripts/build_exports.py')
            require((ROOT / rel).read_bytes() == (tmp / rel).read_bytes(),
                    f'{rel} is out of date. Run: python scripts/build_exports.py')
    return summary


def main():
    parser = argparse.ArgumentParser(description='Build and check the InflAIM codelist downloads.')
    parser.add_argument('--check', action='store_true',
                        help='check that generated files are up to date, without changing anything')
    args = parser.parse_args()
    try:
        summary = check() if args.check else generate(ROOT)
    except CheckFailed as error:
        sys.exit(f'Check failed: {error}')
    print(json.dumps(summary, indent=2))
    print('All checks passed.' if args.check else 'Generated files updated.')


if __name__ == '__main__':
    main()
