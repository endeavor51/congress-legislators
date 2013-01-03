#!/usr/bin/env python

# Use the House' member labels file to update some basic info, including bioguide IDs, for members.

# Assumes state and district are already present.

import csv
import utils
from utils import download, load_data, save_data, parse_date


house_labels = "labels-113.csv"

# default to not caching
cache = utils.flags().get('cache', False)
force = not cache

y = load_data("legislators-current.yaml")
by_district = { }
for m in y:
  last_term = m['terms'][-1]
  if last_term['type'] != 'sen':
    full_district = "%s%02d" % (last_term['state'], int(last_term['district']))
    by_district[full_district] = m


for rec in csv.DictReader(open(house_labels)):
  full_district = rec['113 ST/DIS']

  # empty seat - IL-02
  if not by_district.has_key(full_district):
    continue

  by_district[full_district]['terms'][-1]['office'] = rec["ADDRESS"]
  by_district[full_district]["name"]["first"] = rec["FIRST"]
  if rec["MIDDLE"]:
    by_district[full_district]["name"]["middle"] = rec["MIDDLE"]
  by_district[full_district]["name"]["last"] = rec["LAST"]
  by_district[full_district]["id"]["bioguide"] = rec["BIOGUIDE ID"]
  print "[%s] Saved" % full_district

save_data(y, "legislators-current.yaml")