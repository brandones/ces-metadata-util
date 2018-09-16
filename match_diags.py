#! env/bin/python3
"""
match_diags.py

Attempts to match diagnoses from SSA (Mexican MoH) diagnosis list with
those in the PIH concepts server (icd-pih.csv) and, secondarily, CIEL
(icd-ciel.csv).
"""
import csv
import json
import os
from typing import Dict, List, Tuple

SSA_CSV = os.path.join(".", "input", "diagnoses", "ssa-diagnoses.csv")
PIH_CSV = os.path.join(".", "input", "diagnoses", "pih-diagnoses.csv")
PIH_MATCHES_CSV = os.path.join(".", "output", "diagnoses-matches-pih.csv")
CIEL_CSV = os.path.join(".", "input", "diagnoses", "ciel-diagnoses.csv")
CIEL_MATCHES_CSV = os.path.join(".", "output", "diagnoses-matches-ciel.csv")
OCL_JSON = os.path.join(".", "input", "diagnoses", "who-diagnoses.json")
UNMATCHED_CSV = os.path.join(".", "output", "diagnoses-unmatched.csv")


def main():
    # Make sure the directories we're going to use exist
    os.makedirs(os.path.join(".", "output"), exist_ok=True)

    # Match the SSA diagnoses with existing PIH diagnoses
    ssa_data = clean_csv_list(csv_as_list(SSA_CSV))

    pih_data = clean_csv_list(csv_as_list(PIH_CSV))
    pih_id_to_ssa_name, unmatched_ssa_data = match_on_icd_code(ssa_data, pih_data)
    print("Found {} matches from PIH concepts".format(len(pih_id_to_ssa_name)))
    print(str(len(unmatched_ssa_data)) + " unmatched")
    write_to_csv(pih_id_to_ssa_name, PIH_MATCHES_CSV)

    # Match the remaining SSA diagnoses with diagnoses from the CIEL
    # diagnoses that PIH has
    ciel_data = clean_csv_list(csv_as_list(CIEL_CSV))
    ciel_id_to_ssa_name, unmatched_ssa_data = match_on_icd_code(
        unmatched_ssa_data, ciel_data
    )
    print("Found {} matches from CIEL concepts".format(len(ciel_id_to_ssa_name)))
    print(str(len(unmatched_ssa_data)) + " unmatched")
    write_to_csv(ciel_id_to_ssa_name, CIEL_MATCHES_CSV)

    # Match the remaining SSA diagnoses with diagnoses from the WHO,
    # as represented on the OCL website
    ocl_data = from_json_file(OCL_JSON)
    formatted_ocl_data = [
        (l["from_concept_code"], l["to_concept_code"]) for l in ocl_data
    ]
    ocl_ciel_id_and_ssa_name, unmatched_ssa_data = match_on_icd_code(
        unmatched_ssa_data, formatted_ocl_data
    )
    print(
        "Found {} matches from OCL CIEL concepts".format(len(ocl_ciel_id_and_ssa_name))
    )
    print(str(len(unmatched_ssa_data)) + " unmatched")
    write_to_csv(ocl_ciel_id_and_ssa_name, CIEL_MATCHES_CSV)

    write_to_csv(unmatched_ssa_data, UNMATCHED_CSV)


def match_on_icd_code(
    ssa_data: List[List], concept_data: List
) -> Tuple[List[Tuple], List]:
    """
    Given the SSA diagnosis data and the concept_id to icd_code mappings
    from PIH or CIEL, this finds appropriate matches based on the icd_code.

    Args:
        ssa_data (list): data from the CSV file
        concept_data (list): (concept_id, icd_code) from PIH or CIEL

    Returns:
        matches (list[tuple]): (concept_id, ssa_name) tuples
        unmatched_ssa (list): entries from ssa_data which were not matched
    """
    icd_code_to_ssa_name = {fix_ssa_icd_code(l[2]): l[4] for l in ssa_data}

    # Put concept_data into a dict, which will de-duplicate on ICD code
    icd_code_to_concept_id = {l[1]: l[0] for l in concept_data}

    concept_id_and_ssa_name = [
        (c[1], icd_code_to_ssa_name[c[0]])
        for c in icd_code_to_concept_id.items()
        if c[0] in icd_code_to_ssa_name
    ]
    selected_concept_ids = [l[0] for l in concept_id_and_ssa_name]
    selected_icd_codes = [
        k for k, v in icd_code_to_concept_id.items() if v in selected_concept_ids
    ]
    unmatched = [
        l for l in ssa_data if fix_ssa_icd_code(l[2]) not in selected_icd_codes
    ]
    return concept_id_and_ssa_name, unmatched


def print_dict_items(data: Dict, limit: int):
    """ Prints `limit` items from `data` """
    print([[k, v] for k, v in data.items()][:limit])


def csv_as_list(filename: str):
    """ Returns a list representation of the CSV data at `filename` """
    with open(filename, "rt", encoding="utf8") as csvfile:
        reader = csv.reader(csvfile)
        return list(reader)


def clean_csv_list(input_list: List):
    """Drops blank lines & the header line"""
    return [l for l in input_list if l != []][1:]


def from_json_file(filename: str):
    """ Returns a dict representation of the JSON data at `filename` """
    with open(filename) as f:
        return json.load(f)


def fix_ssa_icd_code(code: str):
    """
    Fixes SSA's wierd ICD code representation.

    They're supposed to look like 'K73.0', but SSA represents them like
    'K730'. Prints the code with a warning if it is longer than 4 characters.
    """
    if len(code) == 3:
        return code
    else:
        if len(code) > 4:
            print("Weird SSA ICD code: " + code)
        return code[:3] + "." + code[3:]


def write_to_csv(data: List, filename: str):
    """ Writes `data` to a new CSV file at `filename`. """
    with open(filename, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


if __name__ == "__main__":
    main()
