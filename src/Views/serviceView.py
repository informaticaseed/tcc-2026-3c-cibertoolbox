import customtkinter as ctk
import subprocess
import sys
from pathlib import Path
from tkinter import messagebox

from src.Models.settings_model import SettingsModel
from src.Views.historyView import HistoryView


class ServicesView(ctk.CTkToplevel):

    def __init__(self, janela_principal):
        super().__init__(janela_principal)

        self.janela_principal = janela_principal

        tema = SettingsModel().obter_tema()

        self.BG = tema["bg"]
        self.SIDE = tema["secundario"]
        self.CARD = tema["card"]
        self.CARD_HOVER = tema["card_hover"]
        self.PANEL = tema["painel"]
        self.BORDER = tema["border"]

        self.TEXT = tema["texto"]
        self.MUTED = tema["texto_secundario"]

        self.DESTAQUE = tema["destaque"]
        self.HOVER = tema["hover"]

        self.title(
            "CiberToolBox - Serviços"
        )

        self.geometry(
            "1200x700"
        )

        self.minsize(
            950,
            600
        )

        self.configure(
            fg_color=self.BG
        )

        self.protocol(
            "WM_DELETE_WINDOW",
            self.fechar
        )

        self.janela_principal.withdraw()

        try:
            self.state("zoomed")
        except ctk.TclError:
            pass

        self.criar_layout()

    # ========================================================
    # LAYOUT
    # ========================================================

    def criar_layout(self):
        topo = ctk.CTkFrame(
            self,
            height=72,
            corner_radius=0,
            fg_color=self.PANEL,
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
            pady=16,
        )

        ctk.CTkLabel(
            topo,
            text="SERVIÇOS",
            font=(
                "Consolas",
                26,
                "bold"
            ),
            text_color=self.DESTAQUE,
        ).pack(
            side="left",
            padx=10,
        )

        conteudo = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        conteudo.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=35,
        )

        ctk.CTkLabel(
            conteudo,
            text="Recursos do CiberToolBox",
            font=(
                "Arial",
                27,
                "bold"
            ),
            text_color=self.TEXT,
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            conteudo,
            text=(
                "Histórico, relatórios, orientação "
                "e recursos complementares."
            ),
            text_color=self.MUTED,
        ).pack(
            anchor="w",
            pady=(5, 25)
        )

        grade = ctk.CTkFrame(
            conteudo,
            fg_color="transparent"
        )

        grade.pack(
            fill="both",
            expand=True
        )

        grade.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        self.criar_card(
            grade,
            0,
            0,
            "Histórico",
            (
                "Consulte as ferramentas utilizadas "
                "e seus resultados resumidos."
            ),
            self.abrir_historico,
        )

        self.criar_card(
            grade,
            0,
            1,
            "Relatórios",
            (
                "Gere relatórios a partir das "
                "atividades registradas."
            ),
            self.relatorio_em_breve,
        )

        self.criar_card(
            grade,
            1,
            0,
            "Central de Ajuda",
            (
                "Entenda o objetivo e o uso correto "
                "das funcionalidades."
            ),
            self.abrir_ajuda,
        )

        self.criar_card(
            grade,
            1,
            1,
            "Jogos",
            (
                "Acesse recursos recreativos "
                "secundários do projeto."
            ),
            self.abrir_jogos,
        )

    # ========================================================
    # CARD
    # ========================================================

    def criar_card(
        self,
        pai,
        linha,
        coluna,
        titulo,
        descricao,
        comando,
    ):
        card = ctk.CTkFrame(
            pai,
            fg_color=self.CARD,
            border_width=1,
            border_color=self.BORDER,
            corner_radius=18,
        )

        card.grid(
            row=linha,
            column=coluna,
            sticky="nsew",
            padx=10,
            pady=10,
        )

        ctk.CTkLabel(
            card,
            text=titulo,
            font=(
                "Arial",
                20,
                "bold"
            ),
            text_color=self.DESTAQUE,
        ).pack(
            anchor="w",
            padx=24,
            pady=(25, 8),
        )

        ctk.CTkLabel(
            card,
            text=descricao,
            wraplength=360,
            justify="left",
            text_color=self.MUTED,
        ).pack(
            anchor="w",
            padx=24,
        )

        ctk.CTkButton(
            card,
            text="Abrir",
            height=40,
            fg_color=self.DESTAQUE,
            hover_color=self.HOVER,
            command=comando,
        ).pack(
            anchor="w",
            padx=24,
            pady=25,
        )

    # ========================================================
    # HISTÓRICO
    # ========================================================

    def abrir_historico(self):
        HistoryView(self)

    # ========================================================
    # RELATÓRIO
    # ========================================================

    def relatorio_em_breve(self):
        messagebox.showinfo(
            "Relatórios",
            (
                "O próximo passo será gerar "
                "relatórios diretamente do histórico."
            ),
            parent=self,
        )

    # ========================================================
    # AJUDA
    # ========================================================

    def abrir_ajuda(self):
        messagebox.showinfo(
            "Central de Ajuda",
            (
                "Ferramentas de auditoria devem ser "
                "utilizadas somente em ambientes próprios "
                "ou devidamente autorizados.\n\n"
                "A dashboard de Ferramentas apresenta "
                "uma descrição antes da execução."
            ),
            parent=self,
        )

    # ========================================================
    # JOGOS
    # ========================================================

    def abrir_jogos(self):
        janela = ctk.CTkToplevel(self)

        janela.title(
            "Jogos"
        )

        janela.geometry(
            "420x300"
        )

        janela.configure(
            fg_color=self.BG
        )

        ctk.CTkLabel(
            janela,
            text="Jogos",
            font=(
                "Arial",
                23,
                "bold"
            ),
            text_color=self.TEXT,
        ).pack(
            pady=25
        )

        ctk.CTkButton(
            janela,
            text="Dino",
            width=220,
            height=42,
            command=self.executar_dino,
        ).pack(
            pady=8
        )

        ctk.CTkButton(
            janela,
            text="Flappy Bird",
            width=220,
            height=42,
            command=self.executar_flappy,
        ).pack(
            pady=8
        )

    def executar_dino(self):
        raiz = Path(__file__).resolve().parents[2]

        script = (
            raiz
            / "src"
            / "Servicos"
            / "Dino_game"
            / "main.py"
        )

        subprocess.Popen(
            [
                sys.executable,
                str(script),
            ]
        )

    def executar_flappy(self):
        raiz = Path(__file__).resolve().parents[2]

        script = (
            raiz
            / "src"
            / "Servicos"
            / "Flappy_Bird"
            / "Main.py"
        )

        subprocess.Popen(
            [
                sys.executable,
                str(script),
            ]
        )

    # ========================================================
    # FECHAR
    # ========================================================

    def fechar(self):
        self.destroy()

        if self.janela_principal.winfo_exists():
            self.janela_principal.deiconify()

            self.janela_principal.lift()
            self.janela_principal.focus_force()