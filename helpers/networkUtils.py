# Network Utilities
#
# Various helper functions for dealing with network data

# returns one named calculation from a list of calculations
def getCalcByName(network, name):
  for calc in network:
    if calc["name"] == name:
      return calc
