"""
PADRÃO CHAIN OF RESPONSIBILITY

Os filtros (interceptadores) formam uma corrente. Cada elo pode:
  - barrar o registro (retornando None), interrompendo a corrente;
  - modificar o registro (ex.: mascarar dados sensíveis);
  - repassá-lo ao próximo elo.
O Logger só conhece o primeiro elo, sem saber quantos filtros existem.
"""

import re
from abc import ABC, abstractmethod
from typing import Iterable, Optional

from .levels import LogLevel
from .record import LogRecord


class LogFilter(ABC):
    """Elo da corrente. Subclasses implementam apenas process()."""

    def __init__(self) -> None:
        self._next: Optional["LogFilter"] = None

    def set_next(self, next_filter: "LogFilter") -> "LogFilter":
        """Liga o próximo elo e devolve-o, permitindo a.set_next(b).set_next(c)."""
        self._next = next_filter
        return next_filter

    def handle(self, record: LogRecord) -> Optional[LogRecord]:
        """Processa o registro e, se ele sobreviver, repassa ao próximo elo."""
        result = self.process(record)
        if result is None or self._next is None:
            return result
        return self._next.handle(result)

    @abstractmethod
    def process(self, record: LogRecord) -> Optional[LogRecord]:
        """Retorna o registro (talvez alterado) ou None para descartá-lo."""


class LevelFilter(LogFilter):
    """Descarta registros abaixo de um nível mínimo."""

    def __init__(self, min_level: LogLevel):
        super().__init__()
        self._min_level = min_level

    def process(self, record: LogRecord) -> Optional[LogRecord]:
        return record if record.level >= self._min_level else None


class KeywordBlockFilter(LogFilter):
    """Descarta registros que contenham alguma palavra proibida."""

    def __init__(self, keywords: Iterable[str]):
        super().__init__()
        self._keywords = [k.lower() for k in keywords]

    def process(self, record: LogRecord) -> Optional[LogRecord]:
        text = record.message.lower()
        return None if any(k in text for k in self._keywords) else record


class MaskSensitiveDataFilter(LogFilter):
    """Mascara e-mails e números de cartão antes de qualquer gravação."""

    _EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
    _CARD = re.compile(r"\b(?:\d[ -]?){13,16}\b")

    def process(self, record: LogRecord) -> Optional[LogRecord]:
        masked = self._EMAIL.sub("***@***", record.message)
        masked = self._CARD.sub("**** **** **** ****", masked)
        return record.with_message(masked)
