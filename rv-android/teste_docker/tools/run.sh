#!/bin/env bash

docker run -it --rm --device /dev/kvm -e PARTITION=24576 -e MEMORY=6144 -e CORES=2 --name rvsec-tool phtcosta/rvandroid_tools:0.0.1


#docker run -d --device /dev/kvm -p 5555:5555 -v androiddata:/data -e PARTITION=24576 -e MEMORY=6144 -e CORES=2 --name docker-android-emulator cndaqiang/docker-android-emulator:api-33
