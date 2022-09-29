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
client = snyk.SnykClient(token, version="2022-09-15~experimental", url="https://api.snyk.io/rest")

# We need an org id, but any org ID will do
response = client.get("/orgs").json()
org_id = response["data"][0]["id"]

print(org_id)

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
            response = client.get(f"/orgs/{org_id}/packages/{encoded_purl}/issues").json()
            for vuln in response["data"]:
                print(f"    {vuln['id']}")
        except:
            print(f"Error with {purl}")

