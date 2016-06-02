# Jinja Setup
#
# Registers some functions that are used in the Jinja templating system by the site

import re
from jinja2 import evalcontextfilter, Markup, escape

def countFilter(count):
  try:
    count = int(count)
    if count <= 50:
      return count
    else:
      return 10
  except Exception, e:
    return 10

def register(environment):
  environment.line_statement_prefix = '%'

  environment.filters["count"] = countFilter
