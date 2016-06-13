# View controller for screener results table

import sys, json, base64
from os import path
from flask import render_template

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from helpers import dbQuery, conf

# converts the json object containing descrimination info into a
# dictionary for use with mongo
#
# It shouldn't be necessary to check the validity of calculation names (since garbage
# ones should just pass through), but if it is necessary a list of all valid
# calculation/attribute names will have to be checked for each element of inDict
def queryGen(in64):
  inDict = json.loads(base64.b64decode(in64))
  res = {"$and": []}
  for calcName, calcValue in inDict.iteritems():
    resName = "calculations." + calcName + ".data.res"
    if "True" in calcValue: # boolean
      if not(calcValue["True"] and calcValue["False"]): # if both true and false checked don't even bother
        resObj = {"$or": [
          {resName: {"$exists": False}},
          {resName: calcValue["True"]} # either one or the other or neither; in any case calcValue["True"] is what it should be
        ]}
        res["$and"].append(resObj)
    else:
      res["$and"].append({"$or": [ # max/min
        {resName: {"$exists": False}}, # if calculation isn't in database
        {resName: {"$gte": calcValue["min"], "$lte": calcValue["max"]}}
      ]})
  return res

def render(args):
  query = queryGen(args.get("descrim"))
  networkList = dbQuery.getNetworkList(0, 0, 0, 0, descrim=query)
  return render_template("mixins/screenResults.html", networkList=networkList, dbQuery=dbQuery, conf=conf)
