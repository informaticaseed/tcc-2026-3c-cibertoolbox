import customtkinter as ctk
from src.Models.Validação import Verification
import time
class Auth_validacao:
    #Transformando por padrão a classe eum classe inteira sem o instanciamento
    @classmethod
    def validar_login(cls, user, pwd):
        print("="*20)
        print("LOG DE LOGIN")
        print("="*20)
        
        # Instanciamos o model diretamente aqui dentro para a lógica funcionar
        model_validador = Verification()
        
        # Captura e trata os dados dos inputs da View
        usuario = user.get().strip().upper()
        senha = pwd.get().strip().upper()
        
        print(f"User: {usuario}\nSenha: {senha}")
        
        # O IF da validação chamando o Model
        if model_validador.checar_credenciais(usuario, senha):
            print("Login Válido!")
            print("="*20)
            for i in range(10):
                pontos = "." * (i % 4)
                print(f"\rInicializando Tela principal{pontos:<3}", end="", flush=True)
                time.sleep(0.4)
            print("\nConcluído!")
            print("="*20)
            from src.Views.main_window import ClientView
            janela_login = user.winfo_toplevel()
            janela_login.withdraw()
            main_app = ClientView()
            main_app.mainloop()
            
        else:
            print("Login Inválido! Acesso negado.")