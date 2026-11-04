"""
PADRÃO FACTORY METHOD
Define um metodo fábrica abstrato (create_logger) para instanciar loggers
pré-configurados para diferentes contextos/ambientes (Desenvolvimento, Produção),
delegando às subclasses a decisão de quais filtros, formatters e appenders instanciar.
"""

from abc import ABC, abstractmethod

from .appenders import ConsoleAppender, FileAppender
from .builder import LoggerBuilder
from .decorators import AnsiColorFormatter, PrefixFormatter
from .filters import LevelFilter, MaskSensitiveDataFilter
from .formatters import JsonFormatter, TextFormatter
from .levels import LogLevel
from .logger import Logger
from .manager import LogManager


class LoggerFactory(ABC):
    """Criador abstrato que declara o Factory Method."""

    @abstractmethod
    def create_logger(self, name: str) -> Logger:
        """Factory Method: subclasses decidem como instanciar e configurar o Logger."""

    def get_registered_logger(self, name: str) -> Logger:
        """Cria o logger via Factory Method e já o registra no LogManager (Singleton)."""
        logger = self.create_logger(name)
        return LogManager().register(logger)


class DevelopmentLoggerFactory(LoggerFactory):
    """Fábrica para ambiente de desenvolvimento: tudo no console com cores e nível DEBUG."""

    def create_logger(self, name: str) -> Logger:
        colored_formatter = AnsiColorFormatter(PrefixFormatter(TextFormatter(), "[DEV]"))
        return (
            LoggerBuilder(name)
            .with_level(LogLevel.DEBUG)
            .add_appender(ConsoleAppender(colored_formatter))
            .build()
        )


class ProductionLoggerFactory(LoggerFactory):
    """Fábrica para produção: filtra DEBUG, mascara dados sensíveis e grava em JSON."""

    def __init__(self, log_file: str = "production.log") -> None:
        self._log_file = log_file

    def create_logger(self, name: str) -> Logger:
        return (
            LoggerBuilder(name)
            .with_level(LogLevel.INFO)
            .add_filter(LevelFilter(LogLevel.INFO))
            .add_filter(MaskSensitiveDataFilter())
            .add_appender(ConsoleAppender(PrefixFormatter(TextFormatter(), "[PROD]")))
            .add_appender(FileAppender(self._log_file, JsonFormatter()))
            .build()
        )