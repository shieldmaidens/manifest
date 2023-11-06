#!/usr/bin/env python3

from argparse import ArgumentParser
from os.path import join
from subprocess import run
from shlex import split
from variables import Variables, pushd


# pylint: disable=maybe-no-member
class Build:
    """
    A class that provides methods to build, clean, generate, and lint projects.

    Attributes:
        supported_projects (list): A list of supported project names.
        _project_map (dict): A dictionary that maps project names to 
            their respective build, clean, generate, and lint commands.
        _vars (Variables): An instance of the Variables class.
    """

    supported_projects = ["api", "pleiades"]
    _project_map = {
        "api": {
            "path": "api",
            "deps": None,
            "build": "buf build",
            "clean": "",
            "generate": "buf generate",
            "lint": "buf lint",
        },
        "pleiades": {
            "path": "pleiades",
            "deps": ["api"],
            "build": "cargo build",
            "clean": "cargo clean",
            "generate": "",
            "lint": "cargo clippy",
        },
    }

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
        self._vars = Variables()

    def run(self) -> None:
        """
        Runs the build process for the specified project.

        If `full_rebuild` is True, the method first cleans all existing 
        build artifacts before starting the build process.
        """
        if self.full_rebuild:
            self.clean_all()
        self.build(self.project)

    def build(self, project=""):
        """
        Builds the specified project.

        Args:
            project (str): The name of the project to build.
                Valid values are "api", "pleiades", and "all". Defaults to "".

        Raises:
            ValueError: If an invalid project name is specified.
        """
        # pylint: disable=fixme
        # todo (sienna): implement this when macos uses >3.10
        # match project:
        #     case "api":
        #         self._build_api()
        #     case "pleiades":
        #         self._build_api()
        #         self._build_pleiades()
        #     case "all":
        #         self._build_all()
        #     case _:
        #         raise ValueError(f"invalid project: {self.project}")
        if project == "api":
            self._build_api()
        elif project == "pleiades":
            self._build_api()
            self._build_pleiades()
        elif project == "all":
            self._build_all()
        else:
            raise ValueError(f"invalid project: {self.project}")

    def clean_all(self):
        """
        Cleans all supported projects by iterating through the list 
        of supported projects and running the clean command specified 
        in the project map. If no clean command is specified, the 
        method does nothing for that project.
        """
        for project in self.supported_projects:
            project_path = join(self._vars.env_root, self._project_map[project]["path"])
            with pushd(project_path):
                print(f"cleaning {project}")
                if self._project_map[project]["clean"] != "":
                    run(split(self._project_map[project]["clean"]), check=False)

    def _clean_api(self):
        project_path = join(self._vars.env_root, self._project_map["api"]["path"])
        with pushd(project_path):
            print("cleaning api")
            if self._project_map["api"]["clean"] != "":
                run(split(self._project_map["api"]["clean"]), check=False)

    def _build_api(self):
        project_path = join(self._vars.env_root, self._project_map["api"]["path"])
        with pushd(project_path):
            print("building api")
            run(split(self._project_map["api"]["build"]), check=False)

            print("generating api definitions")
            run(split(self._project_map["api"]["generate"]), check=False)

    def _clean_pleiades(self) -> None:
        project_path = join(self._vars.env_root, self._project_map["pleiades"]["path"])
        with pushd(project_path):
            print("cleaning pleiades")
            run(split(self._project_map["pleiades"]["clean"]), check=False)

    def _build_pleiades(self):
        project_path = join(self._vars.env_root, self._project_map["pleiades"]["path"])
        with pushd(project_path):
            if self.full_rebuild:
                print("full rebuild requested for pleiades")
                self._clean_pleiades()
                self._clean_api()
                self._build_api()

            print("building pleiades")
            run(split(self._project_map["pleiades"]["build"]), check=False)

    def _build_all(self):
        print("unsupported right now")


def main():
    """
    Entry point for the build helper tool for the Nova engine.

    Parses command line arguments and runs the build process for the specified project.
    """
    parser = ArgumentParser(description="build helper for nova engine")
    parser.add_argument(
        "-p",
        "--project",
        choices=Build.supported_projects,
        default="pleiades",
        help="the project to build",
        required=True,
    )
    # parser.add_argument(
    #     "-l",
    #     "--lint",
    #     action="store_true",
    #     help="run linters before building",
    #     default=False,
    # )
    # parser.add_argument(
    #     "--lint-only",
    #     action="store_true",
    #     help="run linters but don't build",
    #     default=False,
    # )
    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="clean the project before building it",
        default=False,
    )
    parser.add_argument(
        "--clean-only",
        action="store_true",
        help="clean the project but don't build it",
        default=False,
    )
    parser.add_argument(
        "-f",
        "--full-rebuild",
        action="store_true",
        help="do a full rebuild of the project",
        default=False,
    )
    parser.add_argument(
        "-g",
        "--generate",
        action="store_true",
        help="run any code generation steps before building",
        default=True,
    )
    args = parser.parse_args()

    build = Build(**vars(args))
    build.run()


if __name__ == "__main__":
    main()
