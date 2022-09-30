#!/usr/bin/env bash

if [ $# -le 2 ]; then
	echo "Usage: $0 <version> <glibc_src> <prefix> ..."
	exit 1
fi

version="$1"
shift
glibc_src="$1"
shift
prefix="$1"
shift

IMAGE=$(python3 image_selector.py $version)
if [ -z $IMAGE ]; then
	echo image selection failed, see message?
	exit 1
fi

echo using image ${IMAGE}
mkdir -p "$prefix"
# map glibc_src, prefix to the same path to make `compile_commands.json` as correct as possible
podman run -it -v "$glibc_src":"$glibc_src" -v "$prefix":"$prefix"  -v ./install.py:/install.py \
    -e CFLAGS="$CFLAGS" ${IMAGE} \
    /install.py -i "$version" -s "$glibc_src" -p "$prefix" -nc -nd $@
