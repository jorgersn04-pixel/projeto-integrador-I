import services
import os
import re

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\n[Pressione ENTER para retornar ao menu principal]...")

def ler_nome(mensagem):
    padrao_nome = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$'
    while True:
        nome = input(mensagem).strip()
        if len(nome) >= 3 and re.match(padrao_nome, nome):
            return nome.title()
        print(" Inválido! O nome deve conter APENAS letras e ter no mínimo 3 caracteres.")

def ler_email(mensagem):
    padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    while True:
        email = input(mensagem).strip().lower()
        if re.match(padrao, email): return email
        print(" E-mail Inválido! Formato esperado: nome@empresa.com")

def ler_inteiro(mensagem, min_val=None, max_val=None):
    while True:
        try:
            valor = int(input(mensagem).strip())
            if (min_val is not None and valor < min_val) or (max_val is not None and valor > max_val):
                print(f" Valor fora do limite ({min_val} a {max_val}).")
                continue
            return valor
        except ValueError:
            print(" Entrada inválida! Digite APENAS números.")

def ler_texto_livre(mensagem, min_chars=5):
    while True:
        texto = input(mensagem).strip()
        if len(texto) >= min_chars: return texto
        print(f" Muito curto! Descreva com pelo menos {min_chars} caracteres.")

def ler_id_valido(mensagem, lista_ids_validos, nome_entidade="ID"):
    while True:
        id_digitado = ler_inteiro(mensagem)
        if id_digitado in lista_ids_validos: return id_digitado
        print(f" {nome_entidade} não existe! Escolha um ID da lista acima.")

# INTERFACE
def exibir_menu():
    limpar_tela()
    print("="*60)
    print(" 🏢 SCSC - SISTEMA DE HELPDESK CORPORATIVO ")
    print("="*60)
    print(" 1. Cadastrar Novo Funcionário")
    print(" 2. Abrir Solicitação       (Apenas Solicitante)")
    print(" 3. Painel de Consulta      (Geral)")
    print(" 4. Encaminhar Chamado      (Apenas Operador -> Técnico)")
    print(" 5. Atualizar Status        (Apenas Técnico/Operador)")
    print(" 0. Encerrar o Sistema")
    print("="*60)
    return ler_inteiro(" Escolha uma opção: ", 0, 5)

