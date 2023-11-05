#!/usr/bin/env python3

from contextlib import contextmanager
from subprocess import run
from os import chdir, getcwd
from os.path import join, abspath
from shutil import copy

from link import link

env_root = abspath(join(__file__, "..", "..", ".."))

@contextmanager
def pushd(path):
    prev = getcwd()
    chdir(path)
    try:
        yield
    finally:
        chdir(prev)


def setup_env():
    src = abspath(join(env_root, "manifest", ".envrc"))
    dest = abspath(join(env_root, ".envrc"))
    copy(src, dest)
    with pushd(env_root):
        print("running direnv allow")
        run(["direnv", "allow"])


def main():
    setup_env()
    link()


if __name__ == "__main__":
    main()
