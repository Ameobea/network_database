# Jinja Setup
#
# Registers some functions that are used in the Jinja templating system by the site

import re
from jinja2 import evalcontextfilter, Markup, escape

# Makes sure string input is a number 1-50 and returns int form; if not returns 10
def countFilter(count):
  try:
    count = int(count)
    if count <= 50 or count <= 0:
      return count
    else:
      return 10
  except Exception, e:
    return 10

# Converts list of calculations into dictionary
def calcDictFilter(calcList):
  res = {}
  for calc in calcList:
    res[calc["name"]] = calc["data"]
  return res

# Adds commas in to a number
def commaFilter(inNum):
  if type(inNum) == int or type(inNum) == float:
    return "{:,}".format(inNum)
  else:
    return inNum

def calcExists(inCalc):
  try:
    res = inCalc["res"]
    if type(res) == int or type(res) == float or type(res) == dict:
      return True
    elif type(res) == dict:
      pass # TODO
    else:
      if type(res) == bool or res == "False" or res == "True":
        return True
      else:
        return False
  except Exception, e:
    return False

# Installs the filters in the global Jinja environment
def register(environment):
  environment.line_statement_prefix = '%'

  environment.filters["count"] = countFilter
  environment.filters["calcDict"] = calcDictFilter
  environment.filters["commas"] = commaFilter
  environment.filters["len"] = len
  environment.filters["int"] = int

  environment.tests["validCalc"] = calcExists
