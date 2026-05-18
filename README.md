# SCSC - Sistema de Controle de Solicitações Corporativas

## Descrição

Sistema desenvolvido em Python e MySQL para gerenciamento de solicitações corporativas.

O sistema permite:

- Cadastro de usuários
- Login por perfil
- Abertura de solicitações
- Classificação automática de prioridade
- Atribuição de técnicos
- Atualização de status
- Estatísticas de solicitações

---

# Tecnologias utilizadas

- Python 3
- MySQL
- mysql-connector-python
- python-dotenv

---

# Estrutura do projeto

SCSC/
│
├── main.py
├── services.py
├── database.py
├── banco.sql
├── .env
├── .gitignore
├── requirements.txt
└── README.md

---

# Como executar o projeto

## 1. Clone o repositório

git clone LINK_DO_REPOSITORIO

---

## 2. Crie o ambiente virtual

### Windows

python -m venv venv

---

## 3. Ative o ambiente virtual

### Windows

venv\Scripts\activate

### Linux/Mac

source venv/bin/activate

---

## 4. Instale as dependências

pip install -r requirements.txt

---

# Configuração do banco

## 1. Abra o MySQL Workbench

Execute o arquivo:

banco.sql

Isso criará:
- banco de dados
- tabelas
- usuários iniciais

---

## 2. Configure o arquivo .env

Crie um arquivo chamado:

.env

na raiz do projeto.

Adicione:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASS=sua_senha
DB_NAME=projetoIntegrador
