#! ./env/bin/python
#
# The resulting AH file is generating the error:
#
# Data too long for column 'user_generated_id' at row 1
#

import pandas

raw_locs = pandas.read_csv("input/cat_localidad_JUN2018.csv", encoding="latin1")
our_mun_file = open("input/our-mun-hugo.txt", "r")
our_muns = our_mun_file.readlines()
our_muns = [l.strip().replace(",", "").replace("'", "") for l in our_muns]

our_loc_rows = raw_locs[
    (raw_locs["NOM_ENT"] == "Chiapas") & (raw_locs["NOM_MUN"].isin(our_muns))
]
our_locs = our_loc_rows[
    ["NOM_ENT", "CVE_ENT", "NOM_MUN", "CVE_MUN", "NOM_LOC", "CVE_LOC"]
]

all_mun_duped = raw_locs[["NOM_ENT", "CVE_ENT", "NOM_MUN", "CVE_MUN"]]
all_mun = all_mun_duped.drop_duplicates()
all_mun_except_us = all_mun[~all_mun["NOM_MUN"].isin(our_muns)]

loc_output = [
    row["NOM_ENT"]
    + "^"
    + str(row["CVE_ENT"])
    + "|"
    + row["NOM_MUN"]
    + "^"
    + str(row["CVE_MUN"])
    + "|"
    + row["NOM_LOC"]
    + "^"
    + str(row["CVE_LOC"])
    for index, row in our_locs.iterrows()
]

mun_output = [
    row["NOM_ENT"]
    + "^"
    + str(row["CVE_ENT"])
    + "|"
    + row["NOM_MUN"]
    + "^"
    + str(row["CVE_MUN"])
    for index, row in all_mun_except_us.iterrows()
]

with open("results/mexico_address_hierarchy_entries.csv", "w") as outfile:
    outfile.write("\n".join(loc_output))
    outfile.write("\n".join(mun_output))
