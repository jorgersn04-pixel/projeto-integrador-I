from database import conectar, fechar_conexao


# ====================================
# FUNÇÃO AUXILIAR: BUSCAR E EXIBIR USUÁRIOS EXISTENTES
# ====================================
def mostrar_usuarios_existentes(cursor):
    """Busca e exibe de forma organizada os usuários cadastrados no banco."""
    cursor.execute("SELECT id_usuario, nome, perfil FROM usuarios")
    usuarios = cursor.fetchall()

    print("\n===== USUÁRIOS EXISTENTES NO SISTEMA =====")

    if not usuarios:
        print("Nenhum usuário cadastrado no sistema.")

    for usu in usuarios:
        print(f" ID: {usu[0]} | Nome: {usu[1]} |")

    print("==========================================")


# ====================================
# LOGIN
# ====================================
def login():
    conexao = conectar()

    if conexao is None:
        print("\n[Erro] Falha ao conectar ao banco de dados.")
        return None

    cursor = conexao.cursor()

    while True:
        mostrar_usuarios_existentes(cursor)

        entrada_id = input("\nDigite seu ID: ").strip()

        

        if not entrada_id:
            print("\n[Erro] O ID não pode ficar vazio.")
            continue

        try:
            id_usuario = int(entrada_id)
        except ValueError:
            print("\n[Erro] Entrada inválida! O ID precisa ser um número.")
            continue

        cursor.execute("""
            SELECT id_usuario, nome, perfil
            FROM usuarios
            WHERE id_usuario = %s
        """, (id_usuario,))

        resultado = cursor.fetchone()

        if resultado is None:
            print(f"\n[Erro] ID {id_usuario} inexistente no sistema!")
        else:
            fechar_conexao(conexao, cursor)
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
    while True:
        nome = input("Nome completo (0 para voltar): ").strip()

        if nome == "0":
            return

        if len(nome) < 10:
            print("\n[Erro] Nome muito curto!")
            print("Por favor, digite o seu nome completo (mínimo de 10 caracteres).\n")
        elif nome.isdigit():
            print("\n[Erro] O nome não pode conter apenas números.\n")
        else:
            break

    while True:
        email = input("Email (0 para voltar): ").strip().lower()

        if email == "0":
            return

        dominios_permitidos = (
            "@gmail.com",
            "@outlook.com",
            "@hotmail.com",
            "@live.com",
            "@icloud.com",
            "@yahoo.com"
        )

        if not email:
            print("\n[Erro] O campo de e-mail não pode ficar vazio.")

        elif email.isdigit():
            print("\n[Erro] O e-mail não pode conter apenas números.")

        elif "@" not in email or "." not in email:
            print("\n[Erro] E-mail inválido!")
            print("Digite um e-mail válido. Exemplo: usuario@gmail.com\n")

        elif not email.endswith(dominios_permitidos):
            print("\n[Erro] Domínio inválido!")
            print("Domínios aceitos:")
            print("- Gmail")
            print("- Outlook")
            print("- Hotmail")
            print("- Live")
            print("- iCloud")
            print("- Yahoo\n")

        else:
            break

    while True:
        print("\n===== PERFIL DO USUÁRIO =====")
        print("Digite 1 para Solicitante")
        print("Digite 2 para Operador")
        print("Digite 3 para Técnico")
        print("Digite 0 para Voltar")

        opcao_perfil = input("\nEscolha o perfil (1-3): ").strip()

        if opcao_perfil == "0":
            return
        elif opcao_perfil == "1":
            perfil = "solicitante"
            print(f"-> Perfil selecionado: 1 - {perfil}")
            break
        elif opcao_perfil == "2":
            perfil = "operador"
            print(f"-> Perfil selecionado: 2 - {perfil}")
            break
        elif opcao_perfil == "3":
            perfil = "tecnico"
            print(f"-> Perfil selecionado: 3 - {perfil}")
            break
        else:
            print("\n[Perfil Inválido!]")
            print("Por favor, digite novamente um perfil válido: 1 para Solicitante, 2 para Operador ou 3 para Técnico.")

    conexao = conectar()

    if conexao is None:
        print("\n[Erro] Não foi possível conectar ao banco de dados.")
        return

    cursor = conexao.cursor()

    sql = """
    INSERT INTO usuarios(nome, email, perfil)
    VALUES (%s, %s, %s)
    """

    try:
        cursor.execute(sql, (nome, email, perfil))
        conexao.commit()

        print("\n=============================================")
        print("        USUÁRIO CADASTRADO COM SUCESSO!      ")
        print("=============================================")
        print(f" Nome   : {nome}")
        print(f" Email  : {email}")
        print(f" Perfil : {perfil.capitalize()}")
        print("=============================================\n")

    except Exception as erro:
        print(f"\n[Erro ao salvar no banco]: {erro}")

    finally:
        fechar_conexao(conexao, cursor)


