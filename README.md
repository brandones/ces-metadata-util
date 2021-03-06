# CES Metadata Utility

Tools for generating Compañeros en Salud metadata for OpenMRS.

If there's a `setup.sh` script in the directory, run that first.

Put raw data in `input`. The scripts use `intermediates` internally.
The scripts output to `output`. Put manually worked-on files in
`results`.

## Medications TODO

- Sort `results/meds-unmatched-ssa-manual.csv` into
   `results/meds-unmatched-ssa-needs.csv` and
   `results/meds-matches-choice-ssa-manual.csv`.
- Ask about `results/meds-unmatched-ces-questions.csv` and the remainder
    of `results/meds-unmatched-ssa-manual.csv`.
- Request concepts for
   `results/meds-unmatched-ces-needs.csv` and
   `results/meds-unmatched-ssa-needs.csv`.
- Create list of CIEL-not-PIH concepts from `results/meds-matches-choice-*`.
- Request concept imports for those, as well as `meds-matches-ciel-*`.
- Assemble final medications table.

## Obtaining Diagnosis Data

Diagnosis ICD-10 codes can be extracted with

```
SELECT crm.concept_id, crt.code
FROM concept_reference_term AS crt
INNER JOIN concept_reference_map as crm
    ON crm.concept_reference_term_id=crt.concept_reference_term_id
WHERE crm.concept_map_type_id=2
    AND crt.code LIKE '___._'
GROUP BY crm.concept_id
INTO OUTFILE '/var/lib/mysql-files/bistenes-ciel-icd-3dig.csv'
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';
```

Diagnosis names can be extracted with

```
SELECT cn.concept_id, cn.name, cn.locale, crt.code
FROM concept_reference_term AS crt
INNER JOIN concept_reference_map as crm ON crm.concept_reference_term_id=crt.concept_reference_term_id
INNER JOIN concept_name AS cn ON cn.concept_id=crm.concept_id
WHERE cn.locale IN ('en', 'es') AND crm.concept_map_type_id=2 AND cn.voided=0 AND crt.code LIKE '___._'
INTO OUTFILE '/var/lib/mysql-files/bistenes-pih-icd-3dig.csv'
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';
```

CIEL Diagnosis data obtained from OpenConceptLab using

```
wget 'http://api.openconceptlab.org/orgs/CIEL/sources/CIEL/concepts/?&conceptClass=Drug&limit=8000'
```
