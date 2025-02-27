# SóPapo – Aplicação de chat de conversas baseado no whatsApp

Descrição:

SóPapo é uma plataforma de mensagens em tempo real desenvolvida com Flask no backend e React.js no frontend. O sistema permite comunicação por mensagens, com o recurso de criação de sala e gerenciamento de sala.


# Funcionalidades:

```
* Cadastro e autenticação de usuários (JWT).
* Criação e gerenciamento de salas de conversa.
* Envio e recebimento de mensagens.
* Controle de acesso, (só poderá mandar msg os que são participantes das salas)

* Indicadores de leitura e entrega (não funcional)
* Compartilhamento de arquivos (não funcional)
```


# Tecnologias Utilizadas backend:
```
Flask – Framework para desenvolvimento da API
Flask-SQLAlchemy – ORM para gerenciamento do banco de dados
Flask-JWT-Extended – Autenticação via tokens JWT
Flask-SocketIO – Suporte para comunicação em tempo real (implementado, mas não usado no projeto atual)
PostgreSQL – Banco de dados relacional
WebSockets – Comunicação em tempo real
```
# Estrutura do Projeto

```

├── app.py-----------------------------------------(Inicializador do projeto, ponto de entrada da aplicação Flask)
├── auth
│   ├── exception.py------------------------------(Define exceções personalizadas para autenticação e autorização)
│   ├── hash.py-----------------------------------(Lida com hash de senhas e segurança)
│   ├── jwt.py------------------------------------(Gerenciamento de tokens JWT para autenticação)
│   │   ├── grupos.py----------------------------(Gerenciamento de grupos no sistema)
│   │   ├── hash.py------------------------------(Funções relacionadas a hash e segurança)
│   │   ├── jwt.py--------------------------------(Autenticador JWT)
│   │   ├── rooms.py-----------------------------(Não usado atualmente)
│   │   ├── routes.py----------------------------(Novas rotas do projeto)
│   │   └── schemas.pyc--------------------------(Esquema de dados compilado)
│   ├── rooms.py---------------------------------(Gerenciamento de salas e participantes)
│   ├── routes.py--------------------------------(Define as rotas de autenticação do sistema)
│   └── schemas.py------------------------------(Define os esquemas de dados para validação)
├── config.py------------------------------------(Configurações gerais do projeto, como conexões e variáveis de ambiente)
├── datebase
│   └── create_db.py----------------------------(Script para criação do banco de dados)
├── doc
│   ├── Modelo de banco de dados.png------------(Imagem representando o modelo do banco de dados)
│   └── DVP SD SóPapo.docx.pdf------------------(Documentação do projeto)
├── extensions.py--------------------------------(Extensões e configurações adicionais para a aplicação)
├── migration-----------------------------------(Diretório para controle de migrações do banco de dados)
├── models
│   └── models.py-------------------------------(Define os modelos de dados do banco de dados usando SQLAlchemy)
├── README.md----------------------------------(Arquivo de documentação geral do projeto)
├── requirements.txt---------------------------(Lista de dependências necessárias para rodar o projeto)
├── routes
│   └── auth.py---------------------------------(Antiga rota de autenticação do projeto, atualmente não usada)
├── sockets.py---------------------------------(Configuração do WebSockets para mensagens em tempo real)
├── templates
│   └── index.html-----------------------------(Modelo de página HTML para renderização no backend)
├── testadb.py---------------------------------(Não usado atualmente)
├── teste1.py----------------------------------(Arquivos de teste e debug)
├── teste2.py----------------------------------(Arquivos de teste e debug)
└── utils.py-----------------------------------(Não usado atualmente)
```




# Antes de instalar, você precisa ter:
```
Python 3.10+
PostgreSQL instalado (ainda não funcionando a conexaão com o banco de dados)
Node.js (caso vá rodar o frontend no futuro)
```

 Instalação e Execução

#  1. Clonar o repositório
```
HTTPs: https://github.com/lucasBalmantcoder/so_papo.git
SSH: git@github.com:lucasBalmantcoder/so_papo.git
```
#  2. Criar e ativar ambiente virtual
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows
```
# 3. Instalar dependências
```
pip install -r requirements.txt
```
# 4. Configurar banco de dados
```
Na pasta .env configure o link do db postgree

APP_NAME=so_papo

# Chave secreta para segurança
SECRET_KEY= "example"

# Configuração do Banco de Dados
POSTGRES_USER="example"
POSTGRES_PASSWORD="example"

POSTGRES_HOST="localhost"  # Ou o endereço do servidor do banco de dados

POSTGRES_PORT="5432"  # Porta padrão do PostgreSQL

POSTGRES_DB=" seubancoaqui " # adicione o nome do seu banco de dados

# URL do banco de dados para SQLAlchemy
DATABASE_URL=postgresql://example:example@localhost:5432/seubancoaqui

# Configuração do JWT

JWT_SECRET_KEY=sua_chave_jwt
```
# 5. Rodar a aplicação
```
flask run

python app.py
```
# testes
```
A API estará rodando em http://127.0.0.1:5000

```