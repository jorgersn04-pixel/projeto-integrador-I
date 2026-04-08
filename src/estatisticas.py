from database import Database


def total_chamados():
    db = Database()
    conexao = db.conectar()

    if conexao:
        cursor = conexao.cursor()
        sql = "SELECT COUNT(*) FROM chamados"

        try:
            cursor.execute(sql)
            resultado = cursor.fetchone()
            print(f"Total de chamados: {resultado[0]}")
        except Exception as erro:
            print(f"Erro ao consultar total de chamados: {erro}")
        finally:
            cursor.close()
            db.desconectar()


def chamados_por_status():
    db = Database()
    conexao = db.conectar()

    if conexao:
        cursor = conexao.cursor()
        sql = """
            SELECT status, COUNT(*)
            FROM chamados
            GROUP BY status
        """

        try:
            cursor.execute(sql)
            resultados = cursor.fetchall()

            print("\n--- CHAMADOS POR STATUS ---")
            for status, quantidade in resultados:
                print(f"{status}: {quantidade}")
        except Exception as erro:
            print(f"Erro ao consultar chamados por status: {erro}")
        finally:
            cursor.close()
            db.desconectar()


def chamados_por_tecnico():
    db = Database()
    conexao = db.conectar()

    if conexao:
        cursor = conexao.cursor()
        sql = """
            SELECT u.nome, COUNT(c.id) AS total
            FROM chamados c
            INNER JOIN usuarios u ON c.id_tecnico = u.id
            GROUP BY u.nome
        """

        try:
            cursor.execute(sql)
            resultados = cursor.fetchall()

            print("\n--- CHAMADOS POR TÉCNICO ---")
            if resultados:
                for tecnico, total in resultados:
                    print(f"{tecnico}: {total}")
            else:
                print("Nenhum chamado atribuído a técnico.")
        except Exception as erro:
            print(f"Erro ao consultar chamados por técnico: {erro}")
        finally:
            cursor.close()
            db.desconectar()
