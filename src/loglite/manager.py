"""
PADRÃO SINGLETON

O LogManager existe uma única vez no processo e guarda todos os loggers
por nome. Assim, qualquer módulo da aplicação que chamar get_logger("pagamentos")
recebe exatamente o mesmo objeto, com a mesma configuração, sem precisar
passar o logger de mão em mão.
"""

import threading
from typing import Dict, Optional

from .builder import LoggerBuilder
from .logger import Logger


class LogManager:
    """Registro global de loggers (instância única)."""

    _instance: Optional["LogManager"] = None
    _lock = threading.Lock()

    def __new__(cls) -> "LogManager":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._loggers = {}
        return cls._instance

    def register(self, logger: Logger) -> Logger:
        self._loggers[logger.name] = logger
        return logger

    def get_logger(self, name: str = "root") -> Logger:
        """Devolve o logger com esse nome; cria um padrão (console) se não existir."""
        if name not in self._loggers:
            self._loggers[name] = LoggerBuilder(name).build()
        return self._loggers[name]

    def reset(self) -> None:
        """Fecha e remove todos os loggers (útil em testes)."""
        for logger in self._loggers.values():
            logger.close()
        self._loggers.clear()

    _loggers: Dict[str, Logger]


def get_logger(name: str = "root") -> Logger:
    """Atalho para LogManager().get_logger(name)."""
    return LogManager().get_logger(name)
