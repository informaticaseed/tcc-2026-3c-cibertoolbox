import customtkinter as ctk

from src.Controller.auth_controller import Auth_validacao
from src.Models.settings_model import SettingsModel


class LoginClientView(ctk.CTk):
    """Tela de login que também respeita o tema salvo em Configurações."""

    def __init__(self):
        super().__init__()

        self.settings_model = SettingsModel()
        self.carregar_tema()

        self.title("CiberToolBox | Login")
        self.geometry("650x430")
        self.resizable(False, False)
        self.configure(fg_color=self.BG)
        self.eval("tk::PlaceWindow . center")

        self.login_inicial()

    def carregar_tema(self):
        tema = self.settings_model.obter_tema()
        self.BG = tema["bg"]
        self.CARD = tema["card"]
        self.BORDER = tema["border"]
        self.TEXT = tema["texto"]
        self.MUTED = tema["texto_secundario"]
        self.DESTAQUE = tema["destaque"]
        self.HOVER = tema["hover"]

    def login_inicial(self):
        ctk.CTkLabel(
            self,
            text="CIBERTOOLBOX",
            text_color=self.TEXT,
            font=("Consolas", 28, "bold"),
        ).pack(pady=(25, 4))

        ctk.CTkLabel(
            self,
            text="Acesso ao ambiente de ferramentas",
            text_color=self.MUTED,
            font=("Arial", 13),
        ).pack(pady=(0, 18))

        painel = ctk.CTkFrame(
            self,
            width=390,
            height=270,
            fg_color=self.CARD,
            border_width=2,
            border_color=self.BORDER,
            corner_radius=22,
        )
        painel.pack()
        painel.pack_propagate(False)

        detalhe = ctk.CTkFrame(
            painel,
            width=14,
            height=220,
            fg_color=self.DESTAQUE,
            corner_radius=8,
        )
        detalhe.place(x=22, rely=0.5, anchor="w")

        ctk.CTkLabel(
            painel,
            text="LOGIN",
            text_color=self.DESTAQUE,
            font=("Consolas", 19, "bold"),
        ).pack(pady=(24, 12))

        self.user = ctk.CTkEntry(
            painel,
            placeholder_text="Usuário",
            width=260,
            height=42,
            corner_radius=14,
            border_color=self.DESTAQUE,
            fg_color=self.BG,
            text_color=self.TEXT,
        )
        self.user.pack(pady=7)

        self.pwd = ctk.CTkEntry(
            painel,
            placeholder_text="Senha",
            show="●",
            width=260,
            height=42,
            corner_radius=14,
            border_color=self.DESTAQUE,
            fg_color=self.BG,
            text_color=self.TEXT,
        )
        self.pwd.pack(pady=7)

        self.btn = ctk.CTkButton(
            painel,
            text="ENTRAR",
            width=180,
            height=40,
            corner_radius=15,
            fg_color=self.DESTAQUE,
            hover_color=self.HOVER,
            text_color="white",
            font=("Arial", 14, "bold"),
            command=self.realizar_login,
        )
        self.btn.pack(pady=(14, 5))

        self.bind("<Return>", lambda _event: self.realizar_login())
        self.user.focus()

    def realizar_login(self):
        Auth_validacao.validar_login(self.user, self.pwd)
