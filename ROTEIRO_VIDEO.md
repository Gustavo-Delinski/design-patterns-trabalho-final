# Roteiro do vídeo (trio) — ~12 a 15 min

## 1. Visão geral (Aluno 1, ~1 min)
"A LogLite é uma biblioteca Python de logging. O problema que resolve: registar eventos em vários destinos e formatos, filtrando e mascarando dados sensíveis, sem misturar isso com a regra de negócio e permitindo que o desenvolvedor estenda tudo sem alterar a lib."

## 2. Uso prático padrão (Aluno 2, ~1.5 min)
- Executar `examples/uso_padrao.py`: mostrar a fábrica (`DevelopmentLoggerFactory`), a recuperação do mesmo objeto via `get_logger` (Singleton), o Builder, a máscara de e-mail/cartão e o ficheiro JSON gerado.

## 3. Uso prático estendido (Aluno 3 - Eduardo, ~1.5 min)
- Executar `examples/uso_estendido.py`: demonstrar a extensibilidade (Open/Closed Principle). 
- Destacar que o cliente (desenvolvedor) conseguiu criar novos formatadores, filtros, appenders, decoradores personalizados (ex: `TruncateFormatter`) e fábricas (ex: `AuditLoggerFactory`) no seu próprio projeto sem tocar no código original da pasta `src/`.

## 4. Defesa arquitetural (Foco da avaliação)

### Aluno 1 — Strategy e Observer

**Strategy** (`formatters.py`)
- Interface `Formatter` com o método `format()`; `TextFormatter` e `JsonFormatter` são estratégias concretas.
- O `Appender` recebe a estratégia por composição (`self.formatter`) e apenas chama `format()`.
- Problema resolvido: sem isto, cada appender teria um `if formato == "json"...`. Um formato novo obrigaria a alterar todos os appenders. Com Strategy, qualquer appender aceita qualquer formatter, e o cliente cria o `CsvFormatter` sem mexer na biblioteca.

**Observer** (`logger.py`, `appenders.py`)
- `Logger` é o sujeito: métodos `subscribe()`, `unsubscribe()`, `_notify()`.
- `Appender` é o observador: método `update()`.
- Problema resolvido: um mesmo evento precisa ir para a consola, ficheiro e alerta simultaneamente. O Logger não sabe que destinos existem; apenas percorre a lista. Adicionar um destino = `subscribe`, sem alterar o Logger (baixo acoplamento).

### Aluno 2 — Chain of Responsibility e Builder

**Chain of Responsibility** (`filters.py`)
- `LogFilter` possui `_next`, `set_next()` e `handle()`; as subclasses apenas implementam `process()`.
- Cada elo da corrente pode descartar (retorna `None`, interrompendo o fluxo), modificar (`MaskSensitiveDataFilter`) ou repassar o registo.
- Problema resolvido: cumpre o requisito de "intercetar os logs". Os filtros são independentes, combináveis e a ordem é totalmente configurável. O Logger apenas conhece o primeiro elo.

**Builder** (`builder.py`)
- `LoggerBuilder` com métodos fluentes `with_level`, `add_filter`, `add_appender`, `build`.
- O método `build()` interliga os elos da corrente de filtros (`_link_filters`) e inscreve os appenders.
- Problema resolvido: um Logger tem demasiadas peças opcionais. Sem o Builder, o cliente teria de encadear os filtros manualmente e lidar com um construtor com dezenas de parâmetros. O Builder torna a configuração legível e encapsula a complexidade da montagem.

### Aluno 3 (Eduardo) — Decorator e Factory Method

**Decorator** (`decorators.py`)
- Onde foi implementado: Classe base `FormatterDecorator` que recebe outro `Formatter` no construtor. Implementações concretas `PrefixFormatter` e `AnsiColorFormatter`.
- Problema resolvido: Para adicionar cores na consola, truncamento de texto ou prefixos de ambiente a formatos já existentes, teríamos de criar uma explosão combinatória de subclasses (`ColoredJsonFormatter`, `ColoredTextFormatter`, etc.). O Decorator resolve o problema permitindo empilhar comportamentos extras sobre qualquer estratégia de formatação de forma dinâmica.

**Factory Method** (`factories.py`)
- Onde foi implementado: Classe abstrata `LoggerFactory` (com o método fábrica `create_logger`) e subclasses concretas `DevelopmentLoggerFactory` e `ProductionLoggerFactory`.
- Problema resolvido: Evita que o desenvolvedor tenha de instanciar o Builder repetidamente com a mesma longa configuração em vários pontos do sistema. Centraliza a criação de loggers pré-configurados por ambiente, permitindo ao cliente criar as suas próprias fábricas de contexto (como a `AuditLoggerFactory` no exemplo estendido).

### Extra
**Singleton** (`manager.py`): A classe `LogManager` com controlo de concorrência (`__new__` e lock) garante que a chamada `get_logger("pagamentos")` devolve exatamente a mesma instância configurada em qualquer módulo do projeto.