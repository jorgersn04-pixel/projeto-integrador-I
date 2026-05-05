import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def conectar():
    """Estabelece a conexão com o banco de dados de forma portátil."""
    try:
        conexao = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT', '3306'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME')
        )
        if conexao.is_connected():
            return conexao
    except Error as e:
        print(f"\n Falha Crítica: Não foi possível conectar ao servidor MySQL.")
        print(f" Verifique se o arquivo .env está correto e se você tem acesso à rede.")
        print(f"Detalhe técnico: {e}")
        return None

def fechar_conexao(conexao, cursor):
    """Garante o encerramento seguro e liberação de memória."""
    try:
        if cursor is not None:
            cursor.close()
        if conexao is not None and conexao.is_connected():
            conexao.close()
    except Exception:
        pass
