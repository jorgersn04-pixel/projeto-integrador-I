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
        if len(nome) < 3:
            print("❌ O nome é muito curto. Digite um nome completo válido.")
            continue
        if re.match(padrao_nome, nome):
            return nome.title()
        print("❌ Formato Inválido! O nome deve conter APENAS letras e espaços.")


def ler_email(mensagem):
    padrao_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    while True:
        email = input(mensagem).strip().lower()
        if re.match(padrao_email, email):
            return email
        print("❌ E-mail Inválido! Use o formato corporativo: nome@empresa.com")


def ler_inteiro(mensagem, min_val=None, max_val=None):
    while True:
        try:
            valor = int(input(mensagem).strip())
            if min_val is not None and valor < min_val:
                print(f"❌ Valor mínimo permitido: {min_val}.")
                continue
            if max_val is not None and valor > max_val:
                print(f"❌ Valor máximo permitido: {max_val}.")
                continue
            return valor
        except ValueError:
            print("❌ Entrada inválida! Digite APENAS números inteiros.")


def ler_texto_livre(mensagem, min_chars=5):
    while True:
        texto = input(mensagem).strip()
        if len(texto) < min_chars:
            print(f"❌ Muito curto! Digite no mínimo {min_chars} caracteres.")
        else:
            return texto


def ler_id_valido(mensagem, lista_ids_validos, nome_entidade="ID"):
    while True:
        id_digitado = ler_inteiro(mensagem)
        if id_digitado in lista_ids_validos:
            return id_digitado
        print(f"❌ {nome_entidade} inexistente! Escolha um ID válido listado acima.")


# ==============================================================================
# INTERFACE DO SISTEMA
# ==============================================================================

def exibir_menu():
    limpar_tela()
    print("=" * 55)
    print(" 🏢 SCSC - SISTEMA DE HELPDESK CORPORATIVO ")
    print("=" * 55)
    print(" 1. Cadastrar Novo Funcionário")
    print(" 2. Abrir Nova Solicitação (Chamado)")
    print(" 3. Painel de Consulta de Solicitações")
    print(" 4. Atualizar Status de Solicitação")
    print(" 0. Encerrar o Sistema")
    print("=" * 55)
    return ler_inteiro("👉 Escolha uma opção: ", 0, 4)


def main():
    while True:
        opcao = exibir_menu()

        if opcao == 1:
            limpar_tela()
            print("--- 👤 CADASTRO DE NOVO FUNCIONÁRIO ---\n")

            nome = ler_nome("Nome completo: ")
            email = ler_email("E-mail corporativo: ")

            print("\nPerfis de Acesso:")
            print("[1] Solicitante (Abre chamados)")
            print("[2] Operador (Gerencia atendimento)")
            print("[3] Técnico (Realiza manutenção)")

            op_perfil = ler_inteiro("Selecione o perfil (1 a 3): ", 1, 3)
            perfil = 'solicitante' if op_perfil == 1 else 'operador' if op_perfil == 2 else 'tecnico'

            services.cadastrar_usuario(nome, email, perfil)
            pausar()

        elif opcao == 2:
            limpar_tela()
            print("--- 📝 ABERTURA DE NOVA SOLICITAÇÃO ---\n")

            usuarios = services.listar_usuarios()
            if not usuarios:
                print("⚠️  Não há funcionários cadastrados no banco de dados.")
                print("Cadastre um funcionário primeiro para vincular o chamado.")
                pausar()
                continue

            ids_usuarios = [u['id_usuario'] for u in usuarios]

            print("Funcionários disponíveis:")
            for u in usuarios:
                print(f" ID: {u['id_usuario']:<3} | {u['nome']} ({u['perfil']})")

            print("-" * 40)
            id_solicitante = ler_id_valido("ID do Solicitante: ", ids_usuarios, "Funcionário")

            print("\nDetalhamento:")
            categoria = ler_texto_livre("Categoria (Ex: Hardware, Sistema, Rede): ")
            descricao = ler_texto_livre("Descrição detalhada do problema: ", min_chars=10)

            print("\nMatriz de Classificação (1=Baixo, 2=Médio, 3=Alto):")
            urgencia = ler_inteiro("Nível de URGÊNCIA (1 a 3): ", 1, 3)
            impacto = ler_inteiro("Nível de IMPACTO (1 a 3): ", 1, 3)

            services.abrir_chamado(id_solicitante, categoria, descricao, urgencia, impacto)
            pausar()

        elif opcao == 3:
            limpar_tela()
            print("--- 📊 PAINEL DE CONSULTA ---\n")
            chamados = services.listar_chamados()

            if not chamados:
                print("Nenhuma solicitação encontrada na base de dados.")
            else:
                print(f"{'ID':<4} | {'SOLICITANTE':<16} | {'CATEGORIA':<12} | {'PRIORIDADE':<10} | {'STATUS'}")
                print("-" * 75)
                for c in chamados:
                    print(
                        f"#{c['id_solicitacao']:<3} | {c['nome'][:15]:<16} | {c['categoria'][:11]:<12} | {c['prioridade']:<10} | {c['status']}")
            pausar()

        elif opcao == 4:
            limpar_tela()
            print("--- 🔄 ATUALIZAÇÃO DE STATUS ---\n")

            chamados = services.listar_chamados()
            if not chamados:
                print("⚠️  Não há chamados abertos para atualizar.")
                pausar()
                continue

            ids_chamados = [c['id_solicitacao'] for c in chamados]

            print("Últimos chamados registrados:")
            for c in chamados[:5]:
                print(f" ID: #{c['id_solicitacao']:<3} [{c['status']}] - {c['categoria']}")

            print("-" * 40)
            id_chamado = ler_id_valido("\nID do Chamado que será atualizado: ", ids_chamados, "Chamado")

            print("\nSelecione o Novo Status:")
            print("[1] Em andamento")
            print("[2] Fechada")
            op_status = ler_inteiro("Sua escolha (1 ou 2): ", 1, 2)
            novo_status = 'Em andamento' if op_status == 1 else 'Fechada'

            services.atualizar_status(id_chamado, novo_status)
            pausar()

        elif opcao == 0:
            print("\nEncerrando conexão com segurança. Até a próxima!\n")
            break


if __name__ == "__main__":
    main()
