from usuarios import cadastrar_cliente, cadastrar_tecnico, listar_usuarios
from solicitacoes import abrir_chamado, listar_chamados, atualizar_status_chamado, atribuir_tecnico
from estatisticas import total_chamados, chamados_por_status, chamados_por_tecnico


def menu():
    while True:
        print("\n========== SISTEMA HELP DESK ==========")
        print("1 - Cadastrar cliente")
        print("2 - Cadastrar técnico")
        print("3 - Listar usuários")
        print("4 - Abrir chamado")
        print("5 - Listar chamados")
        print("6 - Atualizar status do chamado")
        print("7 - Atribuir técnico ao chamado")
        print("8 - Ver total de chamados")
        print("9 - Ver chamados por status")
        print("10 - Ver chamados por técnico")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_cliente()
        elif opcao == "2":
            cadastrar_tecnico()
        elif opcao == "3":
            listar_usuarios()
        elif opcao == "4":
            abrir_chamado()
        elif opcao == "5":
            listar_chamados()
        elif opcao == "6":
            atualizar_status_chamado()
        elif opcao == "7":
            atribuir_tecnico()
        elif opcao == "8":
            total_chamados()
        elif opcao == "9":
            chamados_por_status()
        elif opcao == "10":
            chamados_por_tecnico()
        elif opcao == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")


menu()
