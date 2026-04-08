import mysql.connector


class Database:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "SUA_SENHA"
        self.database = "helpdesk_db"
        self.conexao = None

    def conectar(self):
        try:
            self.conexao = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset="utf8"
            )
            return self.conexao
        except mysql.connector.Error as erro:
            print(f"Erro ao conectar ao banco: {erro}")
            return None

    def desconectar(self):
        if self.conexao and self.conexao.is_connected():
            self.conexao.close()
