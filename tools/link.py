#!/usr/bin/env python3

from os import symlink
from os.path import join

from variables import Variables

# the link tree is just a collection of symlinks and their targets
_link_tree = {"api/rust": "pleiades/crates/nova-api"}
_vars = Variables()

def link():
    """
    Links files in the _link_tree dictionary to their corresponding destinations.

    For each source-destination pair in _link_tree, this function creates a symbolic link
    from the source file to the destination file. If the destination file already exists,
    it is skipped.

    Args:
        None

    Returns:
        None
    """
    for src, dest in _link_tree.items():
        print(f"linking {src} to {dest}")

        # add abspaths to it
        src = join(_vars.env_root, src)
        dest = join(_vars.env_root, dest)

        try:
            symlink(src, dest)
        except FileExistsError:
            print(f"{dest} already exists, skipping")


def main():
    """
    This function calls the link function to create symbolic links.
    """
    link()


if __name__ == "__main__":
    main()
