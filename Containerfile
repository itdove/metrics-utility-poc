FROM --platform=linux/amd64 registry.redhat.io/ansible-automation-platform-25/controller-rhel8@sha256:919777713928a849dd1ea550a834ddbe5c363c1d203e7e8bf184ca1f36b3c03c

WORKDIR /metrics-utility-poc

COPY . .

ENTRYPOINT [ "./run.sh" ]
