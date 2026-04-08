from database import Database


def abrir_chamado():
    id_cliente = input("ID do cliente: ")
    titulo = input("Título do chamado: ")
    descricao = input("Descrição do problema: ")

    db = Database()
    conexao = db.conectar()

    if conexao:
        cursor = conexao.cursor()

        sql = """
            INSERT INTO chamados (id_cliente, titulo, descricao, status)
            VALUES (%s, %s, %s, %s)
        """
        valores = (id_cliente, titulo, descricao, "Aberto")

        try:
            cursor.execute(sql, valores)
            conexao.commit()
            print("Chamado aberto com sucesso!")
        except Exception as erro:
            print(f"Erro ao abrir chamado: {erro}")
        finally:
            cursor.close()
            db.desconectar()


def listar_chamados():
    db = Database()
    conexao = db.conectar()

    if conexao:
        cursor = conexao.cursor()
        sql = """
            SELECT c.id, u.nome, c.titulo, c.descricao, c.status, c.data_abertura
            FROM chamados c
            INNER JOIN usuarios u ON c.id_cliente = u.id
            ORDER BY c.id
        """

        try:
            cursor.execute(sql)
            resultados = cursor.fetchall()

            if resultados:
                print("\n--- LISTA DE CHAMADOS ---")
                for chamado in resultados:
                    print(f"""
ID: {chamado[0]}
Cliente: {chamado[1]}
Título: {chamado[2]}
Descrição: {chamado[3]}
Status: {chamado[4]}
Data de abertura: {chamado[5]}
------------------------------
""")
            else:
                print("Nenhum chamado encontrado.")
        except Exception as erro:
            print(f"Erro ao listar chamados: {erro}")
        finally:
            cursor.close()
            db.desconectar()


def atualizar_status_chamado():
    id_chamado = input("ID do chamado: ")
    novo_status = input("Novo status (Aberto / Em andamento / Fechado): ")

    db = Database()
    conexao = db.conectar()

    if conexao:
        cursor = conexao.cursor()
        sql = """
            UPDATE chamados
            SET status = %s
            WHERE id = %s
        """
        valores = (novo_status, id_chamado)

        try:
            cursor.execute(sql, valores)
            conexao.commit()

            if cursor.rowcount > 0:
                print("Status atualizado com sucesso!")
            else:
                print("Chamado não encontrado.")
        except Exception as erro:
            print(f"Erro ao atualizar status: {erro}")
        finally:
            cursor.close()
            db.desconectar()


def atribuir_tecnico():
    id_chamado = input("ID do chamado: ")
    id_tecnico = input("ID do técnico: ")

    db = Database()
    conexao = db.conectar()

    if conexao:
        cursor = conexao.cursor()
        sql = """
            UPDATE chamados
            SET id_tecnico = %s
            WHERE id = %s
        """
        valores = (id_tecnico, id_chamado)

        try:
            cursor.execute(sql, valores)
            conexao.commit()

            if cursor.rowcount > 0:
                print("Técnico atribuído com sucesso!")
            else:
                print("Chamado não encontrado.")
        except Exception as erro:
            print(f"Erro ao atribuir técnico: {erro}")
        finally:
            cursor.close()
            db.desconectar()