# ====================================
# ABRIR SOLICITAÇÃO
# ====================================
def abrir_solicitacao(usuario):
    if not usuario or "id" not in usuario or usuario["id"] is None:
        print("\n[Erro Crítico] Usuário não identificado ou ID ausente!")
        return

    while True:
        print("\n===== CATEGORIAS =====")
        print("Digite 1 para Computadores")
        print("Digite 2 para Internet e Wi-Fi")
        print("Digite 3 para Impressoras")
        print("Digite 4 para Outros")
        print("Digite 0 para Voltar")

        opcao_cat = input("\nEscolha uma categoria: ").strip()

        if opcao_cat == "0":
            return
        elif opcao_cat == "1":
            categoria = "Computadores"
            print(f"\n-> Categoria selecionada: 1 - {categoria}")
            break
        elif opcao_cat == "2":
            categoria = "Internet e Wi-Fi"
            print(f"\n-> Categoria selecionada: 2 - {categoria}")
            break
        elif opcao_cat == "3":
            categoria = "Impressoras"
            print(f"\n-> Categoria selecionada: 3 - {categoria}")
            break
        elif opcao_cat == "4":
            categoria = "Outros"
            print(f"\n-> Categoria selecionada: 4 - {categoria}")
            break
        else:
            print("\n[Categoria inválida!]")
            print("Por favor, digite uma categoria válida (de 1 a 4).\n")

    while True:
        descricao = input("\nDescrição do problema (0 para voltar): ").strip()

        if descricao == "0":
            return

        if not descricao:
            print("\n[Erro] A descrição não pode ficar vazia. Por favor, detalhe o problema ocorrido.")
        elif descricao.isdigit():
            print("\n[Erro] A descrição não pode conter apenas números. Por favor, digite o problema ocorrido por extenso.")
        else:
            break

    while True:
        print("\n===== ESCALA DE URGÊNCIA =====")
        print("1 - Pouco Urgente")
        print("2 - Média Urgência")
        print("3 - Muito Urgente")
        print("0 - Voltar")

        entrada_urgencia = input("Digite o nível de urgência (1-3): ").strip()

        if entrada_urgencia == "0":
            return

        try:
            urgencia = int(entrada_urgencia)

            if 1 <= urgencia <= 3:
                break
            else:
                print("\n[Erro] Valor fora da escala! Escolha de 1 a 3.")

        except ValueError:
            print("\n[Erro] Entrada inválida! Digite apenas números de 1 a 3.")

    while True:
        print("\n===== ESCALA DE IMPACTO =====")
        print("1 - Baixo Impacto (Apenas um usuário)")
        print("2 - Médio Impacto (Um setor afetado)")
        print("3 - Alto Impacto (Empresa inteira parada)")
        print("0 - Voltar")

        entrada_impacto = input("Digite o nível de impacto (1-3): ").strip()

        if entrada_impacto == "0":
            return

        try:
            impacto = int(entrada_impacto)

            if 1 <= impacto <= 3:
                break
            else:
                print("\n[Erro] Valor fora da escala! Escolha de 1 a 3.")

        except ValueError:
            print("\n[Erro] Entrada inválida! Digite apenas números de 1 a 3.")

    prioridade = calcular_prioridade(urgencia, impacto)

    conexao = conectar()

    if conexao is None:
        return

    cursor = conexao.cursor()

    sql = """
    INSERT INTO solicitacoes
    (id_solicitante, categoria, descricao, fator_urgencia, fator_impacto, prioridade)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    valores = (usuario["id"], categoria, descricao, urgencia, impacto, prioridade)

    try:
        cursor.execute(sql, valores)
        conexao.commit()

        id_chamado_gerado = cursor.lastrowid

        print("\n=============================================")
        print("      PAINEL DE SOLICITAÇÃO ABERTA           ")
        print("=============================================")
        print(f" Chamado Nº : {id_chamado_gerado}")
        print(f" Solicitante: {usuario.get('nome', 'Não informado')}")
        print(f" ID Usuário : {usuario['id']}")
        print(f" Categoria  : {categoria}")
        print(f" Descrição  : {descricao}")
        print(f" Urgência   : {urgencia}")
        print(f" Impacto    : {impacto}")
        print("---------------------------------------------")
        print(f" PRIORIDADE DO CHAMADO: {prioridade}")
        print("=============================================\n")

    except Exception as erro:
        print(f"\n[Erro ao abrir solicitação]: {erro}")

    finally:
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
        SELECT id_solicitacao, categoria, prioridade, status
        FROM solicitacoes
        WHERE id_solicitante = %s
        """
        cursor.execute(sql, (usuario["id"],))

    elif usuario["perfil"] == "tecnico":
        sql = """
        SELECT id_solicitacao, categoria, prioridade, status
        FROM solicitacoes
        WHERE id_responsavel = %s
        """
        cursor.execute(sql, (usuario["id"],))

    else:
        print("\n[Erro] Perfil inválido para consulta.")
        fechar_conexao(conexao, cursor)
        return

    resultados = cursor.fetchall()

    print("\n===== SUAS SOLICITAÇÕES =====")

    if not resultados:
        print("Nenhuma solicitação encontrada.")

    for item in resultados:
        print(f"""=========================
Chamado Nº: {item[0]}
Categoria: {item[1]}
Prioridade: {item[2]}
Status: {item[3]}
=========================""")

    fechar_conexao(conexao, cursor)


