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
        print(f" ID: {usu[0]} | Nome: {usu[1]} ({usu[2].capitalize()})")
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
        entrada_id = input("Digite seu ID: ").strip()
        
        if not entrada_id:
            print("\n[Erro] O ID não pode ficar vazio.")
            mostrar_usuarios_existentes(cursor)
            continue
            
        try:
            id_usuario = int(entrada_id)
        except ValueError:
            print("\n[Erro] Entrada inválida! O ID precisa ser um número.")
            mostrar_usuarios_existentes(cursor)
            continue

        sql = """
        SELECT id_usuario, nome, perfil
        FROM usuarios
        WHERE id_usuario = %s
        """
        cursor.execute(sql, (id_usuario,))
        resultado = cursor.fetchone()

        if resultado is None:
            print(f"\n[Erro] ID {id_usuario} inexistente no sistema!")
            mostrar_usuarios_existentes(cursor)
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
    # --- 1. VALIDAÇÃO DO NOME ---
    while True:
        nome = input("Nome completo: ").strip()
        if len(nome) < 10:
            print("\n[Erro] Nome muito curto!")
            print("Por favor, digite o seu nome completo (mínimo de 10 caracteres).\n")
        elif nome.isdigit():
            print("\n[Erro] O nome não pode conter apenas números.\n")
        else:
            break

    # --- 2. VALIDAÇÃO DO EMAIL ---
    while True:
        email = input("Email: ").strip().lower()
        if not email:
            print("\n[Erro] O campo de e-mail não pode ficar vazio.")
        elif email.isdigit():
            print("\n[Erro] O e-mail não pode conter apenas números. Por favor, digite um e-mail válido.")
        elif not email.endswith("@gmail.com"):
            print("\n[Erro] Domínio inválido!")
            print("Você precisa colocar um e-mail válido. Exemplo: usuario@gmail.com ou ex1@gmail.com\n")
        else:
            break

    # --- 3. VALIDAÇÃO DO PERFIL ---
    while True:
        print("\n===== PERFIL DO USUÁRIO =====")
        print("Digite 1 para Solicitante")
        print("Digite 2 para Operador")
        print("Digite 3 para Técnico")
        
        opcao_perfil = input("\nEscolha o perfil (1-3): ").strip()

        if opcao_perfil == "1":
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

    # --- 4. GRAVAÇÃO NO BANCO DE DADOS ---
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

    # --- 1. MENU DE CATEGORIAS ---
    while True:
        print("\n===== CATEGORIAS =====")
        print("Digite 1 para Computadores")
        print("Digite 2 para Internet e Wi-Fi")
        print("Digite 3 para Impressoras")
        print("Digite 4 para Outros")

        opcao_cat = input("\nEscolha uma categoria: ").strip()

        if opcao_cat == "1":
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

    # --- 2. DESCRIÇÃO ---
    while True:
        descricao = input("\nDescrição do problema: ").strip()
        if not descricao:
            print("\n[Erro] A descrição não pode ficar vazia. Por favor, detalhe o problema ocorrido.")
        elif descricao.isdigit():
            print("\n[Erro] A descrição não pode conter apenas números. Por favor, digite o problema ocorrido por extenso.")
        else:
            break

    # --- 3. URGÊNCIA ---
    while True:
        print("\n===== ESCALA DE URGÊNCIA =====")
        print("1 - Pouco Urgente")
        print("2 - Média Urgência")
        print("3 - Muito Urgente")
        
        entrada_urgencia = input("Digite o nível de urgência (1-3): ").strip()
        try:
            urgencia = int(entrada_urgencia)
            if 1 <= urgencia <= 3:
                break
            else:
                print("\n[Erro] Valor fora da escala! Escolha de 1 a 3.")
        except ValueError:
            print("\n[Erro] Entrada inválida! Digite apenas números de 1 a 3.")

    # --- 4. IMPACTO ---
    while True:
        print("\n===== ESCALA DE IMPACTO =====")
        print("1 - Baixo Impacto (Apenas um usuário)")
        print("2 - Médio Impacto (Um setor afetado)")
        print("3 - Alto Impacto (Empresa inteira parada)")
        
        entrada_impacto = input("Digite o nível de impacto (1-3): ").strip()
        try:
            impacto = int(entrada_impacto)
            if 1 <= impacto <= 3:
                break
            else:
                print("\n[Erro] Valor fora da escala! Escolha de 1 a 3.")
        except ValueError:
            print("\n[Erro] Entrada inválida! Digite apenas números de 1 a 3.")

    # --- 5. CÁLCULO E BANCO DE DADOS ---
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
    cursor.execute(sql, valores)
    conexao.commit()
    
    # Captura o número do chamado gerado automaticamente (AUTO_INCREMENT do banco)
    id_chamado_gerado = cursor.lastrowid
    fechar_conexao(conexao, cursor)

    # --- 6. PAINEL DE CONFIRMAÇÃO DO CHAMADO (Ajustado para Número de Chamado) ---
    print("\n=============================================")
    print("      PAINEL DE SOLICITAÇÃO ABERTA           ")
    print("=============================================")
    print(f" Chamado Nº : {id_chamado_gerado}")  # Mudado para Número do chamado
    print(f" Solicitante: {usuario.get('nome', 'Não informado')}")
    print(f" ID Usuário : {usuario['id']}")
    print(f" Categoria  : {categoria}")
    print(f" Descrição  : {descricao}")
    print(f" Urgência   : {urgencia}")
    print(f" Impacto    : {impacto}")
    print("---------------------------------------------")
    print(f" PRIORIDADE DO CHAMADO: {prioridade}")
    print("=============================================\n")


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
    conexao = conectar()
    if conexao is None:
        return

    cursor = conexao.cursor()

    sql = """
    SELECT s.id_solicitacao, solicitante.nome, IFNULL(tecnico.nome, 'Sem técnico'),
           s.categoria, s.prioridade, s.status, s.data_abertura
    FROM solicitacoes s
    INNER JOIN usuarios solicitante ON s.id_solicitante = solicitante.id_usuario
    LEFT JOIN usuarios tecnico ON s.id_responsavel = tecnico.id_usuario
    """
    cursor.execute(sql)
    resultados = cursor.fetchall()

    print("\n===== TODAS SOLICITAÇÕES =====")
    if not resultados:
        print("Nenhum chamado aberto no sistema.")
        
    for item in resultados:
        print(f"""====================================
Chamado Nº: {item[0]}
Solicitante: {item[1]}
Técnico ID/Nome: {item[2]}
Categoria: {item[3]}
Prioridade: {item[4]}
Status: {item[5]}
Data: {item[6]}
====================================""")

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

    # --- VALIDAÇÃO DO NÚMERO DO CHAMADO ---
    while True:
        listar_solicitacoes()
        entrada_chamado = input("\nDigite o Número do Chamado: ").strip()
        
        if not entrada_chamado:
            print("\n[Erro] O número do chamado não pode ficar vazio.")
            continue
        try:
            id_solicitacao = int(entrada_chamado)
            # Verifica se o chamado existe no banco
            cursor.execute("SELECT id_solicitacao FROM solicitacoes WHERE id_solicitacao = %s", (id_solicitacao,))
            if cursor.fetchone() is None:
                print(f"\n[Erro] Chamado Nº {id_solicitacao} não foi encontrado!")
                continue
            break
        except ValueError:
            print("\n[Erro] Entrada inválida! Digite apenas números para o chamado.")

    # --- VALIDAÇÃO DO ID DO TÉCNICO ---
    while True:
        cursor.execute("SELECT id_usuario, nome FROM usuarios WHERE perfil = 'tecnico'")
        tecnicos = cursor.fetchall()

        print("\n===== TÉCNICOS DISPONÍVEIS =====")
        for tec in tecnicos:
            print(f"ID Técnico: {tec[0]} | Nome: {tec[1]}")
        print("================================")

        entrada_tecnico = input("\nDigite o ID do técnico: ").strip()
        if not entrada_tecnico:
            print("\n[Erro] O ID do técnico não pode ficar vazio.")
            continue
        try:
            id_tecnico = int(entrada_tecnico)
            # Verifica se o técnico de fato existe e é técnico
            cursor.execute("SELECT id_usuario FROM usuarios WHERE id_usuario = %s AND perfil = 'tecnico'", (id_tecnico,))
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
    cursor.execute(sql_update, (id_tecnico, id_solicitacao))
    conexao.commit()

    print(f"\nTécnico atribuído com sucesso ao Chamado Nº {id_solicitacao}!")
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

    # --- VALIDAÇÃO DO NÚMERO DO CHAMADO ---
    while True:
        minhas_solicitacoes(usuario)
        entrada_chamado = input("\nDigite o Número do Chamado: ").strip()
        
        if not entrada_chamado:
            print("\n[Erro] O número do chamado não pode ficar vazio.")
            continue
        try:
            id_solicitacao = int(entrada_chamado)
            
            sql = "SELECT status FROM solicitacoes WHERE id_solicitacao = %s"
            cursor.execute(sql, (id_solicitacao,))
            resultado = cursor.fetchone()

            if resultado is None:
                print(f"\n[Erro] Chamado Nº {id_solicitacao} não encontrado!")
                continue
            
            status_atual = resultado[0]
            if status_atual == "Fechada":
                print(f"\n[Aviso] O Chamado Nº {id_solicitacao} já está finalizado (Fechado).")
                fechar_conexao(conexao, cursor)
                return
            break
        except ValueError:
            print("\n[Erro] Entrada inválida! Digite apenas números.")

    # --- VALIDAÇÃO DO STATUS ---
    while True:
        print("\n===== SELECIONE O NOVO STATUS =====")
        print("1 - Em andamento")
        print("2 - Pendente (Aguardando peça/resposta)")
        print("3 - Fechada (Resolvido)")
        
        opcao_status = input("\nEscolha a opção (1-3): ").strip()
        if opcao_status == "1":
            novo_status = "Em andamento"
            break
        elif opcao_status == "2":
            novo_status = "Pendente"
            break
        elif opcao_status == "3":
            novo_status = "Fechada"
            break
        else:
            print("\n[Opção Inválida] Digite um número de 1 a 3.")

    sql_update = "UPDATE solicitacoes SET status = %s WHERE id_solicitacao = %s"
    cursor.execute(sql_update, (novo_status, id_solicitacao))
    conexao.commit()

    print(f"\nStatus do Chamado Nº {id_solicitacao} atualizado para '{novo_status}'!")
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