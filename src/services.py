from database import conectar, fechar_conexao


# ====================================
# LOGIN
# ====================================

def login():
    id_usuario = int(input("Digite seu ID: "))
    conexao = conectar()

    if conexao is None:
        return None

    cursor = conexao.cursor()

    sql = """
    SELECT id_usuario, nome, perfil
    FROM usuarios
    WHERE id_usuario = %s
    """

    cursor.execute(sql, (id_usuario,))

    resultado = cursor.fetchone()

    fechar_conexao(conexao, cursor)

    if resultado is None:
        return None

    return {
        "id": resultado[0],
        "nome": resultado[1],
        "perfil": resultado[2]
    }


# ====================================
# PRIORIDADE
# ====================================

def calcular_prioridade(urgencia, impacto):
    soma = urgencia + impacto

    if soma <= 2:
        return "Baixa"
    elif soma <= 4:
        return "Média"
    else:
        return "Alta"


# ====================================
# CADASTRAR USUÁRIO
# ====================================

def cadastrar_usuario():
    nome = input("Nome: ")
    email = input("Email: ")
    perfil = input(
        "Perfil (solicitante, operador, tecnico): "
    )

    conexao = conectar()

    if conexao is None:
        return

    cursor = conexao.cursor()

    sql = """
    INSERT INTO usuarios(nome, email, perfil)
    VALUES (%s, %s, %s)
    """

    try:
        cursor.execute(
            sql,
            (nome, email, perfil)
        )

        conexao.commit()

        print("\nUsuário cadastrado!")

    except Exception as erro:

        print(f"\nErro: {erro}")

    fechar_conexao(conexao, cursor)


# ====================================
# ABRIR SOLICITAÇÃO
# ====================================

def abrir_solicitacao(usuario):
    categoria = input("Categoria: ")
    descricao = input("Descrição: ")
    urgencia = int(input("Urgência (1-3): "))
    impacto = int(input("Impacto (1-3): "))

    prioridade = calcular_prioridade(
        urgencia,
        impacto
    )

    conexao = conectar()

    if conexao is None:
        return

    cursor = conexao.cursor()

    sql = """
    INSERT INTO solicitacoes
    (
        id_solicitante,
        categoria,
        descricao,
        fator_urgencia,
        fator_impacto,
        prioridade
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    valores = (
        usuario["id"],
        categoria,
        descricao,
        urgencia,
        impacto,
        prioridade
    )

    cursor.execute(sql, valores)

    conexao.commit()

    print(
        f"\nSolicitação aberta com prioridade {prioridade}"
    )

    fechar_conexao(conexao, cursor)


# ====================================
# MINHAS SOLICITAÇÕES
# ====================================

def minhas_solicitacoes(usuario):
    conexao = conectar()

    if conexao is None:
        return

    cursor = conexao.cursor()

    if usuario["perfil"] == "solicitante":

        sql = """
        SELECT
            id_solicitacao,
            categoria,
            prioridade,
            status
        FROM solicitacoes
        WHERE id_solicitante = %s
        """

        cursor.execute(sql, (usuario["id"],))

    elif usuario["perfil"] == "tecnico":

        sql = """
        SELECT
            id_solicitacao,
            categoria,
            prioridade,
            status
        FROM solicitacoes
        WHERE id_responsavel = %s
        """

        cursor.execute(sql, (usuario["id"],))

    resultados = cursor.fetchall()

    print("\n===== SOLICITAÇÕES =====")

    for item in resultados:

        print(f"""
=========================
ID: {item[0]}
Categoria: {item[1]}
Prioridade: {item[2]}
Status: {item[3]}
=========================
""")

    fechar_conexao(conexao, cursor)


# ====================================
# LISTAR SOLICITAÇÕES
# ====================================

def listar_solicitacoes():
    conexao = conectar()

    if conexao is None:
        return

    cursor = conexao.cursor()

    sql = """
    SELECT
        s.id_solicitacao,

        solicitante.nome AS solicitante,

        IFNULL(
            tecnico.nome,
            'Sem técnico'
        ) AS tecnico_responsavel,

        s.categoria,

        s.prioridade,

        s.status,

        s.data_abertura

    FROM solicitacoes s

    INNER JOIN usuarios solicitante
    ON s.id_solicitante = solicitante.id_usuario

    LEFT JOIN usuarios tecnico
    ON s.id_responsavel = tecnico.id_usuario
    """

    cursor.execute(sql)

    resultados = cursor.fetchall()

    print("\n===== TODAS SOLICITAÇÕES =====")

    for item in resultados:

        print(f"""