# ====================================
# LISTAR SOLICITAÇÕES
# ====================================
def listar_solicitacoes():
    while True:
        print("\n===== CONSULTAS E LISTAGENS =====")
        print("1 - Listar todas as solicitações")
        print("2 - Listar por status")
        print("3 - Listar por prioridade")
        print("4 - Listar solicitações de um usuário")
        print("0 - Voltar")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            listar_todas_solicitacoes()

        elif opcao == "2":
            listar_por_status()

        elif opcao == "3":
            listar_por_prioridade()

        elif opcao == "4":
            listar_por_usuario()

        elif opcao == "0":
            return

        else:
            print("\n[Erro] Opção inválida.")

def exibir_solicitacoes(resultados):
    if not resultados:
        print("\nNenhuma solicitação encontrada.")
        return

    for item in resultados:
        print(f"""====================================
Chamado Nº: {item[0]}
Solicitante: {item[1]}
Categoria/Tipo: {item[2]}
Prioridade: {item[3]}
Status: {item[4]}
Data: {item[5]}
====================================""")


def listar_todas_solicitacoes():
    conexao = conectar()

    if conexao is None:
        return

    cursor = conexao.cursor()

    sql = """
    SELECT s.id_solicitacao, solicitante.nome,
           s.categoria, s.prioridade, s.status, s.data_abertura
    FROM solicitacoes s
    INNER JOIN usuarios solicitante
        ON s.id_solicitante = solicitante.id_usuario
    ORDER BY
        FIELD(s.status, 'Aberta', 'Em andamento', 'Em Andamento', 'Fechada'),
        FIELD(s.prioridade, 'Alta', 'Média', 'Baixa'),
        s.data_abertura DESC
    """

    cursor.execute(sql)
    resultados = cursor.fetchall()

    print("\n===== TODAS AS SOLICITAÇÕES =====")
    print("Ordenação: status, prioridade e data de abertura.")
    print("Justificativa: chamados abertos e mais críticos aparecem primeiro.")

    exibir_solicitacoes(resultados)

    fechar_conexao(conexao, cursor)


