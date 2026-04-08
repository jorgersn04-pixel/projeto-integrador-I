from database import Database


def cadastrar_cliente():
    nome = input("Nome do cliente: ")
    email = input("Email do cliente: ")
    telefone = input("Telefone do cliente: ")

    db = Database()
    conexao = db.conectar()

    if conexao:
        cursor = conexao.cursor()
        sql = """
            INSERT INTO usuarios (nome, email, telefone, tipo)
            VALUES (%s, %s, %s, %s)
        """
        valores = (nome, email, telefone, "cliente")

        try:
            cursor.execute(sql, valores)
            conexao.commit()
            print("Cliente cadastrado com sucesso!")
        except Exception as erro:
            print(f"Erro ao cadastrar cliente: {erro}")
        finally:
            cursor.close()
            db.desconectar()


def cadastrar_tecnico():
    nome = input("Nome do técnico: ")
    email = input("Email do técnico: ")
    telefone = input("Telefone do técnico: ")

    db = Database()
    conexao = db.conectar()

    if conexao:
        cursor = conexao.cursor()
        sql = """
            INSERT INTO usuarios (nome, email, telefone, tipo)
            VALUES (%s, %s, %s, %s)
        """
        valores = (nome, email, telefone, "tecnico")

        try:
            cursor.execute(sql, valores)
            conexao.commit()
            print("Técnico cadastrado com sucesso!")
        except Exception as erro:
            print(f"Erro ao cadastrar técnico: {erro}")
        finally:
            cursor.close()
            db.desconectar()


def listar_usuarios():
    db = Database()
    conexao = db.conectar()

    if conexao:
        cursor = conexao.cursor()
        sql = "SELECT id, nome, email, telefone, tipo FROM usuarios ORDER BY id"

        try:
            cursor.execute(sql)
            resultados = cursor.fetchall()

            if resultados:
                print("\n--- LISTA DE USUÁRIOS ---")
                for usuario in resultados:
                    print(
                        f"ID: {usuario[0]} | "
                        f"Nome: {usuario[1]} | "
                        f"Email: {usuario[2]} | "
                        f"Telefone: {usuario[3]} | "
                        f"Tipo: {usuario[4]}"
                    )
            else:
                print("Nenhum usuário cadastrado.")
        except Exception as erro:
            print(f"Erro ao listar usuários: {erro}")
        finally:
            cursor.close()
            db.desconectar()
