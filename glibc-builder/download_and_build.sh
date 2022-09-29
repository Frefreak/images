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

mkdir -p "$prefix"
podman run -it -v "$glibc_src":/glibc -v "$prefix":/prefix  -v ./install.py:/install.py \
    c4r50nz/glibc-builder:ubuntu20.04 \
    /install.py -i "$version" -s /glibc -p /prefix -nc $@
