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
data = json.loads(sys.stdin.read())

# The following has next to no real error handling, it's intended to demonstrate the
# very basic operation of the API
for purl in [component["purl"] for component in data["components"]]:
    # Encode the purl, including encoding forward slashes
    encoded_purl = urllib.parse.quote(purl, safe="")
    purl_o = PackageURL.from_string(purl)
    # Filter out partial purls without versions
    if purl_o.to_dict()["version"]:
        try:
            print(purl)
            response = client.get(f"/packages/{encoded_purl}/vulnerabilities").json()
            for vuln in response["data"]["attributes"]["vulnerabilities"]:
                print(f"    {vuln['id']}")
        except:
            print(f"Error with {purl}")

