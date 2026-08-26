import customtkinter as ctk
from tkinter import messagebox

from src.Controller.servicesController import ServicesController
from src.Models.settings_model import SettingsModel


class HistoryView(ctk.CTkToplevel):

    def __init__(self, services_view):
        super().__init__(services_view)

        self.services_view = services_view
        self.controller = ServicesController()

        tema = SettingsModel().obter_tema()

        self.BG = tema["bg"]
        self.CARD = tema["card"]
        self.PANEL = tema["painel"]
        self.BORDER = tema["border"]

        self.TEXT = tema["texto"]
        self.MUTED = tema["texto_secundario"]

        self.DESTAQUE = tema["destaque"]
        self.HOVER = tema["hover"]

        self.GREEN = tema["verde"]

        self.title(
            "CiberToolBox - Histórico"
        )

        self.geometry(
            "1200x700"
        )

        self.configure(
            fg_color=self.BG
        )

        self.protocol(
            "WM_DELETE_WINDOW",
            self.fechar
        )

        self.services_view.withdraw()

        try:
            self.state("zoomed")
        except ctk.TclError:
            pass

        self.criar_layout()
        self.carregar_historico()

    # ========================================================
    # LAYOUT
    # ========================================================

    def criar_layout(self):
        topo = ctk.CTkFrame(
            self,
            fg_color=self.PANEL,
            height=70,
            corner_radius=0,
        )

        topo.pack(
            fill="x"
        )

        ctk.CTkButton(
            topo,
            text="← Voltar",
            width=100,
            fg_color="transparent",
            hover_color=self.CARD,
            command=self.fechar,
        ).pack(
            side="left",
            padx=20,
            pady=15,
        )

        ctk.CTkLabel(
            topo,
            text="Histórico de atividades",
            font=(
                "Arial",
                23,
                "bold"
            ),
            text_color=self.TEXT,
        ).pack(
            side="left",
            padx=10,
        )

        # ====================================================
        # PESQUISA
        # ====================================================

        barra = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        barra.pack(
            fill="x",
            padx=30,
            pady=20,
        )

        self.pesquisa = ctk.CTkEntry(
            barra,
            placeholder_text=(
                "Pesquisar ferramenta, categoria ou entrada..."
            ),
            height=42,
        )

        self.pesquisa.pack(
            side="left",
            fill="x",
            expand=True,
        )

        self.pesquisa.bind(
            "<KeyRelease>",
            lambda _evento:
                self.carregar_historico()
        )

        ctk.CTkButton(
            barra,
            text="Limpar histórico",
            width=150,
            height=42,
            fg_color=self.DESTAQUE,
            hover_color=self.HOVER,
            command=self.confirmar_limpeza,
        ).pack(
            side="left",
            padx=(15, 0)
        )

        # ====================================================
        # LISTA
        # ====================================================

        self.lista = ctk.CTkScrollableFrame(
            self,
            fg_color=self.BG,
        )

        self.lista.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25),
        )

    # ========================================================
    # CARREGAR HISTÓRICO
    # ========================================================

    def carregar_historico(self):
        for widget in self.lista.winfo_children():
            widget.destroy()

        texto = self.pesquisa.get().strip()

        if texto:
            registros = (
                self.controller
                .buscar_historico(texto)
            )
        else:
            registros = (
                self.controller
                .listar_historico()
            )

        if not registros:
            ctk.CTkLabel(
                self.lista,
                text=(
                    "Nenhuma atividade foi "
                    "registrada ainda."
                ),
                text_color=self.MUTED,
            ).pack(
                pady=60
            )

            return

        for registro in registros:
            self.criar_card(registro)

    # ========================================================
    # CARD
    # ========================================================

    def criar_card(self, registro):
        card = ctk.CTkFrame(
            self.lista,
            fg_color=self.CARD,
            border_width=1,
            border_color=self.BORDER,
            corner_radius=12,
        )

        card.pack(
            fill="x",
            pady=6,
        )

        topo = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        topo.pack(
            fill="x",
            padx=18,
            pady=(15, 5),
        )

        ctk.CTkLabel(
            topo,
            text=registro["ferramenta"],
            font=(
                "Arial",
                16,
                "bold"
            ),
            text_color=self.TEXT,
        ).pack(
            side="left"
        )

        sucesso = bool(
            registro["sucesso"]
        )

        ctk.CTkLabel(
            topo,
            text=(
                "● Sucesso"
                if sucesso
                else "● Falha"
            ),
            text_color=(
                self.GREEN
                if sucesso
                else self.DESTAQUE
            ),
        ).pack(
            side="right"
        )

        ctk.CTkLabel(
            card,
            text=(
                f"Categoria: "
                f"{registro['categoria'] or '-'}\n"
                f"Entrada: "
                f"{registro['entrada'] or '-'}\n"
                f"Mensagem: "
                f"{registro['mensagem'] or '-'}\n"
                f"Data: "
                f"{registro['criado_em']}"
            ),
            justify="left",
            anchor="w",
            text_color=self.MUTED,
        ).pack(
            fill="x",
            padx=18,
            pady=(0, 15),
        )

    # ========================================================
    # LIMPAR
    # ========================================================

    def confirmar_limpeza(self):
        resposta = messagebox.askyesno(
            "Limpar histórico",
            (
                "Deseja realmente apagar "
                "todo o histórico?"
            ),
            parent=self,
        )

        if not resposta:
            return

        self.controller.limpar_historico()

        self.carregar_historico()

    # ========================================================
    # FECHAR
    # ========================================================

    def fechar(self):
        self.destroy()

        if self.services_view.winfo_exists():
            self.services_view.deiconify()

            self.services_view.lift()
            self.services_view.focus_force()