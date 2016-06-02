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
def getNetwork(hash):
  db = getDb()
  cursor = db.networks.find({"hash": hash})
  if cursor.count() > 0:
    return cursor[0]
  else:
    return False

# Returns a list of the hashes of the first `limit` networks in the database
def getNetworkList(limit):
  db = getDb()
  cursor = db.networks.find().limit(limit).sort("hash", 1)
  networks = []
  for network in cursor:
    networks.append(network["hash"])
  return networks
