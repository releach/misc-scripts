#!/usr/bin/env python
# Submits ontology to OOPS REST service to scan for common ontology errors.

import os
import sys
import xml.etree.ElementTree as ET
import requests

def read_ontology_file():
    """Prompt user for OWL file name, read, and return its content."""
    owl_file = input("Enter OWL filename: ")
    owl_path = os.path.join(os.path.dirname(__file__), owl_file)
    try:
        with open(owl_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File {owl_file} not found.")
        sys.exit(1)

def create_request_xml(ontology):
    """Create XML from ontology."""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<OOPSRequest>
    <OntologyUrl></OntologyUrl>
    <OntologyContent><![CDATA[{ontology}]]></OntologyContent>
    <Pitfalls></Pitfalls>
    <OutputFormat>XML</OutputFormat>
</OOPSRequest>
"""

def call_oops_api(request_xml):
    """Submit the ontology to the OOPS API and handle the response."""
    url = "https://oops.linkeddata.es/rest"
    headers = {"Content-Type": "text/xml"}

    try:
        response = requests.post(url, data=request_xml, headers=headers)
        response.raise_for_status() 
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        sys.exit(1)

    process_response(response.text)

def process_response(response_text):
    """Process the API response, extracting and printing pitfalls."""
    try:
        results_xml = ET.fromstring(response_text)
        pitfalls = results_xml.find('{http://www.oeg-upm.net/oops}Pitfall')
        if pitfalls is None:
            print("The OOPS Pitfall Scanner did not encounter any errors.")
        else:
            print("Errors encountered. See pitfall_report.txt for details.")
            for pitfall in results_xml.iter('{http://www.oeg-upm.net/oops}Pitfall'):
                print_pitfall_info(pitfall)
            with open("pitfall_report.txt", "w") as file:
                file.write(response_text)
    except ET.ParseError as e:
        print(f"Error parsing XML response: {e}")
        sys.exit(1)

def print_pitfall_info(pitfall):
    """Print information about a single pitfall."""
    name = pitfall.find('{http://www.oeg-upm.net/oops}Name').text.strip()
    description = pitfall.find('{http://www.oeg-upm.net/oops}Description').text.strip()
    importance = pitfall.find('{http://www.oeg-upm.net/oops}Importance').text.strip()
    print(f"{importance}\n{name}\n{description}\n")

if __name__ == "__main__":
    ontology = read_ontology_file()
    request_xml = create_request_xml(ontology)
    call_oops_api(request_xml)
