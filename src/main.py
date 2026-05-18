from services import *


usuario = login()

if usuario is None:

    print("\nUsuário não encontrado")

else:

    print("\n" + "=" * 40)
    print("SCSC".center(40))
    print("=" * 40)

    print(
        f"\nBem-vindo {usuario['nome']}"
    )

    while True:

        print("\n===== MENU =====")

        # =================================
        # SOLICITANTE
        # =================================

        if usuario["perfil"] == "solicitante":

            print("1 - Abrir solicitação")
            print("2 - Minhas solicitações")
            print("0 - Sair")

        # =================================
        # OPERADOR
        # =================================

        elif usuario["perfil"] == "operador":

            print("1 - Cadastrar usuário")
            print("2 - Abrir solicitação")
            print("3 - Listar solicitações")
            print("4 - Atribuir técnico")
            print("5 - Estatísticas")
            print("0 - Sair")

        # =================================
        # TÉCNICO
        # =================================

        elif usuario["perfil"] == "tecnico":

            print("1 - Minhas solicitações")
            print("2 - Atualizar status")
            print("0 - Sair")

        opcao = input("\nEscolha: ")

        # =================================
        # SOLICITANTE
        # =================================

        if usuario["perfil"] == "solicitante":

            match opcao:

                case "1":
                    abrir_solicitacao(usuario)

                case "2":
                    minhas_solicitacoes(usuario)

                case "0":
                    break

                case _:
                    print("\nOpção inválida")

        # =================================
        # OPERADOR
        # =================================

        elif usuario["perfil"] == "operador":

            match opcao:

                case "1":
                    cadastrar_usuario()

                case "2":
                    abrir_solicitacao(usuario)

                case "3":
                    listar_solicitacoes()

                case "4":
                    atribuir_tecnico(usuario)

                case "5":
                    estatisticas()

                case "0":
                    break

                case _:
                    print("\nOpção inválida")

        # =================================
        # TÉCNICO
        # =================================

        elif usuario["perfil"] == "tecnico":

            match opcao:

                case "1":
                    minhas_solicitacoes(usuario)

                case "2":
                    atualizar_status(usuario)

                case "0":
                    break

                case _:
                    print("\nOpção inválida")
