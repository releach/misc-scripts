#!/usr/bin/env python

# Submits ontology to OOPs REST service to scan for common ontology errors.

import os
import os.path
import subprocess
import sys
import xml.etree.ElementTree as ET

import requests


def create_data():
  dirname = os.path.dirname(__file__)
  owl_file = input("Enter owl filename: ")
  with open(os.path.join(dirname, owl_file), 'r') as file:
    ontology = file.read()

  xml = f"""<?xml version="1.0" encoding="UTF-8"?>
  <OOPSRequest>
        <OntologyUrl></OntologyUrl>
        <OntologyContent><![CDATA[{ontology}
  ]]></OntologyContent>
        <Pitfalls></Pitfalls>
        <OutputFormat>XML</OutputFormat>
  </OOPSRequest>

  """
  return xml

def call_api(xml):

  url = "https://oops.linkeddata.es/rest"
  headers = {"Content-Type":"text/xml"}


  r = requests.post(url, data=xml, headers=headers)
  if r:
    resultsXML = ET.fromstring(r.text)
    pitfalls = resultsXML.find('{http://www.oeg-upm.net/oops}Pitfall')
    if pitfalls is None:
      print("The OOPS Pitfall Scanner did not encounter any errors.")
      sys.exit(0)
    else:
      print("The OOPS Pitfall Scanner has encountered errors. See a full error report for more details.\n")
      for pitfall in resultsXML.iter('{http://www.oeg-upm.net/oops}Pitfall'):
        name = (pitfall.find('{http://www.oeg-upm.net/oops}Name').text).strip()
        description = (pitfall.find('{http://www.oeg-upm.net/oops}Description').text).strip()
        importance = (pitfall.find('{http://www.oeg-upm.net/oops}Importance').text).strip()
        print(
          f'{importance}\n'
          f'{name}\n'
          f'{description}\n'
          )
      with open(os.path.expanduser("pitfall_report.txt"), "w") as file:
        file.write(r.text)
      sys.exit(0)
  else:
    print("Could not connect to OOPS Pitfall Scanner. Check that your ontology file is saved as RDF/XML.")
    sys.exit(1)

if __name__ == "__main__":
  xml = create_data()
  call_api(xml)
