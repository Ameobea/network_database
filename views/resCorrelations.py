# Result correlations view controller

import sys, json, base64
from flask import render_template
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from helpers import dbQuery, conf

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

def render(b64=""):
  nList = json.loads(base64.b64decode(b64))
  networks = []
  for nHash in nList:
    networks.append(dbQuery.getNetwork(nHash))

  return render_template("resCorrelations.html", conf=conf, networks=networks,
      attrOptions=genAttrOptions(networks))
