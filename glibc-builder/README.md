This image contains the tools to build & use glibc.

It is useful when you are on a distro with bleeding edge system toolchains,
which might have some troubles compiling old-ish glibc versions.

Currently the builder is from ubuntu-20.04 and can compile glibc around 2.30.

# how to use

## build

### use existing glibc source

**note**: change command line accordingly, use common sense

1. clone glibc src and checkout to target tag
2. build glibc with this builder image and install.py script:
```sh
podman run -v <glibc_src>:/glibc <prefix>:/prefix \
    c4r50nz/glibc-builder:ubuntu20.04 -- \
    ./install.py -i <version> -s /glibc -p /prefix -nc -nd
```
- **glibc\_src**: root path of glibc source
- **prefix**: where to install the built glibc

A script named `./build_with_existing_src.sh` is provided to make this easier.

### let it download the source to build

1. build glibc with this builder image and install.py script (do not pass `-nd`):
```sh
podman run -v <glibc_src>:/glibc <prefix>:/prefix \
    c4r50nz/glibc-builder:ubuntu20.04 -- \
    ./install.py -i <version> -s /glibc -p /prefix -nc
```
**glibc\_src**: root path of glibc source
**prefix**: where to install the built glibc

A script named `./download_and_build.sh` is provided to make this easier.

### misc

1. `install.py` will `make` with `-j$(nproc)`, change if not desired (with `-j`).
2. If you use the script, better read through what `install.py` does, its very simple and has some
command line options to tweak how to build.
