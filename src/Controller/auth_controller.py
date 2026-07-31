import customtkinter as ctk
from tkinter import messagebox

from src.Models.Validação import Verification
from src.Views.main_window import ClientView


class Auth_validacao:

    @classmethod
    def validar_login(cls, user, pwd):
        # Captura os valores digitados na interface.
        usuario = user.get().strip().upper()

        # A senha não deve receber upper() nem strip().
        senha = pwd.get()

        # Verifica se os campos estão vazios.
        if not usuario or not senha:
            messagebox.showwarning(
                "Campos obrigatórios",
                "Informe o usuário e a senha."
            )
            return

        model_validador = Verification()

        if model_validador.checar_credenciais(usuario, senha):
            messagebox.showinfo(
                "Login realizado",
                "Acesso autorizado."
            )

            janela_login = user.winfo_toplevel()
            janela_login.withdraw()

            ClientView(janela_login)

        else:
            messagebox.showerror(
                "Acesso negado",
                "Usuário ou senha inválidos."
            )

            # Apaga apenas a senha.
            pwd.delete(0, ctk.END)
            pwd.focus()