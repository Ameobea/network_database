# Result correlations view controller

import sys, json, base64
from flask import render_template
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from helpers import dbQuery, conf

# generates the suboptions for each calculation from the
# subcalculations like average, max, min, etc.
# Creates JSON-encoded object to be passed into JavaScript world
def genSubopts(networks):
  res = {}
  for network in networks:
    calcs = network["calculations"]
    for calcName, calcValue in calcs.iteritems():
      res[calcName] = []
      for subcalcName, subcalcValue in calcValue["data"].iteritems():
        if subcalcName != "error" and not(calcName in res[calcName]):
          res[calcName].append(subcalcName)
  return json.dumps(res)

# Generates HTML that goes inside of the select dropdown menus for picking which
# attributes to display in the correlation plot.
def genAttrOptions(networks):
  attrs = {}
  for network in networks:
    for calcName in network["calculations"]:
      if not(calcName in attrs):
        attrs[calcName] = network["calculations"][calcName]["clearName"]
  res = "";
  for attrName, attrValue in attrs.iteritems():
    res += "  <option value=\"" + attrName + "\">" + attrValue + "</option>\n"
  return res

# Returns the index of the element in inList that has a hash of hash
# if it doesn't exist, returns -1
def hashListFilter(hashList, inHash):
  for i in range(0,len(hashList)):
    if hashList[i] == inHash:
      return i
      break
  return -1

# Responsible for generating attribute data and displaying it in
# the /data endpoing for two different subcalculations
def data(b64, calc1, subcalc1, calc2, subcalc2):
  nList = json.loads(base64.b64decode(b64))
  calc1name = "calculations." + calc1 + ".data." + subcalc1
  calc2name = "calculations." + calc2 + ".data." + subcalc2
  res1 = dbQuery.getNetworks(nList, {"hash": 1, calc1name: 1, calc2name: 1, "name": 1})

  hashMap = []
  res = []
  for network in res1:
    calculations = network["calculations"]
    try:
      hashMap.append({"hash": network["hash"], "name": network["name"]})
      res.append([calculations[calc1]["data"][subcalc1],
          calculations[calc2]["data"][subcalc2]])
    except Exception, e:
      pass
  return render_template("mixins/attributePairs.html", data=res, hashList=hashMap)

def render(b64=""):
  nList = json.loads(base64.b64decode(b64))
  networks = []
  for nHash in nList:
    networks.append(dbQuery.getNetwork(nHash))
  attrOptions = genAttrOptions(networks)
  return render_template("resCorrelations.html", conf=conf, networks=networks,
      attrOptions=attrOptions, suboptionDeclarations=genSubopts(networks), b64=b64)
