# Returns the attributes and calculations for a selected set of networks
# in CSV or JSON format.

import sys, hashlib, json, base64
from os import path
from flask import render_template, Response

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from helpers import dbQuery, conf

# Generates an export shortlink for a specific set of input
# networks that leads to an export API endpoint
# Takes two strings as input
def shortlinkGen(inStr):
  payload = base64.urlsafe_b64encode(inStr)
  shortlink = hashlib.sha256(inStr).hexdigest()[:8]
  dbQuery.storeShortlink(shortlink, payload)
  return shortlink

# Serves API endpoint given a shortlink
def shortlinkServe(dFormat, shortlink):
  payload = base64.b64decode(dbQuery.getShortlinkPayload(shortlink))
  print payload
  if payload == None:
    return render_template("shortlinkError.html", conf=conf)
  else: # If shortlinks are expanded to more API than just export, this will need expansion (and moving to different file)
    nList = json.loads(payload)
    cursor = dbQuery.getNetworks(nList, {"_id": 0})
    networks = []
    for network in cursor:
      networks.append(network)
    if dFormat == "csv":
      return csvGen(networks)
    elif dFormat == "json":
      return jsonGen(networks)
    else:
      return render_template("error.html", conf=conf)

def csvGen(networks):
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
        if split[0] in network["calculations"] and split[1] in network["calculations"][split[0]]["data"] and \
            type(network["calculations"][split[0]]["data"][split[1]]) != dict and \
            type(network["calculations"][split[0]]["data"][split[1]]) != list:
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
      res += ","
    res = res[:-1] + "\n"
  return Response(res, mimetype="text/plain")

def jsonGen(networks):
  return json.dumps(networks) # LOL so easy
