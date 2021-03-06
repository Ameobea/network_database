# View controller for the comparison page.

import sys
from os import path
from flask import render_template

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from helpers import dbQuery, conf, jinjaSetup

# Take some calculations from various networks and return a formatted HTML
# table row with the results.  To get result `res` from calculation `calc`,
# key should be "calc.res".  Filters are applied to the data that goes inside
# the table cells in order before being escaped and added to the output string.
def statsRow(name, calcDicts, key, jinjaEnv, filters=[]):
  res = "<tr><td>" + name + "</td>"
  i = -1
  for calcDict in calcDicts:
    i += 1
    try:
      point = calcDict
      for deep in key.split("."):
        point = point[deep]
      data = str(point)
      if filters != []:
        for dataFilter in filters:
          data = dataFilter(data)
      res = res + "<td class='col-" + str(i) + "'>" + str(jinjaEnv.filters["e"](data)) + "</td>"
    except Exception, e:
      res += "<td class='col-" + str(i) + "'></td>" # network doesn't have this attribute, so insert empty cell.
  res += "</tr>"
  return res

# do some calculations and inject into template, then return rendered template
def compare(hashString, jinjaEnv, cookies=None):
  if type(hashString) == bool:
    hashString = cookies.get("compare")
  if hashString != None and hashString != "":
    hashString = hashString.replace("%2C", ",")
    networks = []
    calcDicts = []
    for hash in hashString.split(","):
      network = dbQuery.getNetwork(hash)
      if type(network) != bool:
        networks.append(network)
        calcDicts.append(network["calculations"])
    return render_template("compare.html", conf=conf, networks=networks,
        statsRow=statsRow, calcDicts=calcDicts, jinjaEnv=jinjaEnv)
  else:
    return render_template("compareNoNetworks.html", conf=conf)
