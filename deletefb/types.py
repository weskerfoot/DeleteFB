import attr
import uuid
import pendulum

def convert_timestamp(text):
    """
    Tries to parse a timestamp into a DateTime instance
    Returns `None` if it cannot be parsed
    """
    try:
        return pendulum.from_format(text, "DD/M/YYYY")
    except ValueError:
        try:
            return (pendulum.from_format(text, "DD MMM")
                    .set(year=pendulum.now().year))
        except ValueError:
            return None

# Data type definitions of posts and comments
@attr.s
class Post:
    content = attr.ib()
    comments = attr.ib(default=[])
    date = attr.ib(factory=pendulum.now)
    name = attr.ib(factory=lambda: uuid.uuid4().hex)

@attr.s
class Comment:
    commenter = attr.ib()
    content = attr.ib()
    date = attr.ib(factory=pendulum.now)
    name = attr.ib(factory=lambda: uuid.uuid4().hex)

@attr.s
class Conversation:
    url = attr.ib()
    name = attr.ib()
    timestamp = attr.ib(converter=convert_timestamp)
    messages = attr.ib(default=[])

@attr.s
class Message:
    name = attr.ib()
    content = attr.ib()

    # Remove the last 3 digits from FB's timestamps. They are not standard.
    timestamp = attr.ib(converter=lambda t: pendulum.from_timestamp(int(str(t)[0:-3])))

@attr.s
class Page:
    name = attr.ib()
    date = attr.ib(factory=pendulum.now)
