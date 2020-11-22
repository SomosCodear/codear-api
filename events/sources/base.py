from __future__ import annotations
import abc
import typing
from events import models

__all__ = ['EventSource']


class EventSource(abc.ABC):
  @classmethod
  def get_source_id(cls):
    return cls.SOURCE_ID

  @classmethod
  def get_source_name(cls):
    return cls.SOURCE_NAME

  @abc.abstractmethod
  def get_new_events(self) -> typing.List[models.Event]:
    pass
