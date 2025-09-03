from typing import TypedDict

from .context_id import ContextID


class LoggingContext(TypedDict):
    context_id: ContextID
