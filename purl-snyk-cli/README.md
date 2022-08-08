# Demonstrating using the purl API with the Snyk CLI

In most cases you should just use `snyk test` or `snyk monitor`, but as an example of the low level purl API, here's an example of taking the current JSON output, and then returning a list of vulnerabilities by package.

See the comments in the [cli-to-vuln.py](cli-to-vuln.py) for an explanation. This is intended as an example.

```
$ snyk test --json --print-deps | python cli-to-vuln.py
...
pkg:maven/org.springframework/spring-beans@5.2.3.RELEASE
    SNYK-JAVA-ORGSPRINGFRAMEWORK-2823313
    SNYK-JAVA-ORGSPRINGFRAMEWORK-2436751
pkg:maven/org.springframework/spring-webmvc@5.2.3.RELEASE
pkg:maven/org.springframework/spring-aop@5.2.3.RELEASE
pkg:maven/org.springframework/spring-expression@5.2.3.RELEASE
    SNYK-JAVA-ORGSPRINGFRAMEWORK-2434828
pkg:maven/net.lingala.zip4j/zip4j@1.3.1
    SNYK-JAVA-NETLINGALAZIP4J-1074967
    SNYK-JAVA-NETLINGALAZIP4J-1011359
    SNYK-JAVA-NETLINGALAZIP4J-31679
```
