# Jinja Setup
#
# Registers some functions that are used in the Jinja templating system by the site

import base64, json
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

# bMin and bMax are just like normal python min/max but convert booleans to
# javaScript-style "false" and "true".

def bMin(inArr):
  res = min(inArr)
  if type(res) == bool:
    return str(res).lower() # convert to javascript-style boolean
  return res

def bMax(inArr):
  res = max(inArr)
  if type(res) == bool:
    return str(res).lower() # convert to javascript-style boolean
  return res

# Installs the filters in the global Jinja environment
def register(environment):
  environment.line_statement_prefix = '%'

  environment.filters["count"] = countFilter
  environment.filters["commas"] = commaFilter
  environment.filters["len"] = len
  environment.filters["int"] = int
  environment.filters["min"] = bMin
  environment.filters["max"] = bMax
  environment.filters["b64e"] = base64.b64encode
  environment.filters["b64d"] = base64.b64decode
  environment.filters["jsone"] = json.dumps
  environment.filters["jsond"] = json.loads

  environment.tests["validCalc"] = calcExists
