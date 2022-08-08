import os
import json
import sys
import urllib

import snyk
from packageurl import PackageURL


# Ensure you have a Snyk API token
try:
    token = os.environ["SNYK_TOKEN"]
except KeyError:
    sys.exit("You must provide a SNYK_TOKEN to run Snyk Shell")
client = snyk.SnykClient(token, version="2022-04-04~experimental", url="https://api.snyk.io/rest")

# Read the contents from stdin. This is a very simple implementation with a poor user experience
# but is intended for demonstration purposes only
doc = sys.stdin.read()

# The output of --print-deps --json is not a JSON document, it's
# two JSON documents. But their are lots of line breaks in the output
deps, vulns = doc.split("}\n{")
data = json.loads(deps + "}")

# the response contains details of the type of package. We provide
# a lookup here to convert those to the correct purl type where different
lookup = {"mvn": "maven"}

fmt, version = data["packageFormatVersion"].split(":")
purl_type = lookup[fmt] if fmt in lookup else fmt

def extract(dependencies, package_type):
    resp = []
    for dep in dependencies:
        name = dependencies[dep]["name"].replace(":", "/")
        version = dependencies[dep]["version"]
        purl = PackageURL(name=name, version=version, type="maven")
        resp.append(purl)
        for subdep in extract(dependencies[dep]["dependencies"], package_type):
            resp.append(subdep)
    return resp

for purl in extract(data["dependencies"], purl_type):

    # Encode the purl, including encoding forward slashes
    encoded_purl = urllib.parse.quote(purl.to_string(), safe="")
    # Filter out partial purls without versions
    if purl.to_dict()["version"]:
        try:
            print(purl)
            response = client.get(f"/packages/{encoded_purl}/vulnerabilities").json()
            for vuln in response["data"]["attributes"]["vulnerabilities"]:
                # I'm just printing the ID here, but there is a lot of rich data available about the vulnerability
                print(f"    {vuln['id']}")
        except:
            print(f"Error with {purl}")

