from src.Views.login_view import LoginClientView
import time
import sys

def iniciar_programa():
    print("=" * 25)
    print("Inicializando Janela_login")
    print("=" * 25)
    for i in range(10):
        # Cria de 0 a 3 pontos usando o resto da divisão por 4
        pontos = "." * (i % 4)
        # O ' ' limpa os pontos antigos quando o ciclo reinicia
        print(f"\rConectando{pontos:<3}", end="", flush=True)
        time.sleep(0.4)
    print("\nConcluído!")
    app = LoginClientView()
    app.mainloop()
