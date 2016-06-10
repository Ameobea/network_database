# Distribution Calculations
#
# Reads all networks in the database and returns centralized storage of
# all of the statistics in a centralized collection, eliminating the
# need to select every network when retrieving database-wide statistics.

from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from helpers import dbQuery

db = dbQuery.getDb()
# Uses default values
nList = dbQuery.getNetworkList(0, 0, 0, 0, db=db)

distributions = {}

for hash in nList:
  network = dbQuery.getNetwork(hash)
  for calcName, calcData in network["calculations"].iteritems():
    # non-numerical data types and errors are useless/wasteful for this
    if not("error" in calcData["data"]) and type(calcData["data"]["res"]) != dict and \
        type(calcData["data"]["res"]) != list:
      if not(calcName in distributions):
        distributions[calcName] = [calcData["data"]]
      else:
        distributions[calcName].append(calcData["data"])

# replace the distributions collection with an updated copy, creating it if it doesn't exist
db.distributions.update_one({"name": "main"}, {"$set": {"values": distributions}}, upsert=True)
print("Distributions compiled for all networks.")
