import attr
import uuid
import datetime

def timestamp_now():
    """
    Returns: a timestamp for this instant, in ISO 8601 format
    """
    return datetime.datetime.isoformat(datetime.datetime.now())

# Data type definitions of posts and comments
@attr.s
class Post:
    content = attr.ib()
    comments = attr.ib(default=[])
    date = attr.ib(factory=timestamp_now)
    name = attr.ib(factory=lambda: uuid.uuid4().hex)

@attr.s
class Comment:
    commenter = attr.ib()
    content = attr.ib()
    date = attr.ib(factory=timestamp_now)
    name = attr.ib(factory=lambda: uuid.uuid4().hex)

@attr.s
class Page:
    name = attr.ib()
    date = attr.ib(factory=timestamp_now)
