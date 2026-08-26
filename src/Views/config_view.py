import customtkinter as ctk
from tkinter import messagebox
from src.Models.settings_model import SettingsModel


class ConfigView(ctk.CTkToplevel):
    def __init__(self, janela_principal):
        super().__init__(janela_principal)
        self.janela_principal = janela_principal
        self.model = SettingsModel()
        self.dados = self.model.carregar()
        self.carregar_cores()

        self.title("CiberToolBox - Configurações")
        self.geometry("1050x680")
        self.minsize(900, 600)
        self.configure(fg_color=self.BG)
        self.protocol("WM_DELETE_WINDOW", self.fechar)

        self.janela_principal.withdraw()
        try:
            self.state("zoomed")
        except ctk.TclError:
            pass

        self.after(80, self.trazer_para_frente)
        self.criar_layout()

    def carregar_cores(self):
        tema = self.model.obter_tema()
        self.BG = tema["bg"]
        self.SIDE = tema["secundario"]
        self.CARD = tema["card"]
        self.PANEL = tema["painel"]
        self.BORDER = tema["border"]
        self.TEXT = tema["texto"]
        self.MUTED = tema["texto_secundario"]
        self.DESTAQUE = tema["destaque"]
        self.HOVER = tema["hover"]
        self.GREEN = tema["verde"]

    def trazer_para_frente(self):
        self.lift()
        self.focus_force()
        try:
            self.attributes("-topmost", True)
            self.after(180, lambda: self.attributes("-topmost", False))
        except ctk.TclError:
            pass

    def criar_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        lateral = ctk.CTkFrame(
            self, width=240, corner_radius=0, fg_color=self.SIDE,
            border_width=1, border_color=self.BORDER,
        )
        lateral.grid(row=0, column=0, sticky="nsew")
        lateral.grid_propagate(False)

        ctk.CTkLabel(
            lateral, text="CONFIGURAÇÕES", font=("Consolas", 21, "bold"),
            text_color=self.DESTAQUE,
        ).pack(anchor="w", padx=24, pady=(30, 5))
        ctk.CTkLabel(
            lateral, text="Preferências do CiberToolBox", text_color=self.MUTED,
        ).pack(anchor="w", padx=24)
        ctk.CTkLabel(
            lateral,
            text="As alterações são salvas em JSON local e podem ser restauradas a qualquer momento.",
            wraplength=190, justify="left", text_color=self.MUTED,
        ).pack(anchor="w", padx=24, pady=30)
        ctk.CTkButton(
            lateral, text="← Voltar ao início", fg_color=self.DESTAQUE,
            hover_color=self.HOVER, command=self.fechar,
        ).pack(side="bottom", fill="x", padx=22, pady=24)

        principal = ctk.CTkScrollableFrame(self, fg_color=self.BG)
        principal.grid(row=0, column=1, sticky="nsew", padx=30, pady=25)
        ctk.CTkLabel(
            principal, text="Preferências", font=("Arial", 28, "bold"),
            text_color=self.TEXT,
        ).pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(
            principal, text="Personalize a aparência e o comportamento do CiberToolBox.",
            text_color=self.MUTED,
        ).pack(anchor="w", pady=(0, 20))

        aparencia = self.card(principal, "Aparência")

        self.cor_destaque = ctk.StringVar(value=self.dados.get("cor_destaque", "Vermelho"))
        self.linha_opcao(
            aparencia, "Cor de destaque", "Altera botões, títulos e elementos selecionados",
            lambda pai: ctk.CTkOptionMenu(
                pai, values=["Vermelho", "Laranja", "Azul", "Verde", "Roxo"],
                variable=self.cor_destaque,
            ),
        )

        self.tema_fundo = ctk.StringVar(value=self.dados.get("tema_fundo", "Escuro"))
        self.linha_opcao(
            aparencia, "Tema de fundo", "Altera as cores gerais da interface",
            lambda pai: ctk.CTkOptionMenu(
                pai, values=["Escuro", "Preto", "Cinza"], variable=self.tema_fundo,
            ),
        )

        self.escala = ctk.StringVar(value=f"{int(float(self.dados['escala_interface']) * 100)}%")
        self.linha_opcao(
            aparencia, "Escala da interface", "Tamanho geral dos componentes",
            lambda pai: ctk.CTkOptionMenu(
                pai, values=["90%", "100%", "110%", "120%"], variable=self.escala,
            ),
        )

        self.animacoes = ctk.BooleanVar(value=bool(self.dados["animacoes"]))
        self.linha_opcao(
            aparencia, "Animações", "Ativa ou desativa o movimento do menu principal",
            lambda pai: ctk.CTkSwitch(
                pai, text="", variable=self.animacoes, progress_color=self.DESTAQUE,
            ),
        )

        self.maximizado = ctk.BooleanVar(value=bool(self.dados["abrir_maximizado"]))
        self.linha_opcao(
            aparencia, "Abrir maximizado", "Telas principais iniciam ocupando a área disponível",
            lambda pai: ctk.CTkSwitch(
                pai, text="", variable=self.maximizado, progress_color=self.DESTAQUE,
            ),
        )

        rede = self.card(principal, "Ferramentas de rede")
        self.max_portas = ctk.StringVar(value=str(self.dados["max_portas_scan"]))
        self.linha_opcao(
            rede, "Limite do scanner", "Quantidade máxima de portas por varredura",
            lambda pai: ctk.CTkOptionMenu(
                pai, values=["32", "64", "128", "256","512","1024"], variable=self.max_portas,
            ),
        )
        self.timeout = ctk.StringVar(value=str(self.dados["timeout_porta"]))
        self.linha_opcao(
            rede, "Timeout por porta", "Tempo máximo de conexão em segundos",
            lambda pai: ctk.CTkOptionMenu(
                pai, values=["0.10", "0.25", "0.50", "1.00"], variable=self.timeout,
            ),
        )

        sobre = self.card(principal, "Sobre")
        ctk.CTkLabel(
            sobre,
            text=("CiberToolBox v0.3.0\n\nProjeto acadêmico de cibersegurança com foco em "
                  "centralização, usabilidade e aprendizado."),
            justify="left", text_color=self.MUTED, wraplength=680,
        ).pack(anchor="w", padx=22, pady=(0, 18))

        botoes = ctk.CTkFrame(principal, fg_color="transparent")
        botoes.pack(fill="x", pady=12)
        ctk.CTkButton(
            botoes, text="Salvar configurações", height=44,
            fg_color=self.DESTAQUE, hover_color=self.HOVER, command=self.salvar,
        ).pack(side="left")
        ctk.CTkButton(
            botoes, text="Restaurar padrões", height=44, fg_color="transparent",
            border_width=1, border_color=self.BORDER, command=self.restaurar,
        ).pack(side="left", padx=12)
        self.status = ctk.CTkLabel(principal, text="", text_color=self.GREEN)
        self.status.pack(anchor="w")

    def card(self, pai, titulo):
        frame = ctk.CTkFrame(
            pai, fg_color=self.CARD, border_width=1,
            border_color=self.BORDER, corner_radius=14,
        )
        frame.pack(fill="x", pady=10)
        ctk.CTkLabel(
            frame, text=titulo, font=("Arial", 18, "bold"),
            text_color=self.DESTAQUE,
        ).pack(anchor="w", padx=22, pady=(18, 12))
        return frame

    def linha_opcao(self, pai, titulo, descricao, criar_widget):
        linha = ctk.CTkFrame(pai, fg_color="transparent")
        linha.pack(fill="x", padx=22, pady=10)
        texto = ctk.CTkFrame(linha, fg_color="transparent")
        texto.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(
            texto, text=titulo, font=("Arial", 14, "bold"), text_color=self.TEXT,
        ).pack(anchor="w")
        ctk.CTkLabel(texto, text=descricao, text_color=self.MUTED).pack(anchor="w")
        widget = criar_widget(linha)
        widget.pack(side="right", padx=8)

    def coletar(self):
        escala = int(self.escala.get().replace("%", "")) / 100
        return {
            "escala_interface": escala,
            "animacoes": bool(self.animacoes.get()),
            "abrir_maximizado": bool(self.maximizado.get()),
            "max_portas_scan": int(self.max_portas.get()),
            "timeout_porta": float(self.timeout.get()),
            "cor_destaque": self.cor_destaque.get(),
            "tema_fundo": self.tema_fundo.get(),
        }

    def salvar(self):
        dados = self.model.salvar(self.coletar())
        ctk.set_widget_scaling(float(dados["escala_interface"]))
        self.status.configure(text="Configurações salvas. Volte ao início para aplicar a nova aparência.")

    def restaurar(self):
        if not messagebox.askyesno(
            "Restaurar", "Deseja restaurar as configurações padrão?", parent=self,
        ):
            return

        self.dados = self.model.restaurar_padrao()
        self.escala.set("100%")
        self.animacoes.set(True)
        self.maximizado.set(True)
        self.max_portas.set("128")
        self.timeout.set("0.25")
        self.cor_destaque.set("Vermelho")
        self.tema_fundo.set("Escuro")
        ctk.set_widget_scaling(1.0)
        self.status.configure(text="Configurações padrão restauradas.")

    def fechar(self):
        self.destroy()
        if not self.janela_principal.winfo_exists():
            return

        if hasattr(self.janela_principal, "aplicar_configuracoes"):
            self.janela_principal.aplicar_configuracoes()

        self.janela_principal.deiconify()
        config = self.model.carregar()
        try:
            self.janela_principal.state(
                "zoomed" if config.get("abrir_maximizado", True) else "normal"
            )
        except ctk.TclError:
            pass
        self.janela_principal.lift()
        self.janela_principal.focus_force()
