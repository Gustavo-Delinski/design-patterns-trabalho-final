"""
Destinos de log (appenders).

Os Appenders são os OBSERVADORES do padrão Observer (ver logger.py):
eles se inscrevem no Logger e são notificados a cada evento.
Cada Appender recebe um Formatter (Strategy) por composição.
Para criar um destino novo (banco, Slack, arquivo remoto...), basta herdar de Appender.
"""

import sys
from abc import ABC, abstractmethod
from typing import List, Optional, TextIO

from .formatters import Formatter, TextFormatter
from .levels import LogLevel
from .record import LogRecord


class Appender(ABC):
    """Interface do observador. Implementa a lógica comum; subclasses só escrevem."""

    def __init__(self, formatter: Optional[Formatter] = None,
                 min_level: LogLevel = LogLevel.DEBUG):
        self.formatter = formatter or TextFormatter()
        self.min_level = min_level

    def update(self, record: LogRecord) -> None:
        """Chamado pelo Logger (sujeito) quando há um novo evento."""
        if record.level >= self.min_level:
            self.write(self.formatter.format(record))

    @abstractmethod
    def write(self, text: str) -> None:
        """Grava o texto já formatado no destino."""

    def close(self) -> None:
        """Libera recursos. Padrão: nada a fazer."""


class ConsoleAppender(Appender):
    """Escreve no terminal (stdout por padrão)."""

    def __init__(self, formatter: Optional[Formatter] = None,
                 min_level: LogLevel = LogLevel.DEBUG, stream: TextIO = sys.stdout):
        super().__init__(formatter, min_level)
        self._stream = stream

    def write(self, text: str) -> None:
        print(text, file=self._stream)


class FileAppender(Appender):
    """Acrescenta cada linha ao final de um arquivo."""

    def __init__(self, path: str, formatter: Optional[Formatter] = None,
                 min_level: LogLevel = LogLevel.DEBUG):
        super().__init__(formatter, min_level)
        self._file = open(path, "a", encoding="utf-8")

    def write(self, text: str) -> None:
        self._file.write(text + "\n")
        self._file.flush()

    def close(self) -> None:
        self._file.close()


class MemoryAppender(Appender):
    """Guarda as linhas em uma lista. Útil em testes unitários."""

    def __init__(self, formatter: Optional[Formatter] = None,
                 min_level: LogLevel = LogLevel.DEBUG):
        super().__init__(formatter, min_level)
        self.lines: List[str] = []

    def write(self, text: str) -> None:
        self.lines.append(text)
