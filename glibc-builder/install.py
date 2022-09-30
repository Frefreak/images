#!/usr/bin/env python3
import os
import sys
import time
import argparse
import re
from shlex import quote
from shutil import rmtree

parser = argparse.ArgumentParser()

glibc_src = "https://ftp.gnu.org/gnu/glibc/"

parser.add_argument(
    "-l", "--list", action="store_true", help="list available glibc versions"
)
parser.add_argument("-i", "--install", help="install glibc with specified version")
parser.add_argument("-j", "--job", help="make -j", default=None)
parser.add_argument(
    "-c", "--cc", help="compile with customed gcc command", default="gcc"
)
parser.add_argument(
    "-s", "--src", help="src directory to store source code", default="./"
)
parser.add_argument("-p", "--prefix", help="install prefix", default=None)
parser.add_argument(
    "-nd",
    "--no-download",
    dest="download",
    help="use existing src folder, will use src as 'glibc' src folder if used",
    action="store_false",
)
parser.add_argument(
    "-nc",
    "--no-check",
    dest="check",
    help="whether to check sig for downloaded file",
    action="store_false",
)
parser.add_argument(
    "-nt",
    "--no-tcache",
    dest="tcache",
    help="whether enables tcache",
    action="store_false",
)
parser.set_defaults(check=True, tcache=True, download=True)

MIN_VER = (2, 10)


def get_available_versions():
    import requests
    from bs4 import BeautifulSoup
    r = requests.get(glibc_src)
    html = BeautifulSoup(r.text, "lxml")
    versions = []
    for l in html.select("table > tr > td:nth-of-type(2)"):
        m = re.match(r"^glibc-(2.+)\.tar\.gz$", l.text)
        if m:
            v = m.group(1)
            try:
                if tuple(map(int, v.split("."))) >= MIN_VER:
                    versions.append(v)
            except ValueError:
                pass
    return versions


def install(args, version):
    print(args)
    if args.prefix is None:
        print("need to specify prefix")
        sys.exit(1)
    prefix = os.path.abspath(args.prefix)
    os.chdir(args.src)
    if args.download:
        import requests
        targz = f"glibc-{version}.tar.gz"
        targz_sig = f"glibc-{version}.tar.gz.sig"
        print(f"downloading {targz}...")
        r = requests.get(glibc_src + targz)
        with open(targz, "wb") as f:
            f.write(r.content)
        print(f"downloading {targz_sig}...")
        r = requests.get(glibc_src + targz_sig)
        with open(targz_sig, "wb") as f:
            f.write(r.content)

        if args.check:
            os.system(f"gpg --verify {targz_sig} {targz}")
            input("press enter to continue ")

        print("\x1b[31;1mextracting...\x1b[0m")
        time.sleep(1)
        os.system(f"tar xzvf {targz}")

    print("\x1b[31;1mconfiguring...\x1b[0m")
    time.sleep(1)
    if args.download:
        os.chdir(f"glibc-{version}")
    build_dir = f"build-{version}"
    if not args.tcache:
        build_dir += "_no-tcache"
    try:
        os.stat(build_dir)
        print(f"remove {os.path.abspath(os.curdir)}/{build_dir}? (note: possible a mapping path)")
        choice = input("[y/n]")
        if choice.lower() == 'y':
            rmtree(build_dir)
            os.mkdir(build_dir)
    except FileNotFoundError:
        os.mkdir(build_dir)
    os.chdir(build_dir)
    cflags = os.getenv("CFLAGS", "")
    # remove CFLAGS from env so it won't be used by make/gcc automatically?
    try:
        os.environ.pop('CFLAGS')
    except KeyError:
        pass
    if cflags:
        cflags = f'CFLAGS={quote(cflags)}'
    if args.tcache:
        print("\x1b[31;1mTCACHE enabled (if supported)\x1b[0m")
        print("full commandline:")
        print(f"CC={args.cc} {cflags} ../configure --prefix={prefix}")
        time.sleep(1)
        os.system(f"CC={args.cc} {cflags} ../configure --prefix={prefix}")
    else:
        print("\x1b[31;1mTCACHE disabled\x1b[0m")
        print("full commandline:")
        print(f"CC={args.cc} {cflags} ../configure --prefix={prefix}")
        time.sleep(1)
        os.system(f"CC={args.cc} {cflags} ../configure --prefix={prefix} --disable-experimental-malloc")

    print("\x1b[31;1mbuilding & installing...\x1b[0m")
    if args.job:
        print(f'making with -j{args.job}')
        time.sleep(1)
        os.system(f"bear make -j{args.job}")
    else:
        print(f'making with -j (whatever core you have)')
        time.sleep(1)
        os.system(f"bear make -j$(nproc)")
    os.system(f"make install")


def main():
    args = parser.parse_args()
    if args.list:
        versions = get_available_versions()
        print("\n".join(versions))
    elif args.install:
        install(args, args.install)


if __name__ == "__main__":
    main()
