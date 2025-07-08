# sea-api

Esta documentação descreve a arquitetura e os detalhes de implementação de um projeto Python usando o framework FastAPI, seguindo o padrão de arquitetura Hexagonal (também conhecido como Ports and Adapters).

## Visão Geral
O projeto segue a [arquitetura Hexagonal](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)) para garantir a separação clara de preocupações e facilitar a manutenção e testabilidade do código. Ele é dividido em várias camadas principais:

1. **Aplicação**: A camada de aplicação contém as regras de negócios do sistema e depende das portas (interfaces) para interagir com o mundo externo.

2. **Adaptadores**: Os adaptadores conectam a camada de aplicação às portas externas, como APIs HTTP, bancos de dados, ou qualquer outro sistema externo.

3. **Portas**: As portas são interfaces que definem como a camada de aplicação se comunica com o mundo externo. Elas são implementadas pelos adaptadores.

## Configuração das Variáveis de Ambiente

Para configurar corretamente seu ambiente de desenvolvimento, você precisa definir as variáveis de ambiente necessárias. Você pode fazer isso criando um arquivo `.env` no diretório raiz do seu projeto e definindo as variáveis nele. Aqui estão as variáveis de ambiente necessárias:

```env
SECRET_KEY=<seu_valor_secreto>

DB_HOST=<seu_host_do_banco_de_dados>
DB_USER=<seu_usuario_do_banco_de_dados>
DB_NAME=<seu_nome_do_banco_de_dados>
DB_PASS=<sua_senha_do_banco_de_dados>
DB_PORT=<sua_porta_do_banco_de_dados>

SUPERUSER_EMAIL=<seu_email_do_superusuario>
SUPERUSER_PASSWORD=<sua_senha_do_superusuario>

MAIL_FROM=<seu_email_de_envio>
MAIL_FROM_NAME=<seu_nome_de_envio>
MAIL_SERVER=<seu_servidor_de_email>
MAIL_PORT=<sua_porta_do_servidor_de_email>
MAIL_USER=<seu_usuario_do_email>
MAIL_PASSWORD=<sua_senha_do_email>

STORAGE_PROVIDER=<seu_provedor_de_armazenamento>
STORAGE_ENDPOINT_URL=<sua_url_do_endpoint_de_armazenamento>
STORAGE_ACCESS_KEY=<sua_chave_de_acesso_do_armazenamento>
STORAGE_SECRET_KEY=<sua_chave_secreta_do_armazenamento>
STORAGE_BUCKET=<seu_bucket_de_armazenamento>

API_BASE_URL=<sua_url_base_da_API>
WEB_APP_BASE_URL=<sua_url_base_do_aplicativo_web>

ALLOW_ORIGINS=<suas_origens_permitidas>

```
## Configuração do Ambiente de Desenvolvimento

### Instalação do `pipenv`

O `pipenv` é uma ferramenta útil para gerenciar ambientes virtuais e dependências Python em projetos. Para configurar seu ambiente de desenvolvimento, siga estas etapas:

#### Passo 1: Instale o Python (se necessário)

