import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os


# Carrega variáveis do .env
load_dotenv()


def conectar():
    """
    Cria conexão com o banco MySQL.
    """

    try:
        conexao = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT", "3306"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv(
                "DB_NAME",
                "projetoIntegrador"
            )
        )

        if conexao.is_connected():
            return conexao

    except Error as erro:
        print("\n===== ERRO =====")
        print("Não foi possível conectar ao banco.")
        print(f"Detalhe técnico: {erro}")

    return None


def fechar_conexao(conexao=None, cursor=None):
    """
    Fecha cursor e conexão com segurança.
    """

    try:
        if cursor is not None:
            cursor.close()

        if (
            conexao is not None
            and conexao.is_connected()
        ):
            conexao.close()

    except Exception:
        pass
