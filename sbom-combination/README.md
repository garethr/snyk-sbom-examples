# Combining SBOMs

The Snyk APIs currently provide SBOMs at the project level. But let's say you have a repository containing two separate projects, a Javascript frontend and a Java backend. And you'd like to provide an SBOM with details from both. You can do that with the [CycloneDX CLI](https://github.com/CycloneDX/cyclonedx-cli).


## Download the individual component SBOMs

First download the individual SBOMs you want to combine. I'm just down that manually below, but you could do this programatically based on tags or other project metadata. 

```
$ http https://api.snyk.io/rest/orgs/<orgId>/projects/<projectId>/sbom Authorization:"token $SNYK_TOKEN" version==2022-03-31~experimental format=="cyclonedx+json" > npm.json
$ http https://api.snyk.io/rest/orgs/<orgId>/projects/<projectId>/sbom Authorization:"token $SNYK_TOKEN" version==2022-03-31~experimental format=="cyclonedx+json" > maven.json
```


## Merge into a single SBOM

Most likely a hierarchical SBOM is what you're after, where the SBOMs are still separate, but combined at a higher level.

```
$ cyclonedx merge --input-files npm.json maven.json --output-format json --hierarchical --name my-app --version 0.1.0
```

This outputs to stdout a new SBOM, which, along with the individual SBOMs will have a node like the following:

```
{
  "ref": "my-app@0.1.0",
  "dependsOn": [
    "todo-list@0.1.0:todo-list@0.1.0",
    "io.pivotal.sporing:todo-list@0.0.1-SNAPSHOT:io.pivotal.sporing:todo-list@0.0.1-SNAPSHOT"
  ]
}
```
