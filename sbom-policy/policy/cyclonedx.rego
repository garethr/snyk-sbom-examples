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

deny[msg] {
    count(input.components) > max_components
    msg := sprintf("%s has %d components, more than the maximum allowed number of %d", [name, count(input.components), max_components])
}
