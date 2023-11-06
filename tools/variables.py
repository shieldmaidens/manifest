#!/usr/bin/env python3

from contextlib import contextmanager
from json import dumps
from os import chdir, getcwd
from os.path import abspath, join


class Variables:
    """
    A class that defines various variables used in the project.

    Attributes:
        env_root (str): The absolute path of the project's root directory.
        pleiades_tmp (str): The path of the temporary directory used by Pleiades.
    """

    env_root = abspath(join(__file__, "..", "..", ".."))
    pleiades_tmp = "/tmp/pleiades"

    def __init__(self) -> None:
        pass

    def __iter__(self):
        attrs = [a for a in dir(self) if not a.startswith("__")]
        for attr in attrs:
            yield {attr: getattr(self, attr)}

    def __str__(self) -> str:
        variables = list(self.__iter__())
        return dumps(variables)


@contextmanager
def pushd(path: str):
    """
    Change the current working directory to the given path, and pushes 
    the previous working directory onto a stack. This allows the 
    caller to easily return to the previous working directory later.

    :param path: The path to change the current working directory to.
    :yield: None
    """
    prev = getcwd()
    chdir(path)
    try:
        yield
    finally:
        chdir(prev)


if __name__ == "__main__":
    print(Variables())
