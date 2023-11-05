#!/usr/bin/env python3

from os import symlink
from os.path import abspath, join

# the link tree is just a collection of symlinks and their targets
_link_tree = {"api/rust": "pleiades/crates/nova-api"}


def link():
    for src, dest in _link_tree.items():
        print(f"linking {src} to {dest}")
        root = abspath(join(__file__, "..", "..", ".."))

        # add abspaths to it
        src = join(root, src)
        dest = join(root, dest)

        try:
            symlink(src, dest)
        except FileExistsError:
            print(f"{dest} already exists, skipping")


def main():
    link()


if __name__ == "__main__":
    main()