def listar_por_status():
    while True:
        print("\n===== FILTRAR POR STATUS =====")
        print("1 - Aberta")
        print("2 - Em andamento")
        print("3 - Fechada")
        print("0 - Voltar")

        opcao = input("\nEscolha o status: ").strip()

        if opcao == "0":
            return
        elif opcao == "1":
            status = "Aberta"
            break
        elif opcao == "2":
            status = "Em Andamento"
            break
        elif opcao == "3":
            status = "Fechada"
            break
        else:
            print("\n[Erro] Opção inválida.")

    conexao = conectar()

    if conexao is None:
        return

    cursor = conexao.cursor()

    sql = """
    SELECT s.id_solicitacao, solicitante.nome,
           s.categoria, s.prioridade, s.status, s.data_abertura
    FROM solicitacoes s
    INNER JOIN usuarios solicitante
        ON s.id_solicitante = solicitante.id_usuario
    WHERE s.status = %s
    ORDER BY
        FIELD(s.prioridade, 'Alta', 'Média', 'Baixa'),
        s.data_abertura DESC
    """

    cursor.execute(sql, (status,))
    resultados = cursor.fetchall()

    print(f"\n===== SOLICITAÇÕES COM STATUS: {status} =====")
    exibir_solicitacoes(resultados)

    fechar_conexao(conexao, cursor)


def listar_por_prioridade():
    while True:
        print("\n===== FILTRAR POR PRIORIDADE =====")
        print("1 - Alta")
        print("2 - Média")
        print("3 - Baixa")
        print("0 - Voltar")

        opcao = input("\nEscolha a prioridade: ").strip()

        if opcao == "0":
            return
        elif opcao == "1":
            prioridade = "Alta"
            break
        elif opcao == "2":
            prioridade = "Média"
            break
        elif opcao == "3":
            prioridade = "Baixa"
            break
        else:
            print("\n[Erro] Opção inválida.")

    conexao = conectar()

    if conexao is None:
        return

    cursor = conexao.cursor()

    sql = """
    SELECT s.id_solicitacao, solicitante.nome,
           s.categoria, s.prioridade, s.status, s.data_abertura
    FROM solicitacoes s
    INNER JOIN usuarios solicitante
        ON s.id_solicitante = solicitante.id_usuario
    WHERE s.prioridade = %s
    ORDER BY
        FIELD(s.status, 'Aberta', 'Em andamento', 'Em Andamento', 'Fechada'),
        s.data_abertura DESC
    """

    cursor.execute(sql, (prioridade,))
    resultados = cursor.fetchall()

    print(f"\n===== SOLICITAÇÕES COM PRIORIDADE: {prioridade} =====")
    exibir_solicitacoes(resultados)

    fechar_conexao(conexao, cursor)


