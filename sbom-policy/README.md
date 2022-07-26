# Apply policy to your SBOMs

One use case for a consistent bill of materials format is to check it against a set of organisational policies. For this example we'll write a set of policies using [Open Policy Agent](https://www.openpolicyagent.org/) and apply them using [Conftest](https://www.conftest.dev/).

The policy below demonstrates two thing you might be interested in enforcing:

1. A soft limit to the number of components within a given project
2. A disallowed list of specific software components

These are purely examples, the Rego language used by Open Policy Agent can be used to define any policy you like. 

```rego
package main


max_components = 30

name = input.metadata.component.name

disallow_list = [
    "com.fasterxml.jackson.core:jackson-core",
    "net.bytebuddy:byte-buddy",
]

deny[msg] {
    component := input.components[_]
    component.name = disallow
    contains(component[_], disallow_list[_])
    msg := sprintf("%s is using %s %s which is not permitted", [name, component.name, component.version])
}

warn[msg] {
    count(input.components) > max_components
    msg := sprintf("%s has %d components, more than the maximum allowed number of %d", [name, count(input.components), max_components])
}
```


As a quick example of applying the policy against a specific Snyk project we're just piping the CycloneDX document into `conftest`.

```
$ http https://api.snyk.io/rest/orgs/<orgId>/projects/<projectId>/sbom Authorization:"token $SNYK_TOKEN" version==2022-03-31~experimental format=="cyclonedx+json" | conftest test -
WARN - - main - io.pivotal.sporing:todo-list has 104 components, more than the maximum allowed number of 30
FAIL - - main - io.pivotal.sporing:todo-list is using net.bytebuddy:byte-buddy 1.10.19 which is not permitted
FAIL - - main - io.pivotal.sporing:todo-list is using com.fasterxml.jackson.core:jackson-core 2.11.4 which is not permitted

3 tests, 0 passed, 1 warning, 2 failures, 0 exceptions
```

This provides a quick way of running a policy against a single project. You could automate this further by using the API to iterate over projects before retrieving the SBOMs, use Open Policy Agent directly rather than via the `conftest` CLI tool, send policy violations into Slack and more.