def main():
    while True:
        opcao = exibir_menu()

        if opcao == 1:
            limpar_tela()
            print("---  CADASTRO DE NOVO FUNCIONÁRIO ---\n")
            nome = ler_nome("Nome completo: ")
            email = ler_email("E-mail corporativo: ")
            print("\n[1] Solicitante | [2] Operador | [3] Técnico")
            op_perfil = ler_inteiro("Selecione o perfil (1 a 3): ", 1, 3)
            perfil = 'solicitante' if op_perfil == 1 else 'operador' if op_perfil == 2 else 'tecnico'
            services.cadastrar_usuario(nome, email, perfil)
            pausar()

        elif opcao == 2:
            limpar_tela()
            print("---  ABERTURA DE NOVA SOLICITAÇÃO ---\n")
            usuarios = services.listar_usuarios()
            if not usuarios:
                print(" Cadastre um funcionário primeiro.")
                pausar()
                continue
            
            for u in usuarios: print(f" ID: {u['id_usuario']:<3} | {u['nome']} ({u['perfil']})")
            id_solicitante = ler_id_valido("\nInforme o SEU ID numérico: ", [u['id_usuario'] for u in usuarios], "Funcionário")
            
            # Bloqueio Lógico
            if services.verificar_perfil(id_solicitante) != 'solicitante':
                print("\n Acesso Negado: Apenas 'Solicitantes' podem abrir novos chamados.")
                pausar()
                continue
            
            categoria = ler_texto_livre("\nCategoria (Ex: Hardware, Sistema): ")
            descricao = ler_texto_livre("Descrição detalhada: ", 10)
            print("\nMatriz (1=Baixo, 2=Médio, 3=Alto):")
            urgencia = ler_inteiro("Nível de URGÊNCIA (1 a 3): ", 1, 3)
            impacto = ler_inteiro("Nível de IMPACTO (1 a 3): ", 1, 3)
            
            services.abrir_chamado(id_solicitante, categoria, descricao, urgencia, impacto)
            pausar()

        elif opcao == 3:
            limpar_tela()
            print("---  PAINEL DE CONSULTA ---\n")
            chamados = services.listar_chamados()
            if not chamados:
                print("Nenhuma solicitação encontrada.")
            else:
                print(f"{'ID':<4} | {'SOLICITANTE':<15} | {'TÉCNICO':<15} | {'PRIORIDADE':<10} | {'STATUS'}")
                print("-" * 75)
                for c in chamados:
                    tecnico = c['tecnico'] if c['tecnico'] else "Não atribuído"
                    print(f"#{c['id_solicitacao']:<3} | {c['solicitante'][:14]:<15} | {tecnico[:14]:<15} | {c['prioridade']:<10} | {c['status']}")
            pausar()

        elif opcao == 4:
            limpar_tela()
            print("---  TRIAGEM: ENCAMINHAR CHAMADO ---\n")
            usuarios = services.listar_usuarios()
            id_operador = ler_id_valido("Informe o SEU ID (Apenas Operadores): ", [u['id_usuario'] for u in usuarios])
            
            if services.verificar_perfil(id_operador) != 'operador':
                print("\n Acesso Negado: Apenas Operadores fazem triagem.")
                pausar()
                continue
                
            chamados = services.listar_chamados()
            ids_chamados = [c['id_solicitacao'] for c in chamados if c['status'] == 'Aberta']
            if not ids_chamados:
                print("\n Não há chamados 'Abertos' aguardando triagem.")
                pausar()
                continue
                
            print("\nChamados Aguardando Triagem:")
            for c in chamados:
                if c['status'] == 'Aberta':
                    print(f" ID: #{c['id_solicitacao']} | Categoria: {c['categoria']} | Prioridade: {c['prioridade']}")
            
            id_chamado = ler_id_valido("\nID do Chamado para encaminhar: ", ids_chamados, "Chamado")
            
            print("\nTécnicos Disponíveis:")
            ids_tecnicos = []
            for u in usuarios:
                if u['perfil'] == 'tecnico':
                    print(f" ID: {u['id_usuario']} | Nome: {u['nome']}")
                    ids_tecnicos.append(u['id_usuario'])
                    
            if not ids_tecnicos:
                print(" Não há técnicos cadastrados no sistema.")
                pausar()
                continue
                
            id_tecnico = ler_id_valido("ID do Técnico escolhido: ", ids_tecnicos, "Técnico")
            services.atribuir_chamado(id_chamado, id_tecnico)
            pausar()

        elif opcao == 5:
            limpar_tela()
            print("---  ATUALIZAÇÃO DE STATUS ---\n")
            usuarios = services.listar_usuarios()
            id_func = ler_id_valido("Informe o SEU ID (Técnico/Operador): ", [u['id_usuario'] for u in usuarios])
            
            if services.verificar_perfil(id_func) == 'solicitante':
                print("\n Acesso Negado: Solicitantes não alteram status de chamados.")
                pausar()
                continue
            
            chamados = services.listar_chamados()
            ids_chamados = [c['id_solicitacao'] for c in chamados if c['status'] != 'Fechada']
            if not ids_chamados:
                print("\n Não há chamados ativos para atualizar.")
                pausar()
                continue
                
            id_chamado = ler_id_valido("\nID do Chamado que será atualizado: ", ids_chamados, "Chamado")
            
            print("\n[1] Em andamento | [2] Fechada")
            op_status = ler_inteiro("Novo Status (1 ou 2): ", 1, 2)
            services.atualizar_status(id_chamado, 'Em andamento' if op_status == 1 else 'Fechada')
            pausar()

        elif opcao == 0:
            print("\nEncerrando conexão com segurança. Até a próxima!\n")
            break

if __name__ == "__main__":
    main()
