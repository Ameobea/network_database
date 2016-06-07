# Database interface
#
# Casey Primozic
#
# Contains functions pertaining to the database and allowing easier access to it.

import sys
from os import path
from pymongo import MongoClient

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from helpers import conf

def getDb():
  client = MongoClient(conf.MONGO_ADDRESS, conf.MONGO_PORT)
  return client[conf.MONGO_DATABASE]

# Returns a network from the database with the given hash.
# If it doesn't exist, returns False.
def getNetwork(networkHash):
  db = getDb()
  res = db.networks.find_one({"hash": networkHash})
  if res != None:
    return res
  else:
    return False

# Returns a list of the hashes of the first `limit` networks in the database
def getNetworkList(limit, sortBy, sortDirection, start):
  if sortBy != "name" and sortBy != "hash" and sortBy != "uploadDate":
    sortBy = "name"
  if sortDirection == "forward":
    sortDirection = 1
  else:
    sortDirection = -1
  db = getDb()
  cursor = db.networks.find().skip(start).limit(limit).sort(sortBy, sortDirection)
  networks = []
  for network in cursor:
    networks.append(network["hash"])
  return networks

# Wipes ALL data from database.  Yeah, be careful.
def flush():
  db = getDb()
  db.dropDatabase()
