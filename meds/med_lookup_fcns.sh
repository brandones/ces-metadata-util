function medlookup { grep -i "$1" results/meds-matches-* ; }
function medgrep { grep -i $1 input/HUM_Drug_List-13.csv input/meds-ciel.json ; }
function medgrep2 { grep -i $1 HUM_Drug_List-13.csv meds-ciel.json | grep -i $2 ; }
