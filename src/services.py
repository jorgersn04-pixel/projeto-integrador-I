# ==============================================================================
# Projeto Integrador 1 - 1º Ano | Sistemas de Informação
# Autor: Jorge Rodrigues dos Santos Neto
# Arquivo: services.py - Regras de Negócio, Perfis e CRUD
# ==============================================================================

from database import conectar, fechar_conexao
import mysql.connector

def verificar_perfil(id_usuario):
    """Verifica o papel do usuário (solicitante, operador, tecnico) no banco."""
    conexao = conectar()
    if not conexao: return None
    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute("SELECT perfil FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        usuario = cursor.fetchone()
        return usuario['perfil'] if usuario else None
    except Exception:
        return None
    finally:
        fechar_conexao(conexao, cursor)

def cadastrar_usuario(nome, email, perfil):
    conexao = conectar()
    if not conexao: return False
    cursor = conexao.cursor()
    try:
        sql = "INSERT INTO usuarios (nome, email, perfil) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nome, email, perfil))
        conexao.commit()
        print(f"\n Sucesso: Usuário '{nome}' cadastrado com ID {cursor.lastrowid}.")
        return True
    except mysql.connector.IntegrityError:
        print(f"\n Erro de Integridade: O e-mail '{email}' já está em uso!")
        return False
    finally:
        fechar_conexao(conexao, cursor)

def listar_usuarios():
    conexao = conectar()
    if not conexao: return []
    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_usuario, nome, perfil FROM usuarios")
        return cursor.fetchall()
    finally:
        fechar_conexao(conexao, cursor)

def calcular_prioridade(urgencia, impacto):
    pontuacao = urgencia + impacto
    if pontuacao >= 5: return 'Alta'
    elif pontuacao >= 3: return 'Média'
    else: return 'Baixa'

def abrir_chamado(id_solicitante, categoria, descricao, urgencia, impacto):
    conexao = conectar()
    if not conexao: return False
    cursor = conexao.cursor()
    prioridade = calcular_prioridade(urgencia, impacto)
    try:
        sql = """
            INSERT INTO solicitacoes 
            (id_solicitante, categoria, descricao, fator_urgencia, fator_impacto, prioridade) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (id_solicitante, categoria, descricao, urgencia, impacto, prioridade))
        conexao.commit()
        print(f"\n Chamado #{cursor.lastrowid} aberto com sucesso! Prioridade gerada: {prioridade}")
        return True
    finally:
        fechar_conexao(conexao, cursor)

def atribuir_chamado(id_chamado, id_tecnico):
    """Atualiza o chamado com o Técnico escolhido pelo Operador."""
    conexao = conectar()
    if not conexao: return False
    cursor = conexao.cursor()
    try:
        cursor.execute("UPDATE solicitacoes SET id_tecnico = %s, status = 'Em andamento' WHERE id_solicitacao = %s", (id_tecnico, id_chamado))
        conexao.commit()
        print(f"\n Sucesso: Chamado #{id_chamado} encaminhado para o Técnico ID {id_tecnico}.")
        return True
    except Exception as e:
        print(f"\n Erro ao atribuir chamado: {e}")
        return False
    finally:
        fechar_conexao(conexao, cursor)

def listar_chamados():
    conexao = conectar()
    if not conexao: return []
    cursor = conexao.cursor(dictionary=True)
    try:
        sql = """
            SELECT s.id_solicitacao, u.nome AS solicitante, t.nome AS tecnico, s.categoria, s.prioridade, s.status 
            FROM solicitacoes s
            JOIN usuarios u ON s.id_solicitante = u.id_usuario
            LEFT JOIN usuarios t ON s.id_tecnico = t.id_usuario
            ORDER BY FIELD(s.status, 'Aberta', 'Em andamento', 'Fechada'), s.id_solicitacao DESC
        """
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        fechar_conexao(conexao, cursor)

def atualizar_status(id_chamado, novo_status):
    conexao = conectar()
    if not conexao: return False
    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute("SELECT status FROM solicitacoes WHERE id_solicitacao = %s", (id_chamado,))
        chamado = cursor.fetchone()
        
        if not chamado:
            print("\n Erro: Chamado não encontrado.")
            return False
            
        if chamado['status'] == 'Fechada':
            print("\n Bloqueio de Segurança: Não é permitido alterar um chamado já encerrado.")
            return False

        cursor.execute("UPDATE solicitacoes SET status = %s WHERE id_solicitacao = %s", (novo_status, id_chamado))
        conexao.commit()
        print(f"\n Status do chamado #{id_chamado} atualizado para '{novo_status}'.")
        return True
    finally:
        fechar_conexao(conexao, cursor)
