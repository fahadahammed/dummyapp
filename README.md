# DummyApp

This repo consists of code for a dummy fast api application to demonstrate CI/CD, healthchecks, scalability, docker build, publish package, testing etc.

## Helm Install

```
$ helm upgrade --install --debug dummyapp ./ --values values.development.yaml -n dummyapp-development --create-namespace --atomic
```

To install certificate using helm, needed to ommit certificate kind as it is handled via annotation in ingress.