def listar_por_usuario():
    conexao = conectar()

    if conexao is None:
        return

    cursor = conexao.cursor()

    while True:
        mostrar_usuarios_existentes(cursor)

        entrada = input("\nDigite o ID do usuário (0 para voltar): ").strip()

        if entrada == "0":
            fechar_conexao(conexao, cursor)
            return

        if not entrada:
            print("\n[Erro] O ID do usuário não pode ficar vazio.")
            continue

        try:
            id_usuario = int(entrada)

            cursor.execute(
                "SELECT id_usuario, nome FROM usuarios WHERE id_usuario = %s",
                (id_usuario,)
            )

            usuario = cursor.fetchone()

            if usuario is None:
                print(f"\n[Erro] Usuário ID {id_usuario} não encontrado.")
                continue

            break

        except ValueError:
            print("\n[Erro] Digite apenas números.")

    sql = """
    SELECT s.id_solicitacao, solicitante.nome,
           s.categoria, s.prioridade, s.status, s.data_abertura
    FROM solicitacoes s
    INNER JOIN usuarios solicitante
        ON s.id_solicitante = solicitante.id_usuario
    WHERE s.id_solicitante = %s
    ORDER BY
        FIELD(s.status, 'Aberta', 'Em andamento', 'Em Andamento', 'Fechada'),
        FIELD(s.prioridade, 'Alta', 'Média', 'Baixa'),
        s.data_abertura DESC
    """

    cursor.execute(sql, (id_usuario,))
    resultados = cursor.fetchall()

    print(f"\n===== SOLICITAÇÕES DO USUÁRIO: {usuario[1]} =====")
    exibir_solicitacoes(resultados)

    fechar_conexao(conexao, cursor)

# ====================================
# ATRIBUIR TÉCNICO
# ====================================
def atribuir_tecnico(usuario):
    if usuario["perfil"] != "operador":
        print("\nApenas operadores podem atribuir técnicos.")
        return

    conexao = conectar()

    if conexao is None:
        return

    cursor = conexao.cursor()

    while True:
        listar_todas_solicitacoes()

        entrada_chamado = input("\nDigite o Número do Chamado (0 para voltar): ").strip()

        if entrada_chamado == "0":
            fechar_conexao(conexao, cursor)
            return

        if not entrada_chamado:
            print("\n[Erro] O número do chamado não pode ficar vazio.")
            continue

        try:
            id_solicitacao = int(entrada_chamado)

            cursor.execute(
                "SELECT id_solicitacao FROM solicitacoes WHERE id_solicitacao = %s",
                (id_solicitacao,)
            )

            if cursor.fetchone() is None:
                print(f"\n[Erro] Chamado Nº {id_solicitacao} não foi encontrado!")
                continue

            break

        except ValueError:
            print("\n[Erro] Entrada inválida! Digite apenas números para o chamado.")

    while True:
        cursor.execute("SELECT id_usuario, nome FROM usuarios WHERE perfil = 'tecnico'")
        tecnicos = cursor.fetchall()

        print("\n===== TÉCNICOS DISPONÍVEIS =====")

        if not tecnicos:
            print("Nenhum técnico cadastrado no sistema.")
            fechar_conexao(conexao, cursor)
            return

        for tec in tecnicos:
            print(f"ID Técnico: {tec[0]} | Nome: {tec[1]}")

        print("================================")
        print("Digite 0 para Voltar")

        entrada_tecnico = input("\nDigite o ID do técnico: ").strip()

        if entrada_tecnico == "0":
            fechar_conexao(conexao, cursor)
            return

        if not entrada_tecnico:
            print("\n[Erro] O ID do técnico não pode ficar vazio.")
            continue

        try:
            id_tecnico = int(entrada_tecnico)

            cursor.execute(
                "SELECT id_usuario FROM usuarios WHERE id_usuario = %s AND perfil = 'tecnico'",
                (id_tecnico,)
            )

            if cursor.fetchone() is None:
                print(f"\n[Erro] Técnico com ID {id_tecnico} não cadastrado ou inválido!")
                continue

            break

        except ValueError:
            print("\n[Erro] Entrada inválida! Digite apenas números para o ID do técnico.")

    sql_update = """
    UPDATE solicitacoes
    SET id_responsavel = %s, status = 'Em andamento'
    WHERE id_solicitacao = %s
    """

    try:
        cursor.execute(sql_update, (id_tecnico, id_solicitacao))
        conexao.commit()

        print(f"\nTécnico atribuído com sucesso ao Chamado Nº {id_solicitacao}!")

    except Exception as erro:
        print(f"\n[Erro ao atribuir técnico]: {erro}")

    finally:
        fechar_conexao(conexao, cursor)
