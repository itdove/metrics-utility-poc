# Metric-cpu-poc

## Build/Push image

1. make build
2. Retag the image toward your own image repo
3. podman push <image>

## Edit install/cronjob.yaml

Change the image in the [cronjob.yaml](install/cronjob.yaml) to point to your own image

### Deploy

1. Set you kubeconfig file to point to your Customer SaaS instance
2. `oc apply -k install`
