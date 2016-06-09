# View controller for the screener page

import sys
from os import path
from flask import render_template

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from helpers import dbQuery, conf

def dHistogram(calcName, clearName, distributions):
  res = "<script type='text/javascript'>\n$(document).ready(function(){\nvar data=["
  data = distributions[calcName]
  for p in data:
    res += str(p["res"]) + ","
  res += "];\n"
  res += (
    "$('#" + calcName + "Histogram').highcharts({\n"
      "title: {text: '" + clearName + " Distibution'},\n"
      "chart: {type: 'histogram'},\n"
      "series: [{data: data}]\n"
    "});\n"
    "});\n"
    "</script>"
    "<div id='" + calcName + "Histogram'></div>"
  )
  return res

def render():
  distributions = dbQuery.getDistributions()
  return render_template("screener.html", conf=conf, dHistogram=dHistogram, distributions=distributions["values"])
