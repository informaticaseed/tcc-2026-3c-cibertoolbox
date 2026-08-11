import time


def iniciar_programa():
    # Importação tardia: a interface só é carregada quando o programa inicia.
    from src.Views.login_view import LoginClientView

    print("=" * 25)
    print("Inicializando Janela_login")
    print("=" * 25)
    for i in range(10):
        pontos = "." * (i % 4)
        print(f"\rConectando{pontos:<3}", end="", flush=True)
        time.sleep(0.4)
    print("\nConcluído!")

    app = LoginClientView()
    app.mainloop()