# ====================================
# ATUALIZAR STATUS
# ====================================
def atualizar_status(usuario):
    if usuario["perfil"] != "tecnico":
        print("\nApenas técnicos podem alterar status.")
        return

    conexao = conectar()

    if conexao is None:
        return

    cursor = conexao.cursor()

    while True:
        minhas_solicitacoes(usuario)

        entrada_chamado = input("\nDigite o Número do Chamado (0 para voltar): ").strip()

        if entrada_chamado == "0":
            fechar_conexao(conexao, cursor)
            return

        if not entrada_chamado:
            print("\n[Erro] O número do chamado não pode ficar vazio.")
            continue

        try:
            id_solicitacao = int(entrada_chamado)

            sql = """
            SELECT status
            FROM solicitacoes
            WHERE id_solicitacao = %s
            AND id_responsavel = %s
            """

            cursor.execute(sql, (id_solicitacao, usuario["id"]))
            resultado = cursor.fetchone()

            if resultado is None:
                print(f"\n[Erro] Chamado Nº {id_solicitacao} não encontrado para este técnico!")
                continue

            status_atual = resultado[0]

            if status_atual == "Fechada":
                print(f"\n[Aviso] O Chamado Nº {id_solicitacao} já está finalizado (Fechado).")
                fechar_conexao(conexao, cursor)
                return

            break

        except ValueError:
            print("\n[Erro] Entrada inválida! Digite apenas números.")

    while True:
        print("\n===== SELECIONE O NOVO STATUS =====")
        print("1 - Aberta")
        print("2 - Em andamento (Aguardando peça/resposta)")
        print("3 - Fechada (Resolvido)")
        print("0 - Voltar")

        opcao_status = input("\nEscolha a opção (1-3): ").strip()

        if opcao_status == "0":
            fechar_conexao(conexao, cursor)
            return
        elif opcao_status == "1":
            novo_status = "Aberta"
            break
        elif opcao_status == "2":
            novo_status = "Em Andamento"
            break
        elif opcao_status == "3":
            novo_status = "Fechada"
            break
        else:
            print("\n[Opção Inválida] Digite um número de 1 a 3.")

    sql_update = """
    UPDATE solicitacoes
    SET status = %s
    WHERE id_solicitacao = %s
    AND id_responsavel = %s
    """

    try:
        cursor.execute(sql_update, (novo_status, id_solicitacao, usuario["id"]))
        conexao.commit()

        print(f"\nStatus do Chamado Nº {id_solicitacao} atualizado para '{novo_status}'!")

    except Exception as erro:
        print(f"\n[Erro ao atualizar status]: {erro}")

    finally:
        fechar_conexao(conexao, cursor)


# ====================================
# ESTATÍSTICAS
# ====================================
def estatisticas():
    conexao = conectar()

    if conexao is None:
        return

    cursor = conexao.cursor()

    print("\n===== QUANTIDADE DE CHAMADOS POR STATUS =====")

    sql = "SELECT status, COUNT(*) FROM solicitacoes GROUP BY status"
    cursor.execute(sql)
    resultados_status = cursor.fetchall()

    if not resultados_status:
        print("Nenhum registro encontrado.")

    for item in resultados_status:
        print(f"Status: {item[0]} -> Quantidade: {item[1]}")

    print("\n===== QUANTIDADE DE CHAMADOS POR PRIORIDADE =====")

    sql2 = "SELECT prioridade, COUNT(*) FROM solicitacoes GROUP BY prioridade"
    cursor.execute(sql2)
    resultados_prioridade = cursor.fetchall()

    if not resultados_prioridade:
        print("Nenhum registro encontrado.")

    for item in resultados_prioridade:
        print(f"Prioridade: {item[0]} -> Quantidade: {item[1]}")

    fechar_conexao(conexao, cursor)

