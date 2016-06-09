# Distribution Calculations
#
# Reads all networks in the database and returns centralized storage of
# all of the statistics in a centralized collection, eliminating the
# need to select every network when retrieving database-wide statistics.

from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from helpers import dbQuery

db = dbQuery.getDb()
nList = dbQuery.getNetworkList(0, 0, 0, 0)

distributions = {}

for hash in nList:
  network = dbQuery.getNetwork(hash)
  for calc in network["calculations"]:
    # non-numerical data types and errors are useless/wasteful for this
    if not("error" in calc["data"]) and type(calc["data"]["res"]) != dict and type(calc["data"]["res"]) != list:
      if not(calc["name"] in distributions):
        distributions[calc["name"]] = [calc["data"]]
      else:
        distributions[calc["name"]].append(calc["data"])

db.distributions.update_one({"name": "main"}, {"$set": {"values": distributions}}, upsert=True)
print("Distributions compiled for all networks.")