====================================
ID: {item[0]}
Solicitante: {item[1]}
Técnico: {item[2]}
Categoria: {item[3]}
Prioridade: {item[4]}
Status: {item[5]}
Data: {item[6]}
====================================
""")

    fechar_conexao(conexao, cursor)


# ====================================
# ATRIBUIR TÉCNICO
# ====================================

def atribuir_tecnico(usuario):
    if usuario["perfil"] != "operador":
        print(
            "\nApenas operadores podem atribuir técnicos"
        )

        return

    listar_solicitacoes()

    id_solicitacao = int(
        input("\nID da solicitação: ")
    )

    conexao = conectar()

    if conexao is None:
        return

    cursor = conexao.cursor()

    sql = """
    SELECT id_usuario, nome
    FROM usuarios
    WHERE perfil = 'tecnico'
    """

    cursor.execute(sql)

    tecnicos = cursor.fetchall()

    print("\n===== TÉCNICOS =====")

    for tecnico in tecnicos:

        print(f"""
=========================
ID: {tecnico[0]}
Nome: {tecnico[1]}
=========================
""")

    id_tecnico = int(
        input("\nID do técnico: ")
    )

    sql_update = """
    UPDATE solicitacoes
    SET id_responsavel = %s,
        status = 'Em andamento'
    WHERE id_solicitacao = %s
    """

    cursor.execute(
        sql_update,
        (id_tecnico, id_solicitacao)
    )

    conexao.commit()

    print("\nTécnico atribuído!")

    fechar_conexao(conexao, cursor)


# ====================================
# ATUALIZAR STATUS
# ====================================

def atualizar_status(usuario):
    if usuario["perfil"] != "tecnico":
        print(
            "\nApenas técnicos podem alterar status"
        )

        return

    minhas_solicitacoes(usuario)

    id_solicitacao = int(
        input("\nID da solicitação: ")
    )

    novo_status = input(
        "Novo status: "
    )

    conexao = conectar()

    if conexao is None:
        return

    cursor = conexao.cursor()

    sql = """
    SELECT status
    FROM solicitacoes
    WHERE id_solicitacao = %s
    """

    cursor.execute(sql, (id_solicitacao,))

    resultado = cursor.fetchone()

    if resultado is None:
        print("\nSolicitação não encontrada")

        return

    status_atual = resultado[0]

    if status_atual == "Fechada":
        print(
            "\nSolicitação já está fechada"
        )

        return

    sql_update = """
    UPDATE solicitacoes
    SET status = %s
    WHERE id_solicitacao = %s
    """

    cursor.execute(
        sql_update,
        (novo_status, id_solicitacao)
    )

    conexao.commit()

    print("\nStatus atualizado!")

    fechar_conexao(conexao, cursor)


# ====================================
# ESTATÍSTICAS
# ====================================

def estatisticas():
    conexao = conectar()

    if conexao is None:
        return

    cursor = conexao.cursor()

    print("\n===== POR STATUS =====")

    sql = """
    SELECT status, COUNT(*)
    FROM solicitacoes
    GROUP BY status
    """

    cursor.execute(sql)

    for item in cursor.fetchall():

        print(f"""
Status: {item[0]}
Quantidade: {item[1]}
""")

    print("\n===== POR PRIORIDADE =====")

    sql2 = """
    SELECT prioridade, COUNT(*)
    FROM solicitacoes
    GROUP BY prioridade
    """

    cursor.execute(sql2)

    for item in cursor.fetchall():

        print(f"""
Prioridade: {item[0]}
Quantidade: {item[1]}
""")

    fechar_conexao(conexao, cursor)
