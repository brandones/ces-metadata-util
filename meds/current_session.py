# coding: utf-8
import pandas as dp
import pandas as pd
pd.load_csv('results/meds-ces.csv')
pd.read_csv('results/meds-ces.csv')
ces = pd.read_csv('results/meds-ces.csv')
extant_ciel = pd.read_csv('input/ciel-in-concepts-dict.csv')
extant_ciel
any(extant_ciel[1])
extant_ciel[1]
extant_ciel[0]
extant_ciel.columns.values
extant_ciel = pd.read_csv('input/ciel-in-concepts-dict.csv')
extant_ciel.columns.values
extant_ciel["voided"]
list(extant_ciel["voided"])
any(list(extant_ciel["voided"]))
extant_ciel = extant_ciel[extant_ciel["voided"] == 0]
extant_ciel
ces = ces[ces["concept"].starts_with("CIEL")]
ces = ces[ces.concept.starts_with("CIEL")]
ces = ces[ces.concept.startswith("CIEL")]
ces = ces[ces.concept.str.startswith("CIEL")]
ces = ces[!ces["concept"].isna())
ces = ces[~ces["concept"].isna())
ces = ces[~ces["concept"].isna()]
ces = ces[ces.concept.startswith("CIEL")]
ces = ces[ces.concept.str.startswith("CIEL")]
ces
ces_not_in_dict = ces[ces.concept.str.replace('CIEL:', '') not in extant_ciel]
ces_not_in_dict = ces[~ces.concept.str.replace('CIEL:', '').isin(extant_ciel["ID"])]
ces_not_in_dict
ces_not_in_dict.to_csv('results/ces-drugs-from-ciel.csv')
ssa = ssa[~ssa['concept'].isna()]
ssa
ssa = pd.read_csv('results/meds-ssa.csv')
ssa
ssa = ssa[~ssa['concept'].isna()]
ssa = ssa[ssa.concept.str.startswith('CIEL')]
ssa
ssa.concept
ssa_not_in_dict = ssa[~ssa.concept.str.replace("CIEL:", "").isin(extant_ciel.ID)]
ssa_not_in_dict
ssa_not_in_dict.to_csv("results/ssa-drugs-from-ciel.csv")
ces_not_in_dict.concept.unique()
ces_not_in_dict.concept.unique().to_csv()
pd.DataFrame(ces_not_in_dict.concept.unique()).to_csv('results/ssa-ciel-needs.csv')
pd.DataFrame(ces_not_in_dict.concept.unique()).to_csv('results/ces-ciel-needs.csv')
pd.DataFrame(ssa_not_in_dict.concept.unique()).to_csv('results/ssa-ciel-needs.csv')
get_ipython().run_line_magic('save', 'current_session')
get_ipython().run_line_magic('save', 'current_session 1-48')
all_not_in_dict = ces_not_in_dict["concept"] + ssa_not_in_dict["concept"]
all_not_in_dict
all_not_in_dict = ces_not_in_dict["concept"].concat(ssa_not_in_dict["concept"])
all_not_in_dict = pd.concat([ces_not_in_dict["concept"], ssa_not_in_dict["concept"]])
all_not_in_dict
all_not_in_dict.unique()
all_not_in_dict.unique()
pd.DataFrame(all_not_in_dict.unique()).to_csv("results/ciel-needs.csv")
ces_ready = ces[~ces["concept"].isin(all_not_in_dict)]
ces_ready
ces_ready.to_csv("results/ces-ready.csv")
ssa_ready = ssa[~ssa["concept"].isin(all_not_in_dict)]
ssa_ready.to_csv("results/ssa-ready.csv")
