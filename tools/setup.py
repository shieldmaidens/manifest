#!/usr/bin/env python3


from subprocess import run
from os import mkdir
from os.path import join, abspath
from shutil import copy

from link import link
from variables import Variables, pushd

_vars = Variables()


def create_tmp():
    '''
    creates a tmp directory for pleiades to use
    '''
    print("creating tmp directory")
    try:
        mkdir(_vars.pleiades_tmp)
    except FileExistsError:
        pass


def setup_env():
    """
    Copies the environment file from the manifest directory to the root directory and runs `direnv allow`.
    :return: None
    """
    src = abspath(join(_vars.env_root, "manifest", "envrc"))
    dest = abspath(join(_vars.env_root, ".envrc"))
    copy(src, dest)
    with pushd(_vars.env_root):
        print("running direnv allow")
        run(["direnv", "allow"])


def main():
    """
    This function sets up the environment, links the necessary files, and creates a temporary directory.
    """
    setup_env()
    link()
    create_tmp()


if __name__ == "__main__":
    main()
