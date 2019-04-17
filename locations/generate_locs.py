#! ./env/bin/python

import pandas

raw_locs = pandas.read_csv("input/cat_localidad_JUN2018.csv", encoding="latin1")
our_mun_file = open("input/our-mun.txt", "r")
our_muns = our_mun_file.readlines()
