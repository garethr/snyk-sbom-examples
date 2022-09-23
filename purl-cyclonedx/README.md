# Testing a CycloneDX document for vulnerabilities

Although the Snyk API doesn't have a high level API for testing a CycloneDX (or other SBOM) document yet, the low level purl endpoint can be used. Simply iterate over the components and return the individual lists of vulnerabilities.

For this we can use a sample repo, in this case a Spring Boot application.

```
git clone https://github.com/garethr/snykier
cd snykier
```

We'll also use [syft](https://github.com/anchore/syft) to generate the SBOM, although you can use any suitable tool to list the components.

The example script is written in python, and uses two extra dependencies.

```
pip install pysnyk packageurl-python
```

You don't need to use Python to use the API, but the [cyclone-to-vuln.py](cyclone-to-vuln.py) script provides a very basic implementation you could use as the basis for something more useful.

```
$ syft . -o cyclonedxjson | python cyclone-to-vuln.py
 ✔ Indexed ../../snykier
 ✔ Cataloged packages      [5 packages]

pkg:maven/io.takari/maven-wrapper@0.5.6
pkg:maven/net.lingala.zip4j/zip4j@1.3.1
    SNYK-JAVA-NETLINGALAZIP4J-1074967
    SNYK-JAVA-NETLINGALAZIP4J-1011359
    SNYK-JAVA-NETLINGALAZIP4J-31679
```

Note that the purl endpoint at present only supports npm and maven packages, although other ecosystems will be added soon.
