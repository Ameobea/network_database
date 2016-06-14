# Returns the attributes and calculations for a selected set of networks
# in CSV or JSON format.

import sys, hashlib, json, base64, copy
from os import path
from flask import render_template, Response

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from helpers import dbQuery, conf

# Generates an export shortlink for a specific set of input
# networks that leads to an export API endpoint
# Takes two strings as input
def shortlinkGen(headers):
  payload = base64.urlsafe_b64encode(headers["instr"])
  shortlink = hashlib.sha256(headers["instr"]).hexdigest()[:8]
  dbQuery.storeShortlink(shortlink, payload)
  return shortlink

# Serves API endpoint given a shortlink
def shortlinkServe(dFormat, shortlink, request):
  try:
    if request.args.get("pernode") == "true":
      pernode = True
    else:
      pernode = False
    if request.args.get("inserNone") == "true":
      inserNone = True
    else:
      inserNone = False
  except Exception, e:
    pernode = False
    inserNone = False
  payload = base64.b64decode(dbQuery.getShortlinkPayload(shortlink))
  if payload == None:
    return render_template("shortlinkError.html", conf=conf)
  else: # If shortlinks are expanded to more API than just export, this will need expansion (and moving to different file)
    nList = json.loads(payload)
    cursor = dbQuery.getNetworks(nList, {"_id": 0})
    networks = []
    for network in cursor:
      networks.append(network)
    if dFormat == "csv":
      return csvGen(networks, inserNone)
    elif dFormat == "json":
      return jsonGen(networks, pernode)
    else:
      return render_template("error.html", conf=conf)

# Helper function that determines if a subcalculation is numerical
def isNumerical(network, split):
  return split[0] in network["calculations"] and split[1] in network["calculations"][split[0]]["data"] and \
      type(network["calculations"][split[0]]["data"][split[1]]) != dict and \
      type(network["calculations"][split[0]]["data"][split[1]]) != list

def csvGen(networks, inserNone):
  headers = ["name", "hash"]
  rows = []
  for network in networks:
    for calcName, calcValue in network["calculations"].iteritems(): # Fill header list in with missing headers
      for subcalcName, subcalcValue in calcValue["data"].iteritems():
        if not(calcName + "-" + subcalcName in headers) and subcalcName != "error":
          headers.append(calcName + "-" + subcalcName)
  for network in networks:
    row = []
    for header in headers: # Check network for each attribute and fill in order, putting None in for missing data
      if "-" in header: # calculation/attribute
        split = header.split("-")
        if isNumerical(network, split):
          row.append(network["calculations"][split[0]]["data"][split[1]])
        else:
          row.append(None)
      else: # static network property
        if network[header]:
          row.append(network[header])
        else:
          row.append(None)
    rows.append(row)
  res = ""
  for header in headers:
    res += header + ","
  res = res[:-1] + "\n"
  for row in rows:
    for elem in row:
      if elem != None:
        res += str(elem)
      elif inserNone:
        res += "None"
      res += ","
    res = res[:-1] + "\n"
  return Response(res, mimetype="text/plain")

def jsonGen(networks, pernode):
  if not(pernode):
    for i in range(0, len(networks)):
      network = networks[i]
      for calcName, calcValue in network["calculations"].iteritems():
        for subcalcName, subcalcValue in calcValue["data"].iteritems():
          if not(isNumerical(network, [calcName, subcalcName])):
            network["calculations"][calcName]["data"][subcalcName] = None
  return json.dumps(networks) # LOL so easy
