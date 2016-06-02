# JSON dump data importer
#
# Casey Primozic
#
# This script imports data from JSON dumps taken from various parts
# of the processing pipeline and imports them into MongoDB.
#
# Usage:
# python jsonToMongo.py -c correlation_results.json -d postAnalysisResults.json

import json, sys, argparse
from pymongo import MongoClient
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from helpers import conf

client = MongoClient(conf.MONGO_ADDRESS, conf.MONGO_PORT)
db = client[conf.MONGO_DATABASE]

mainResultsFilename = False

parser = argparse.ArgumentParser(description='Input filename.')
parser.add_argument("-d")
args = parser.parse_args()
globals().update(vars(args))
if d:
  mainResultsFilename = d

def printUsage():
  print("Usage: python jsonToMongo.py -d postAnalysisResults.json")
  sys.exit(2)

def importMain(filename):
  inFile = open(filename, "r")
  inData = json.load(inFile)
  for networkName, networkData in inData.iteritems():
    networkHash = networkData[0]["hash"]
    cursor = db.networks.find({"hash": networkHash})
    if cursor.count() == 0:
      db.networks.insert_one({"hash": networkHash, "name": networkName, "calculations": networkData})
    else:
      doc = cursor[0]
      for calculation in networkData:
        if not(calculation["name"] in doc):
          doc[calculation["name"]] = calculation["data"]
      db.networks.update_one({"hash": networkHash}, {"$set": doc})


if type(mainResultsFilename) != bool:
  importMain(mainResultsFilename)
else:
  print("No input file was supplied.")
  printUsage()
