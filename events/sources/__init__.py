from __future__ import annotations
from .base import EventSource
from .frontendcafe import FrontendCafeEventSource
from .meetup import MeetupEventSource

__all__ = [
    'EventSource',
    'FrontendCafeEventSource',
    'MeetupEventSource',
    'all_sources',
]

all_sources = {
    FrontendCafeEventSource.get_source_id(): FrontendCafeEventSource,
    MeetupEventSource.get_source_id(): MeetupEventSource,
}
