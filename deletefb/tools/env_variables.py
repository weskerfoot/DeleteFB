#!/usr/bin/env python3

import sys
import os
import re
import typing as ty

from types import SimpleNamespace


class EnvVar:
    def __init__(self,
                 env_key: str,
                 dest: ty.Optional[str] = None,
                 type: ty.Type = str,
                 default: ty.Optional[str] = None,
                 help: ty.Optional[str] = None):

        assert re.match('^[a-zA-Z_]+[a-zA-Z0-9_]*$', env_key), "Bad env key {0}".format(env_key)
        self.key = env_key
        self.dest = dest or env_key.lower()
        self.type = type
        self.help = help
        self.default = default


class EnvParser:
    def __init__(self):
        self.env_vars = set()

    def add_argument(self, *args, **kwargs):
        self.env_vars.add(EnvVar(*args, **kwargs))

    def print_help(self):
        print("environment variables:")
        for v in self.env_vars:
            print("  {0}=<{1}>\t{2}".format(v.key, v.type.__name__, v.help or ''))

    def parse_args(self):
        args = {}
        for v in self.env_vars:
            try:
                args[v.dest] = v.type(os.environ.get(v.key, v.default))
            except ValueError:
                print("{0}: error: environment variable {1} should be of type {2}".format(
                      sys.argv[0].split('/')[-1],
                      v.key,
                      v.type.__name__))
                sys.exit(1)
        return SimpleNamespace(**args)
