# SóPapo – Aplicação de chat de conversas baseado no whatsApp

Descrição:

SóPapo é uma plataforma de mensagens em tempo real desenvolvida com Flask no backend e React.js no frontend. O sistema permite comunicação em grupos de estudo, trabalho ou lazer, com recursos como criação de salas, troca de mensagens, compartilhamento de arquivos e mais.


# Funcionalidades:

* Cadastro e autenticação de usuários (JWT)
* Criação e gerenciamento de salas de conversa
* Envio e recebimento de mensagens em tempo real (WebSockets)
* Controle de permissões para participantes
* Indicadores de leitura e entrega
* Compartilhamento de arquivos (Desafio de implementação)



# Tecnologias Utilizadas backend:

Flask – Framework para desenvolvimento da API
Flask-SQLAlchemy – ORM para gerenciamento do banco de dados
Flask-JWT-Extended – Autenticação via tokens JWT
Flask-SocketIO – Suporte para comunicação em tempo real
PostgreSQL – Banco de dados relacional
WebSockets – Comunicação em tempo real


# Tecnologias para o frontend (ainda não implementado)

React.js – Interface do usuário
Redux – Gerenciamento de estado


# Estrutura do Projeto

```
sopapo-backend/
├── doc                  # arquivos solicitados pelo professor
├── teste1.py            # arquivo de teste para aplicação
├── app.py               # Arquivo principal da aplicação Flask
├── config.py            # Configurações do sistema
├── extensions.py        # Inicialização das extensões Flask
├── models/              # Modelos do banco de dados      
│   ├── models.py
├── routes/              # Rotas da API
│   ├── auth.py
├── templates/           # Sem uso 
├── requirements.txt     # Dependências do projeto
└── README.md            # Documentação do projeto
```


# Antes de instalar, você precisa ter:

Python 3.10+
PostgreSQL instalado (ainda não funcionando a conexaão com o banco de dados)
Node.js (caso vá rodar o frontend no futuro)


# Instalação e Execução
🔹 1. Clonar o repositório

HTTPs: https://github.com/lucasBalmantcoder/so_papo.git
SSH: git@github.com:lucasBalmantcoder/so_papo.git

🔹 2. Criar e ativar ambiente virtual

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

🔹 3. Instalar dependências

pip install -r requirements.txt

🔹 4. Configurar banco de dados

    AINDA NÃO FUNCIONA.

🔹  5. Rodar a aplicação

flask run


python app.py

# testes

A API estará rodando em http://127.0.0.1:5000

* execute o test.py para fazer a conexãono servidor.
* adicione um nome de usuário e a sala
* para os testes, usei:

* user: user1
* room: room1

após conexão, é só mandar as mensagens para os outros usuários.
