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
  attrs = []
  for network in networks:
    for calcName in network["calculations"]:
      if not(calcName in attrs):
        attrs.append(calcName)
  res = "";
  for attr in attrs:
    res += "  <option value=\"" + attr + "\">" + attr + "</option>\n"
  return res

# Removes non-numerical data from network calculations and prepares them for JSON-serialization
def stripNetworks(networks):
  for i in range(0, len(networks)):
    networks[i]["_id"] = None
    for calcName, calcValue in networks[i]["calculations"].iteritems():
      for subcalcName, subcalcValue in calcValue["data"].iteritems():
        if type(subcalcValue) == dict or type(subcalcValue) == list:
          networks[i]["calculations"][calcName]["data"][subcalcName] = None
  return json.dumps(networks).replace("'", " ")

def render(b64=""):
  nList = json.loads(base64.b64decode(b64))
  networks = []
  for nHash in nList:
    networks.append(dbQuery.getNetwork(nHash))
  attrOptions = genAttrOptions(networks)
  return render_template("resCorrelations.html", conf=conf, networks=networks,
      attrOptions=attrOptions, suboptionDeclarations=genSubopts(networks),
      strippedNetworks=stripNetworks(networks))
