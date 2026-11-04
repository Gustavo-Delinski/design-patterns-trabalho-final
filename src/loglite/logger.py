"""
PADRÃO OBSERVER

O Logger é o SUJEITO: mantém uma lista de observadores (Appenders) e,
a cada evento, notifica todos eles. O código que gera logs não precisa saber
para onde os logs vão; adicionar um destino é só chamar subscribe().
"""

from typing import Any, List, Optional

from .appenders import Appender
from .filters import LogFilter
from .levels import LogLevel
from .record import LogRecord


class Logger:
    """Sujeito observado. Passa cada registro pela corrente de filtros e notifica os appenders."""

    def __init__(self, name: str, level: LogLevel = LogLevel.DEBUG,
                 filter_chain: Optional[LogFilter] = None):
        self.name = name
        self.level = level
        self._filter_chain = filter_chain
        self._appenders: List[Appender] = []

    # --- gerenciamento de observadores ---
    def subscribe(self, appender: Appender) -> None:
        self._appenders.append(appender)

    def unsubscribe(self, appender: Appender) -> None:
        self._appenders.remove(appender)

    def _notify(self, record: LogRecord) -> None:
        for appender in self._appenders:
            appender.update(record)

    # --- API pública ---
    def log(self, level: LogLevel, message: str, **context: Any) -> None:
        if level < self.level:
            return
        record: Optional[LogRecord] = LogRecord(self.name, level, message, context=context)
        if self._filter_chain is not None:
            record = self._filter_chain.handle(record)
        if record is not None:
            self._notify(record)

    def debug(self, message: str, **context: Any) -> None:
        self.log(LogLevel.DEBUG, message, **context)

    def info(self, message: str, **context: Any) -> None:
        self.log(LogLevel.INFO, message, **context)

    def warning(self, message: str, **context: Any) -> None:
        self.log(LogLevel.WARNING, message, **context)

    def error(self, message: str, **context: Any) -> None:
        self.log(LogLevel.ERROR, message, **context)

    def critical(self, message: str, **context: Any) -> None:
        self.log(LogLevel.CRITICAL, message, **context)

    def close(self) -> None:
        for appender in self._appenders:
            appender.close()
