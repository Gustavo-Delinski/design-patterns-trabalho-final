"""Exemplo 1: uso out-of-the-box, só com classes prontas da biblioteca."""

from loglite import (
    ConsoleAppender, FileAppender, JsonFormatter, LevelFilter, LoggerBuilder,
    LogLevel, LogManager, MaskSensitiveDataFilter, get_logger,
)

# Uso mais simples possível: um logger padrão que escreve no console.
log = get_logger("app")
log.info("Aplicação iniciada")

# Uso configurado com o Builder.
pagamentos = (
    LoggerBuilder("pagamentos")
    .with_level(LogLevel.DEBUG)
    .add_filter(LevelFilter(LogLevel.INFO))       # descarta DEBUG
    .add_filter(MaskSensitiveDataFilter())        # esconde e-mail e cartão
    .add_appender(ConsoleAppender())              # texto no terminal
    .add_appender(FileAppender("pagamentos.log", JsonFormatter()))  # JSON no arquivo
    .build()
)
LogManager().register(pagamentos)

pagamentos.debug("isto não aparece")
pagamentos.info("Compra de joao@email.com no cartão 4111 1111 1111 1111", valor=99.90)
pagamentos.error("Falha no gateway", codigo=502)

# Em qualquer outro módulo, o mesmo logger é recuperado pelo nome (Singleton).
assert get_logger("pagamentos") is pagamentos
pagamentos.close()

# Uso com Factory Method e Decorator (out-of-the-box)
from loglite import DevelopmentLoggerFactory

dev_factory = DevelopmentLoggerFactory()
log_dev = dev_factory.get_registered_logger("autenticacao")
log_dev.debug("Token JWT gerado com sucesso")
log_dev.warning("Tentativa de login lenta")
