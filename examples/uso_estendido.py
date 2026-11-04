"""
Exemplo 2: o cliente ESTENDE a biblioteca sem alterar o código dela (Open/Closed).

Criamos três classes próprias:
  - CsvFormatter      -> novo formato (Strategy)
  - HorarioComercialFilter -> novo interceptador (Chain of Responsibility)
  - AlertaAppender    -> novo destino (Observer)
"""

from datetime import datetime
from typing import Optional

from loglite import (
    Appender, ConsoleAppender, Formatter, LogFilter, LoggerBuilder, LogLevel, LogRecord, FormatterDecorator, LoggerFactory, MemoryAppender, TextFormatter, Logger
)


class CsvFormatter(Formatter):
    def format(self, record: LogRecord) -> str:
        return f"{record.timestamp.isoformat()};{record.level.name};{record.message}"


class HorarioComercialFilter(LogFilter):
    """Fora do horário comercial, só deixa passar erros."""

    def process(self, record: LogRecord) -> Optional[LogRecord]:
        hora = record.timestamp.hour
        if 8 <= hora < 18 or record.level >= LogLevel.ERROR:
            return record
        return None


class AlertaAppender(Appender):
    """Simula o envio de um alerta (ex.: e-mail, Slack, Telegram)."""

    def write(self, text: str) -> None:
        print(f"🚨 ALERTA ENVIADO -> {text}")


logger = (
    LoggerBuilder("estoque")
    .add_filter(HorarioComercialFilter())
    .add_appender(AlertaAppender(CsvFormatter(), min_level=LogLevel.ERROR))
    .add_appender(ConsoleAppender())  # também mostra tudo no terminal
    .build()
)

print("Agora são", datetime.now().strftime("%H:%M"))
logger.info("Produto cadastrado")
logger.error("Estoque negativo para o produto 42")

class TruncateFormatter(FormatterDecorator):
    def __init__(self, wrapped: Formatter, max_len: int = 40) -> None:
        super().__init__(wrapped)
        self._max_len = max_len

    def format(self, record: LogRecord) -> str:
        text = super().format(record)
        return text if len(text) <= self._max_len else text[:self._max_len] + "..."

class AuditLoggerFactory(LoggerFactory):
    def __init__(self) -> None:
        self.memory = MemoryAppender(TruncateFormatter(CsvFormatter(), max_len=50))

    def create_logger(self, name: str) -> Logger:
        return (
            LoggerBuilder(name)
            .with_level(LogLevel.INFO)
            .add_appender(self.memory)
            .build()
        )

audit_factory = AuditLoggerFactory()
audit_log = audit_factory.create_logger("auditoria")
audit_log.info("Operação crítica realizada pelo administrador do sistema central")
print("Auditoria capturada:", audit_factory.memory.lines)