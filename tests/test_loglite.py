import json

import pytest

from loglite import (
    JsonFormatter, KeywordBlockFilter, LevelFilter, LoggerBuilder, LogLevel,
    LogManager, MaskSensitiveDataFilter, MemoryAppender, get_logger, AnsiColorFormatter,
    DevelopmentLoggerFactory,
    FormatterDecorator,
    PrefixFormatter,
    TextFormatter,
)


@pytest.fixture(autouse=True)
def limpar_manager():
    LogManager().reset()
    yield
    LogManager().reset()


def test_text_formatter_padrao():
    mem = MemoryAppender()
    log = LoggerBuilder("t").add_appender(mem).build()
    log.info("olá")
    assert "INFO t: olá" in mem.lines[0]


def test_json_formatter_inclui_contexto():
    mem = MemoryAppender(JsonFormatter())
    log = LoggerBuilder("t").add_appender(mem).build()
    log.error("falhou", codigo=500)
    data = json.loads(mem.lines[0])
    assert data["level"] == "ERROR" and data["codigo"] == 500


def test_corrente_de_filtros():
    mem = MemoryAppender()
    log = (LoggerBuilder("t")
           .add_filter(LevelFilter(LogLevel.INFO))
           .add_filter(KeywordBlockFilter(["senha"]))
           .add_filter(MaskSensitiveDataFilter())
           .add_appender(mem).build())
    log.debug("descartado pelo nível")
    log.info("minha senha é 123")
    log.info("contato: ana@x.com")
    assert mem.lines == [mem.lines[0]]
    assert "***@***" in mem.lines[0]


def test_observer_notifica_todos_appenders():
    a, b = MemoryAppender(), MemoryAppender(min_level=LogLevel.ERROR)
    log = LoggerBuilder("t").add_appender(a).add_appender(b).build()
    log.info("x")
    log.error("y")
    assert len(a.lines) == 2 and len(b.lines) == 1


def test_singleton():
    assert LogManager() is LogManager()
    assert get_logger("a") is get_logger("a")


def test_decorator_empilha_formatacoes():
    formatter = AnsiColorFormatter(PrefixFormatter(TextFormatter(), "[API]"))
    mem = MemoryAppender(formatter)
    log = LoggerBuilder("t").add_appender(mem).build()
    log.error("falha critica")
    assert "[API]" in mem.lines[0]
    assert "\033[31m" in mem.lines[0]


def test_factory_method_cria_logger_configurado():
    factory = DevelopmentLoggerFactory()
    log = factory.get_registered_logger("dev_service")
    assert get_logger("dev_service") is log
    assert log.level == LogLevel.DEBUG