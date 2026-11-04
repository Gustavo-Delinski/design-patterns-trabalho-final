# LogLite

Biblioteca Python de **logging e telemetria in-process**, leve e extensível, construída com Design Patterns.

## Equipe

- Gustavo Delinski Tavares
- Zhou Ka Shen
- Eduardo Jabur Chede Malaghini

## Vídeo de apresentação

Será adicionado na entrega final

---

## O problema que resolve

Aplicações precisam registrar eventos (erros, auditoria, métricas) em lugares diferentes e em formatos diferentes, às vezes escondendo dados sensíveis. Usar `print` espalhado pelo código mistura tudo isso com a regra de negócio. A LogLite separa **o que** é registrado (Logger), **por onde passa** (Filtros), **como é escrito** (Formatters) e **para onde vai** (Appenders), e permite trocar ou estender cada parte sem mexer na biblioteca.

## Instalação

```bash
pip install git+https://github.com/Gustavo-Delinski/design-patterns-trabalho-final.git

# Ou, após clonar o repositório, execute na pasta que contém o pyproject.toml:
pip install -e .
```

Requer Python 3.9+. Sem dependências externas.

## Uso rápido (out-of-the-box)

```python
from loglite import get_logger

log = get_logger("app")
log.info("Aplicação iniciada")
log.error("Falha ao conectar", tentativa=3)
```

## Uso configurado

```python
from loglite import (LoggerBuilder, LogLevel, LevelFilter, MaskSensitiveDataFilter,
                     ConsoleAppender, FileAppender, JsonFormatter, LogManager)

pagamentos = (
    LoggerBuilder("pagamentos")
    .add_filter(LevelFilter(LogLevel.INFO))
    .add_filter(MaskSensitiveDataFilter())
    .add_appender(ConsoleAppender())
    .add_appender(FileAppender("pagamentos.log", JsonFormatter()))
    .build()
)
LogManager().register(pagamentos)

pagamentos.info("Compra de joao@email.com", valor=99.90)
# -> [2026-10-28 14:51:28] INFO pagamentos: Compra de ***@***
```

### Componentes prontos

| Tipo | Classes prontas |
|---|---|
| Formatters | `TextFormatter`, `JsonFormatter` |
| Filtros | `LevelFilter`, `KeywordBlockFilter`, `MaskSensitiveDataFilter` |
| Appenders | `ConsoleAppender`, `FileAppender`, `MemoryAppender` |

## Estendendo a biblioteca

Herde da classe base e implemente um único método. Nada no código da lib precisa mudar.

```python
from loglite import Formatter, LogFilter, Appender

class CsvFormatter(Formatter):
    def format(self, record):
        return f"{record.timestamp.isoformat()};{record.level.name};{record.message}"

class SomenteProducaoFilter(LogFilter):
    def process(self, record):
        return record if record.context.get("env") == "prod" else None

class SlackAppender(Appender):
    def write(self, text):
        enviar_para_slack(text)
```

Exemplos completos em [`examples/`](examples/).

## Arquitetura e padrões de projeto

| Padrão | Onde | Problema resolvido |
|---|---|---|
| **Strategy** | `formatters.py` | Trocar o formato de saída sem alterar os appenders |
| **Observer** | `logger.py` + `appenders.py` | Enviar um evento para vários destinos sem o Logger conhecê-los |
| **Chain of Responsibility** | `filters.py` | Encadear interceptadores que barram ou alteram o log |
| **Builder** | `builder.py` | Montar um Logger com várias peças opcionais de forma legível |
| **Singleton** | `manager.py` | Recuperar o mesmo logger em qualquer módulo pelo nome |
| **Decorator** | `decorators.py` | Empilhar comportamentos extras (cores, prefixos) em qualquer Formatter sem explosão de subclasses |
| **Factory Method** | `factories.py` | Encapsular a criação de loggers pré-configurados por ambiente (Dev, Prod) permitindo extensão |

## Testes

```bash
pip install pytest
PYTHONPATH=src pytest
```