Se você ainda não tem o Python instalado no seu sistema, faça o download e instale a versão mais recente do Python a partir do [site oficial](https://www.python.org/downloads/). Certifique-se de marcar a opção "Adicionar ao PATH" durante a instalação.

#### Passo 2: Instale o `pipenv`

Após ter o Python instalado, abra seu terminal e execute o seguinte comando para instalar o `pipenv` globalmente:

```bash
pip install pipenv
``````

#### Passo 3: Instalação de Dependências de Desenvolvimento

Antes de executar o projeto, é necessário instalar as dependências de desenvolvimento. Para fazer isso, execute o seguinte comando:

```bash
make install-dev
``````

#### Passo 4: Migração do Banco de Dados


Agora o passo de migração do banco de dados está incluído diretamente no README. Certifique-se de substituir `make migrate` pelo comando real que você usa para executar as migrações do banco de dados em seu projeto.

```bash
make migrate
``````
### Executando o Projeto

Agora que você configurou as variáveis de ambiente e migrou o banco de dados, você pode executar o projeto. Para iniciar a aplicação, execute o seguinte comando:

```bash
make run
```

## Rodando Linting e Testes

Para garantir a qualidade do código e a conformidade com as diretrizes do projeto, você pode executar tarefas de linting e testes. Certifique-se de que seu ambiente virtual `pipenv` esteja ativado antes de executar esses comandos.

Claro, você pode adicionar uma seção no README para explicar como rodar as tarefas de linting e testes usando os comandos `make format`, `make lint` e `make test`. Aqui está a seção atualizada:

## Rodando Linting e Testes

Para garantir a qualidade do código e a conformidade com as diretrizes do projeto, você pode executar tarefas de linting e testes. Certifique-se de que seu ambiente virtual `pipenv` esteja ativado antes de executar esses comandos.

### Formatação do Código

Você pode usar o seguinte comando para formatar automaticamente o código do projeto de acordo com as regras de estilo definidas:

```bash
make format
```

Isso usará uma ferramenta de formatação, como o `black`, para aplicar a formatação correta ao código.

### Verificação de Estilo (Linting)

Para verificar seu código em busca de problemas de estilo e possíveis erros, você pode executar o seguinte comando:

```bash
make lint
```

Isso usará uma ferramenta de linting, como o `flake8`, para verificar seu código em busca de conformidade com as diretrizes de estilo definidas no projeto.

### Execução de Testes

Para executar os testes automatizados do projeto, utilize o seguinte comando:

```bash
make test
```

Isso executará todos os testes unitários e de integração definidos no projeto e relatará os resultados.

Certifique-se de que todos os testes passam antes de fazer contribuições ou implantar alterações no projeto.


Com esta seção, os desenvolvedores que usam o projeto terão instruções claras sobre como rodar tarefas de linting e testes para manter a qualidade do código. Certifique-se de que os comandos `make format`, `make lint` e `make test` estejam configurados no seu Makefile de acordo com as ferramentas de formatação, linting e testes que você utiliza no seu projeto.


Entendido, vou explicar como rodar o Docker Compose para configurar o ambiente do banco de dados PostgreSQL e como configurar o banco de dados usando o arquivo `.env` dentro do diretório `.docker/postgres`.

### Rodando o Docker Compose

Para configurar e executar o ambiente do banco de dados PostgreSQL usando o Docker Compose, siga estas etapas:

#### 1. Definindo Variáveis de Ambiente

Primeiro, crie um arquivo `.env` dentro do diretório `.docker/postgres` com o seguinte formato:

```env
POSTGRES_PASSWORD=<senha_do_postgres>
POSTGRES_USER=<usuario_do_postgres>
POSTGRES_DB=<nome_do_banco_de_dados>
```

Substitua `<senha_do_postgres>`, `<usuario_do_postgres>` e `<nome_do_banco_de_dados>` pelos valores desejados para sua configuração do banco de dados PostgreSQL.

#### 2. Rodando o Docker Compose

Certifique-se de que você tenha o Docker e o Docker Compose instalados em seu sistema. Em seguida, no terminal, navegue até o diretório raiz do seu projeto onde está localizado o arquivo `docker-compose.yml`.

Execute o seguinte comando para iniciar o ambiente do Docker Compose:

```bash
docker-compose up -d
```

Isso iniciará o contêiner PostgreSQL em segundo plano, usando as configurações definidas no arquivo `docker-compose.yml`. O PostgreSQL estará agora em execução e pronto para ser usado por sua aplicação.

### Conectando e Configurando o Banco de Dados

Agora que o PostgreSQL está em execução, você pode configurar e conectar-se ao banco de dados da seguinte maneira:

- **Host**: O host do banco de dados será `localhost`.

- **Porta**: A porta padrão é `5432`.

- **Credenciais**: Use as credenciais definidas no arquivo `.env` para o usuário (`POSTGRES_USER`) e senha (`POSTGRES_PASSWORD`).

- **Nome do Banco de Dados**: O nome do banco de dados será `POSTGRES_DB`.

Certifique-se de que sua aplicação esteja configurada para se conectar a essas informações.

Com estas etapas, você configurou com sucesso o ambiente do banco de dados PostgreSQL usando o Docker Compose e definiu as variáveis de ambiente no arquivo `.env`. Agora, sua aplicação deve ser capaz de se conectar ao banco de dados PostgreSQL em execução.

### Tecnologias utilizadas

 - [Docker](https://www.docker.com/) <img align="center" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original-wordmark.svg" />

 - [PostgresQL](https://www.postgresql.org)

 - [FastAPI](https://fastapi.tiangolo.com)