# ====================================
# DELETAR SOLICITAÇÃO
# ====================================

def deletar_solicitacao():
    conexao = conectar()

    if conexao is None:
        return

    cursor = conexao.cursor()

    while True:
        listar_todas_solicitacoes()

        entrada = input("\nDigite o número do chamado que deseja deletar (0 para voltar): ").strip()

        if entrada == "0":
            fechar_conexao(conexao, cursor)
            return

        if not entrada:
            print("\n[Erro] O número do chamado não pode ficar vazio.")
            continue

        try:
            id_solicitacao = int(entrada)

            cursor.execute(
                "SELECT id_solicitacao FROM solicitacoes WHERE id_solicitacao = %s",
                (id_solicitacao,)
            )

            if cursor.fetchone() is None:
                print(f"\n[Erro] Chamado Nº {id_solicitacao} não encontrado.")
                continue

            confirmacao = input(
                f"Tem certeza que deseja deletar o chamado Nº {id_solicitacao}? (s/n): "
            ).strip().lower()

            if confirmacao != "s":
                print("\nOperação cancelada.")
                fechar_conexao(conexao, cursor)
                return

            cursor.execute(
                "DELETE FROM solicitacoes WHERE id_solicitacao = %s",
                (id_solicitacao,)
            )

            conexao.commit()

            print(f"\nChamado Nº {id_solicitacao} deletado com sucesso!")
            break

        except ValueError:
            print("\n[Erro] Digite apenas números.")

        except Exception as erro:
            print(f"\n[Erro ao deletar chamado]: {erro}")
            break

    fechar_conexao(conexao, cursor)
# ====================================
# DELETAR USUÁRIO
# ====================================
def deletar_usuario():
    conexao = conectar()

    if conexao is None:
        return

    cursor = conexao.cursor()

    while True:
        mostrar_usuarios_existentes(cursor)

        entrada = input("\nDigite o ID do usuário que deseja deletar (0 para voltar): ").strip()

        if entrada == "0":
            fechar_conexao(conexao, cursor)
            return

        if not entrada:
            print("\n[Erro] O ID do usuário não pode ficar vazio.")
            continue

        try:
            id_usuario = int(entrada)

            cursor.execute(
                "SELECT id_usuario, nome, perfil FROM usuarios WHERE id_usuario = %s",
                (id_usuario,)
            )

            usuario = cursor.fetchone()

            if usuario is None:
                print(f"\n[Erro] Usuário ID {id_usuario} não encontrado.")
                continue

            print("\nUsuário encontrado:")
            print(f"ID: {usuario[0]}")
            print(f"Nome: {usuario[1]}")
            print(f"Perfil: {usuario[2]}")

            confirmacao = input(f"\nTem certeza que deseja deletar o usuário {usuario[1]}? (s/n): ").strip().lower()

            if confirmacao != "s":
                print("\nOperação cancelada.")
                fechar_conexao(conexao, cursor)
                return

            cursor.execute(
                "UPDATE solicitacoes SET id_responsavel = NULL, status = 'Aberta' WHERE id_responsavel = %s",
                (id_usuario,)
            )

            cursor.execute(
                "DELETE FROM solicitacoes WHERE id_solicitante = %s",
                (id_usuario,)
            )

            cursor.execute(
                "DELETE FROM usuarios WHERE id_usuario = %s",
                (id_usuario,)
            )

            conexao.commit()

            print(f"\nUsuário ID {id_usuario} deletado com sucesso!")
            break

        except ValueError:
            print("\n[Erro] Digite apenas números.")

        except Exception as erro:
            print(f"\n[Erro ao deletar usuário]: {erro}")
            break

    fechar_conexao(conexao, cursor)
