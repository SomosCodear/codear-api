from .base import EventSource
from .frontendcafe import *
from .meetup import *

__all__ = [
    'EventSource',
    'all_sources',
]

all_sources = {
    source.get_source_id(): source
    for source in EventSource.__subclasses__()
}
