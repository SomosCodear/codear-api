from __future__ import annotations
import abc
import typing

__all__ = ['EventSource']


class EventSource(abc.ABC):
    SOURCE_ID: str
    SOURCE_NAME: str

    def __init__(self):
        pass

    @classmethod
    def get_source_id(cls):
        return cls.SOURCE_ID

    @classmethod
    def get_source_name(cls):
        return cls.SOURCE_NAME

    @abc.abstractmethod
    def get_new_events(self) -> typing.List[typing.Dict[str, typing.Any]]:
        pass
