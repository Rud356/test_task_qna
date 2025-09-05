from secrets import token_hex
from typing import NewType

ContextID = NewType("ContextID", str)


def generate_context_id() -> ContextID:
    """
    Generates new context id.

    :return: New context id.
    """
    return ContextID(token_hex(16).upper())
