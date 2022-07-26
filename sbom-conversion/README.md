# Convert to different SBOM formats

The current API supports CycloneDX 1.4 in JSON. Over time we'll add support for different formats and serialisations, but in the meantime it's easy enough to convert to different versions, serilisations and formats using the [CycloneDX CLI](https://github.com/CycloneDX/cyclonedx-cli).

The following examples use the [httpie](https://httpie.io/) client, just for demonstration purpurpose. This will work with any http client.

## Convert to a different CycloneDX version

```bash
$ http https://api.snyk.io/rest/orgs/<orgId>/projects/<projectId>/sbom Authorization:"token $SNYK_TOKEN" version==2022-03-31~experimental format=="cyclonedx+json" | cyclonedx convert --input-format json --output-format json --output-version v1_2
```

## Convert to the CycloneDX XML 

```bash
$ http https://api.snyk.io/rest/orgs/<orgId>/projects/<projectId>/sbom Authorization:"token $SNYK_TOKEN" version==2022-03-31~experimental format=="cyclonedx+json" | cyclonedx convert --input-format json --output-format xml
```

## Convert to SPDX

```bash
$ http https://api.snyk.io/rest/orgs/<orgId>/projects/<projectId>/sbom Authorization:"token $SNYK_TOKEN" version==2022-03-31~experimental format=="cyclonedx+json" | cyclonedx convert --input-format json --output-format spdxjson
```
