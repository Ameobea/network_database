# Network Database Web Interface
This is the database and web UI for the network research project.  Its purpose is to hold networks and network calculations created from the processing pipeline and to present it a simple and accessible format.

## Overview
The web interface has the function of connecting with the database and providing a way for users to both insert their own networks into the database as well as search through networks submitted by others.  Submitted networks are sent through the processing pipeline first.  After that, they are inserted into the database and the calculated stats are used to attempt to classify it.

For users, each network will have a data page listing all of the calculated metrics and including graphs and other visualizations that both show the static statistics as well as how it fits in the models created from the other networks.

## Technical Specifications
The database itself is built on top of MongoDB, a document-based database very popular for its simplicity and utility.  The web server is Flask-based and will interface directly with the database backend.  For now, Highcharts will be used for the frontend visualizations.  Cutestrap is used as a CSS framework.

## Installation
1. `(sudo) pip install flask`
1. `(sudo) pip install pymongo`
