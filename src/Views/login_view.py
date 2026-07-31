import customtkinter as ctk

from config import (
    BG_DARK,
    BORDER_DARK,
    BG_CARD,
    ORANGE_HOVER,
    ORANGE_MAIN,
    RED_MAIN,
    TEXT_LIGHT,
    TEXT_MUTED,
)
from src.Controller.auth_controller import Auth_validacao


class LoginClientView(ctk.CTk):
    """Janela de login inspirada no formato desenhado para o projeto."""

    def __init__(self):
        super().__init__()

        self.title("CiberToolBox | Login")
        self.geometry("650x430")
        self.resizable(False, False)
        self.configure(fg_color=BG_DARK)
        self.eval("tk::PlaceWindow . center")

        self.login_inicial()

    def login_inicial(self):
        # Cabeçalho da aplicação.
        ctk.CTkLabel(
            self,
            text="CIBERTOOLBOX",
            text_color=TEXT_LIGHT,
            font=("Consolas", 28, "bold"),
        ).pack(pady=(25, 4))

        ctk.CTkLabel(
            self,
            text="Acesso ao ambiente de ferramentas",
            text_color=TEXT_MUTED,
            font=("Arial", 13),
        ).pack(pady=(0, 18))

        # Painel central escuro, seguindo a forma simples do seu desenho.
        painel = ctk.CTkFrame(
            self,
            width=390,
            height=270,
            fg_color=BG_CARD,
            border_width=2,
            border_color=BORDER_DARK,
            corner_radius=22,
        )
        painel.pack()
        painel.pack_propagate(False)

        detalhe = ctk.CTkFrame(
            painel,
            width=14,
            height=220,
            fg_color=RED_MAIN,
            corner_radius=8,
        )
        detalhe.place(x=22, rely=0.5, anchor="w")

        ctk.CTkLabel(
            painel,
            text="LOGIN",
            text_color=ORANGE_MAIN,
            font=("Consolas", 19, "bold"),
        ).pack(pady=(24, 12))

        self.user = ctk.CTkEntry(
            painel,
            placeholder_text="Usuário",
            width=260,
            height=42,
            corner_radius=14,
            border_color=RED_MAIN,
            fg_color="#181818",
            text_color=TEXT_LIGHT,
        )
        self.user.pack(pady=7)

        self.pwd = ctk.CTkEntry(
            painel,
            placeholder_text="Senha",
            show="●",
            width=260,
            height=42,
            corner_radius=14,
            border_color=RED_MAIN,
            fg_color="#181818",
            text_color=TEXT_LIGHT,
        )
        self.pwd.pack(pady=7)

        self.btn = ctk.CTkButton(
            painel,
            text="ENTRAR",
            width=180,
            height=40,
            corner_radius=15,
            fg_color=ORANGE_MAIN,
            hover_color=ORANGE_HOVER,
            text_color="black",
            font=("Arial", 14, "bold"),
            command=self.realizar_login,
        )
        self.btn.pack(pady=(14, 5))

        # Permite usar Enter para realizar o login.
        self.bind("<Return>", lambda _event: self.realizar_login())
        self.user.focus()

    def realizar_login(self):
        Auth_validacao.validar_login(self.user, self.pwd)
