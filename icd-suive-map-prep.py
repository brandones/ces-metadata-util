import pandas as pd

tbl = pd.read_csv("icd-suive.csv")
new_tbl = tbl

for index, row in tbl.iterrows():
    if row["ICD"].endswith("X"):
        new_part = {
            "ICD": [row["ICD"].replace("X", str(i)) for i in range(10)],
            "SUIVE": [row["SUIVE"]] * 10,
            "Name": [row["Name"]] * 10,
        }
        new_tbl_part = pd.DataFrame(new_part)
        print(new_tbl_part)
        new_tbl.append(new_tbl_part)
new_tbl

for index, row in tbl.iterrows():
    if row["ICD"].endswith("X"):
        new_part = {
            "ICD": [row["ICD"].replace("X", str(i)) for i in range(10)]
            + [row["ICD"].replace(".X", "")],
            "SUIVE": [row["SUIVE"]] * 11,
            "Name": [row["Name"]] * 11,
        }
        new_tbl_part = pd.DataFrame(new_part)
        print(new_tbl_part)
        new_tbl.append(new_tbl_part)

for index, row in tbl.iterrows():
    if row["ICD"].endswith("X"):
        new_part = {
            "ICD": [row["ICD"].replace("X", str(i)) for i in range(10)]
            + [row["ICD"].replace(".X", "")],
            "SUIVE": [row["SUIVE"]] * 11,
            "Name": [row["Name"]] * 11,
        }
        new_tbl_part = pd.DataFrame(new_part)
        print(new_tbl_part)
        new_tbl = pd.concat([new_tbl, new_tbl_part])
new_tbl
new_tbl.to_csv("icd-suive.csv")
