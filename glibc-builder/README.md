This image contains the tools to build & use glibc.

It is useful when you are on a distro with bleeding edge system toolchains,
which might have some troubles compiling old-ish glibc versions.

Currently this tool should be able to build glibc around version 2.23 - 2.31
(some of the versions in this range are tested, version outside of this range
are untested).

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

### notes

1. `install.py` will `make` with `-j$(nproc)`, change if not desired (with `-j`).
2. If you use the script, you'd better read through what `install.py` does, its very simple and has some
command line options to tweak how to build.
3. `image_selector.py` might not be correct, I only tested a few versions.
4. A `compile_commands.json` will be left in the build folder, you can symlink
it to navigate the code easier.
5. The helper scripts will map `glibc_src` and `prefix` to the same path as host
to make the generated `compile_commands.json` works better. This should be OK
most of the time as long as you do not provide some path already existed in
the container.
6. I'm sure there are many bugs.

## change existing binary's glibc version

Say I have a binary: **babyheap**

```sh
❯ ldd babyheap
        linux-vdso.so.1 (0x00007ffebc1c6000)
        libc.so.6 => /usr/lib/libc.so.6 (0x00007f725da19000)
        /lib64/ld-linux-x86-64.so.2 => /usr/lib64/ld-linux-x86-64.so.2 (0x00007f725df14000)
```

So it is using system glibc. I now want to change it to use glibc-2.23 (assuming
you know the target's glibc version) to make debugging locally easier. One way
is to use `LD_PRELOAD` but I find it doesn't work for some binaries. What seems
to work better is to directly modify the binary. This can be summarized in
`use_glibc.py`.

```sh
❯ ./use_glibc.py babyheap ~/prefix/glibc_2.23/lib babyheap-2.23
Current ld.so:
Path: /lib64/ld-linux-x86-64.so.2

New ld.so:
Path: /home/.../prefix/glibc_2.23/lib/ld-2.23.so

Adding RUNPATH:
Path: /home/.../prefix/glibc_2.23/lib

Writing new binary babyheap-2.23

❯ chmod a+x babyheap-2.23

❯ ldd babyheap-2.23
        linux-vdso.so.1 (0x00007ffdf069b000)
        libc.so.6 => /home/.../prefix/glibc_2.23/lib/libc.so.6 (0x00007fba05a00000)
        /home/.../prefix/glibc_2.23/lib/ld-2.23.so => /usr/lib64/ld-linux-x86-64.so.2 (0x00007fba06386000)
```

and it runs ok:

```sh
❯ ./babyheap-2.23
1. add
2. edit
3. delete
4. show
5. exit
Choice:
```
