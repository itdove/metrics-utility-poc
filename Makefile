.PHONY: build
build:
	podman build -f Containerfile -t quay.io/itdove/metrics-utility-poc

.PHONY: push
push: 
	podman push quay.io/itdove/metrics-utility-poc:latest   

.PHONY: run
run:
	podman run -it quay.io/itdove/metrics-utility-poc:latest

.PHONY: run-bash
run-bash:
	podman run -it --entrypoint "" quay.io/itdove/metrics-utility-poc:latest bash
