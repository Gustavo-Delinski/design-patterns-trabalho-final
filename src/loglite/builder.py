"""
PADRÃO BUILDER

Montar um Logger envolve várias peças opcionais: nível, filtros encadeados
e vários appenders, cada um com seu formatter. O LoggerBuilder oferece uma
interface fluente que monta tudo passo a passo e esconde a ligação dos elos
da corrente de filtros, evitando construtores enormes e confusos.
"""

from typing import List, Optional

from .appenders import Appender, ConsoleAppender
from .filters import LogFilter
from .levels import LogLevel
from .logger import Logger


class LoggerBuilder:
    """Constrói um Logger configurado de forma fluente."""

    def __init__(self, name: str = "root"):
        self._name = name
        self._level = LogLevel.DEBUG
        self._filters: List[LogFilter] = []
        self._appenders: List[Appender] = []

    def with_level(self, level: LogLevel) -> "LoggerBuilder":
        self._level = level
        return self

    def add_filter(self, log_filter: LogFilter) -> "LoggerBuilder":
        self._filters.append(log_filter)
        return self

    def add_appender(self, appender: Appender) -> "LoggerBuilder":
        self._appenders.append(appender)
        return self

    def _link_filters(self) -> Optional[LogFilter]:
        """Encadeia os filtros na ordem em que foram adicionados."""
        if not self._filters:
            return None
        for current, nxt in zip(self._filters, self._filters[1:]):
            current.set_next(nxt)
        return self._filters[0]

    def build(self) -> Logger:
        logger = Logger(self._name, self._level, self._link_filters())
        for appender in self._appenders or [ConsoleAppender()]:
            logger.subscribe(appender)
        return logger
