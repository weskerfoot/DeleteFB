from .config import settings
from contextlib import contextmanager
from pathlib import Path
from datetime import datetime
from time import time

import attr
import cattr
import json
import typing

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Used to avoid duplicates in the log
from pybloom_live import BloomFilter

cattr.register_unstructure_hook(
    datetime, lambda dt: datetime.strftime(dt, format=TIME_FORMAT)
)

def make_filter():
    return BloomFilter(
        capacity=settings["MAX_POSTS"],
        error_rate=0.001
    )

@attr.s
class Archive:
    archive_type = attr.ib()

    # We give the Archive class a file handle
    archive_file = attr.ib()

    _bloom_filter = attr.ib(factory=make_filter)

    def archive(self, content):
        """
        Archive an object
        """

        if hasattr(content, 'name'):
            print("Archiving {0}".format(content.name))

        if content.name not in self._bloom_filter:
            self.archive_file.write(json.dumps(cattr.unstructure(content),
                                               indent=4,
                                               sort_keys=True) + "\n")

            self._bloom_filter.add(content.name)
        return

@contextmanager
def archiver(archive_type):

    archive_file = open(
        str((Path(".") / Path(archive_type).name).with_suffix(".log.{0}".format(time()))),
        mode="ta",
        buffering=1
    )

    archiver_instance = Archive(
        archive_type=archive_type,
        archive_file=archive_file
    )

    try:
        yield archiver_instance
    finally:
        archive_file.close()
