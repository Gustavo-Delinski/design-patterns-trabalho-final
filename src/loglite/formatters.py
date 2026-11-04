"""
PADRÃO STRATEGY

Cada Formatter é uma estratégia intercambiável de transformar um LogRecord em texto.
O Appender não sabe COMO formatar; ele apenas delega para a estratégia recebida.
Para criar um formato novo, o cliente herda de Formatter e implementa format().
"""

import json
from abc import ABC, abstractmethod

from .record import LogRecord


class Formatter(ABC):
    """Interface da estratégia de formatação."""

    @abstractmethod
    def format(self, record: LogRecord) -> str:
        """Converte um registro em texto."""


class TextFormatter(Formatter):
    """Formato legível: [2026-10-28 14:00:00] INFO app: mensagem"""

    def __init__(self, pattern: str = "[{time}] {level} {name}: {message}"):
        self._pattern = pattern

    def format(self, record: LogRecord) -> str:
        return self._pattern.format(
            time=record.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            level=record.level.name,
            name=record.logger_name,
            message=record.message,
        )


class JsonFormatter(Formatter):
    """Formato estruturado em JSON, útil para ferramentas de observabilidade."""

    def format(self, record: LogRecord) -> str:
        payload = {
            "timestamp": record.timestamp.isoformat(),
            "level": record.level.name,
            "logger": record.logger_name,
            "message": record.message,
            **record.context,
        }
        return json.dumps(payload, ensure_ascii=False, default=str)
