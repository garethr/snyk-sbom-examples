# Storing Snyk SBOM data in a local database

For the purposes of this demo I'll be using SQlite. As with any database decision, this has pros and cons. SQLite doesn't have great support for arbitrary JSON data. But it has a unsuppased local experience. Choose whichever database technology you prefer.

I'm going to be using the excellent [sqlite-utils](https://sqlite-utils.datasette.io/en/stable/) package to create the database and run queries. I'm also using the [httpie](https://httpie.io/) HTTP client to access the Snyk API. Neither of these tool are required, both just provide a lovely developer experience.

## Querying for packages 

This is a bit of a contrived example, but here we download the SBOM data from Snyk, and then run a query against an in-memory database created from that data.

```
$ http https://api.snyk.io/rest/orgs/<orgId>/projects/<projectId>/sbom Authorization:"token $SNYK_TOKEN" version==2022-03-31~experimental format=="cyclonedx+json" | sqlite-utils memory - "select json_extract(json_each.value, '\$.purl') as purl from stdin, json_each(stdin.components) where instr(json_each.value, 'logback')"
[{"purl": "pkg:maven/ch.qos.logback/logback-core@1.2.3"},
 {"purl": "pkg:maven/ch.qos.logback/logback-classic@1.2.3"}]
```

Let's break down the query:

```sql
-- use the jsonpath expression to grab the purl field from the individual component
SELECT json_extract(json_each.value, '\$.purl') as purl
-- stdin because we are using the in-memory database. json_each we can can access components individually
FROM stdin, json_each(stdin.components)
-- only return regords which container a specific string. More powerful queries would be possible too but this is faster.
WHERE instr(json_each.value, 'logback')
```

## A persistant database

The above is quite handy for querying an individual project, but what about multiple projects? For that we want to get the data into a local database. For that we can pipe the data to `sqlite-utils` like so:

```
$ http https://api.snyk.io/rest/orgs/<orgId>/projects/<projectId>/sbom Authorization:"token $SNYK_TOKEN" version==2022-03-31~experimental format=="cyclonedx+json" | sqlite-utils insert sbom.db sboms --pk metdata.component.bom-ref -
```

Running this against a few Snyk projects will populate the database. Let's get a list of projects imported, in my case both a Maven project and an npm project.

```
sqlite-utils sbom.db "select json_extract(metadata, '\$.component.purl') as purl from sboms"
[{"purl": "pkg:maven/io.pivotal.sporing/todo-list@0.0.1-SNAPSHOT"},
 {"purl": "pkg:npm/todo-list@0.1.0"}]
```

And then let's run our search for a packages across all of the components of both.

```
$ sqlite-utils sbom.db "select json_extract(metadata, '\$.component.name') as project, json_extract(json_each.value, '\$.purl') as purl from sboms, json_each(sboms.components) where instr(json_each.value, 'json')"
[{"project": "io.pivotal.sporing:todo-list", "purl": "pkg:maven/org.springframework.boot/spring-boot-starter-json@2.4.2"},
 {"project": "io.pivotal.sporing:todo-list", "purl": "pkg:maven/org.springframework.boot/spring-boot-starter-json@2.4.2"},
 {"project": "todo-list", "purl": "pkg:npm/json5@0.5.1"}]
```

This is obviously intended as a low level example. You could build a higher level DSL for common queries, you might want to consider making this a timeseries, and you'd definitely want to consider how best to keep the database up to date. But the above should demonstrate how easy it is to get started.
