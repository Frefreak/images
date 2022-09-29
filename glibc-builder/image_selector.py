#!/usr/bin/env python3

import os
import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("version")


def main():
    args = parser.parse_args()
    segs = args.version.split(".", 1)
    # let it crash
    major = int(segs[0])
    assert(major == 2)
    minor = int(segs[1])
    # just do a simple check (possibly meaningless)
    assert minor > 0

    build_image = os.getenv("BUILD_IMAGE")
    if build_image is not None:
        print(build_image)
    elif minor >= 30:
        print("c4r50nz/glibc-builder:ubuntu20.04")
    elif minor >= 26:
        print("c4r50nz/glibc-builder:ubuntu18.04")
    elif minor >= 23:
        print("c4r50nz/glibc-builder:ubuntu16.04")
    else:
        print(
            "\x1b[31;1mI'm not sure which image should I use, try setting with BUILD_IMAGE\x1b[31;0m",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
