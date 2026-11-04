"""Níveis de severidade suportados pela biblioteca."""

from enum import IntEnum


class LogLevel(IntEnum):
    """Níveis de log ordenados por severidade (maior = mais grave)."""

    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
