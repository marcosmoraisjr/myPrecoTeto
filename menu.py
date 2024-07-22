# Importando o arquivo app.py
import app


def menu():
    while True:
        app.limpa_tela()
        print("\nOpções:")
        print("0. Sair")
        print("1. Analisar ativos")
        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            break
        elif opcao == "1":
            app.limpa_tela()
            app.principal()
            wait = input("Pressione enter para continuar...")
        else:
            app.limpa_tela()
            print("Opção inválida. Tente novamente.")
            wait = input("Pressione enter para continuar...")


if __name__ == "__main__":
    menu()
