#!/usr/bin/env python3

from toml import load as tload

data = None
with open("server/pleiades/Config.toml") as fh:
    data = tload(fh)

print(data["deps"])
