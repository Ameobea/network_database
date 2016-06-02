# Network Utilities
#
# Various helper functions for dealing with network data

def getCalcByName(network, name):
  for calc in network:
    if calc["name"] == name:
      return calc
