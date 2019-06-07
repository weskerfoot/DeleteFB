import attr
import datetime
import uuid
import json

from contextlib import contextmanager
from pathlib import Path


# Used to avoid duplicates in the log
from pybloom_live import BloomFilter

def acquire_path():

    log_file = open(log_path, mode="ta", buffering=1)

    bfilter = BloomFilter(
            capacity=settings["MAX_POSTS"],
            error_rate=0.001
    )

    return

@attr.s
class Post:
    content = attr.ib()
    comments = attr.ib(default=[])
    date = attr.ib(factory=datetime.datetime.now)
    name = attr.ib(factory=uuid.uuid4)

@attr.s
class Comment:
    commenter = attr.ib()
    content = attr.ib()
    date = attr.ib(factory=datetime.datetime.now)
    name = attr.ib(factory=uuid.uuid4)

@attr.s
class Archive:
    archive_type = attr.ib()

    # We give the Archive class a file handle
    # This is better because the archive function
    # should not know about anything related to filesystem paths
    archive_file = attr.ib()

    def archive(self, content):
        # do something
        print("Archiving type {0} with content {1} to directory {2}".format(self.archive_type, content, self.archive_dir))
        self.archive_file.write(json.dumps(content.asdict()))

wall_archive = Archive(archive_type="wall")

comments = [Comment(commenter="Bob", content="Nice post!"),
            Comment(commenter="Alice", content="I hate this")]

wall_archive.archive(Post(content="A post!", comments=comments))
