"""Objeto imutável que representa um evento de log."""

from dataclasses import dataclass, field, replace
from datetime import datetime
from typing import Any, Dict

from .levels import LogLevel


@dataclass(frozen=True)
class LogRecord:
    """Um evento de log. Imutável: filtros que alteram o registro devolvem uma cópia."""

    logger_name: str
    level: LogLevel
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    context: Dict[str, Any] = field(default_factory=dict)

    def with_message(self, new_message: str) -> "LogRecord":
        """Retorna uma cópia do registro com outra mensagem."""
        return replace(self, message=new_message)
