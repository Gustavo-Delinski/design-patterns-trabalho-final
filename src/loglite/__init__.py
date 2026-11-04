"""LogLite: biblioteca de logging leve e extensível."""

from .appenders import Appender, ConsoleAppender, FileAppender, MemoryAppender
from .builder import LoggerBuilder
from .decorators import AnsiColorFormatter, FormatterDecorator, PrefixFormatter
from .factories import DevelopmentLoggerFactory, LoggerFactory, ProductionLoggerFactory
from .filters import KeywordBlockFilter, LevelFilter, LogFilter, MaskSensitiveDataFilter
from .formatters import Formatter, JsonFormatter, TextFormatter
from .levels import LogLevel
from .logger import Logger
from .manager import LogManager, get_logger
from .record import LogRecord

__all__ = [
    "Appender", "ConsoleAppender", "FileAppender", "MemoryAppender",
    "LoggerBuilder",
    "FormatterDecorator", "PrefixFormatter", "AnsiColorFormatter",
    "LoggerFactory", "DevelopmentLoggerFactory", "ProductionLoggerFactory",
    "LogFilter", "LevelFilter", "KeywordBlockFilter", "MaskSensitiveDataFilter",
    "Formatter", "TextFormatter", "JsonFormatter",
    "LogLevel", "Logger", "LogManager", "get_logger", "LogRecord",
]

__version__ = "1.0.0"