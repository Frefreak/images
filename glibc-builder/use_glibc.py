#!/usr/bin/env python3

import argparse
import os
import sys
import lief
import glob


parser = argparse.ArgumentParser()

parser.add_argument('bin')
parser.add_argument('libc_folder')
parser.add_argument('out')
parser.add_argument('-r', '--runpath', default=None)

def main():
    args = parser.parse_args()
    binary = lief.parse(args.bin)

    libc_name = None
    for i in binary.libraries:
        if "libc.so.6" in i:
            libc_name = i
            break

    if libc_name is None:
        print("No libc linked. Exiting.")

    print("Current ld.so:")
    print(f"Path: {binary.interpreter}")
    print()

    libc_folder = args.libc_folder
    # libc_path = str(libc_folder / 'libc.so.6')

    loaders = glob.glob(f'{libc_folder}/ld-2.*.so')
    ld = None
    if len(loaders):
        ld = os.path.abspath(loaders[0])
    if ld is None:
        print(f"Can't find interpreter in {libc_folder}")
        sys.exit(1)
    binary.interpreter = ld
    print("New ld.so:")
    print(f"Path: {binary.interpreter}")
    print()

    runpath = os.path.abspath(args.runpath or libc_folder)
    binary += lief.ELF.DynamicEntryRunPath(runpath)
    print("Adding RUNPATH:")
    print(f"Path: {runpath}")
    print()

    print("Writing new binary {}".format(args.out))
    binary.write(args.out)


if __name__ == "__main__":
    main()
