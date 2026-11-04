"""
PADRÃO DECORATOR
Permite envolver (wrap) qualquer Formatter existente para adicionar novos
comportamentos (cores ANSI, prefixos, truncamento) dinamicamente.
Evita a explosão de subclasses (ex.: ColoredTextFormatter, ColoredJsonFormatter)
e permite empilhar múltiplos decoradores sobre qualquer estratégia de formatação.
"""

from .formatters import Formatter
from .levels import LogLevel
from .record import LogRecord


class FormatterDecorator(Formatter):
    """Decorador base que mantém uma referência para outro Formatter."""

    def __init__(self, wrapped: Formatter) -> None:
        self._wrapped = wrapped

    def format(self, record: LogRecord) -> str:
        return self._wrapped.format(record)


class PrefixFormatter(FormatterDecorator):
    """Adiciona um prefixo fixo (ex.: tag de ambiente ou serviço) ao texto formatado."""

    def __init__(self, wrapped: Formatter, prefix: str) -> None:
        super().__init__(wrapped)
        self._prefix = prefix

    def format(self, record: LogRecord) -> str:
        base_text = super().format(record)
        return f"{self._prefix} {base_text}"


class AnsiColorFormatter(FormatterDecorator):
    """Adiciona cores ANSI ao texto formatado de acordo com o nível de severidade."""

    _COLORS = {
        LogLevel.DEBUG: "\033[36m",     # Ciano
        LogLevel.INFO: "\033[32m",      # Verde
        LogLevel.WARNING: "\033[33m",   # Amarelo
        LogLevel.ERROR: "\033[31m",     # Vermelho
        LogLevel.CRITICAL: "\033[1;35m" # Magenta negrito
    }
    _RESET = "\033[0m"

    def format(self, record: LogRecord) -> str:
        base_text = super().format(record)
        color = self._COLORS.get(record.level, "")
        if not color:
            return base_text
        return f"{color}{base_text}{self._RESET}"