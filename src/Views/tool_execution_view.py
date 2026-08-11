import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox

from src.Controller.ToolsController import ToolsController


BG = "#080B0F"
CARD = "#151A22"
PANEL = "#0F1319"
BORDER = "#2B323D"
TEXT = "#F4F6F8"
MUTED = "#9CA4AF"
RED = "#FF3B3B"
RED_DARK = "#A92525"
ORANGE = "#FF7A1A"
GREEN = "#2ED573"


class ToolExecutionView(ctk.CTkToplevel):
    def __init__(self, dashboard, ferramenta):
        super().__init__(dashboard)
        self.dashboard = dashboard
        self.ferramenta = ferramenta
        self.controller = ToolsController()
        self.arquivo_selecionado = ""

        self.title(f"CiberToolBox - {ferramenta}")
        self.geometry("1050x680")
        self.minsize(900, 600)
        self.configure(fg_color=BG)
        self.protocol("WM_DELETE_WINDOW", self.fechar)

        self.dashboard.withdraw()
        try:
            self.state("zoomed")
        except ctk.TclError:
            pass
        self.after(80, self.trazer_para_frente)
        self.criar_layout()

    def trazer_para_frente(self):
        self.lift()
        self.focus_force()
        try:
            self.attributes("-topmost", True)
            self.after(180, lambda: self.attributes("-topmost", False))
        except ctk.TclError:
            pass

    def criar_layout(self):
        topo = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=0, height=72)
        topo.pack(fill="x")
        ctk.CTkButton(topo, text="← Voltar", width=100, fg_color="transparent",
                      hover_color=CARD, command=self.fechar).pack(side="left", padx=22, pady=16)
        ctk.CTkLabel(topo, text=self.ferramenta, font=("Arial", 24, "bold"),
                     text_color=TEXT).pack(side="left", padx=12)

        corpo = ctk.CTkFrame(self, fg_color="transparent")
        corpo.pack(fill="both", expand=True, padx=30, pady=25)
        corpo.grid_columnconfigure(0, weight=2)
        corpo.grid_columnconfigure(1, weight=3)
        corpo.grid_rowconfigure(0, weight=1)

        self.painel_entrada = ctk.CTkFrame(corpo, fg_color=CARD, border_width=1, border_color=BORDER, corner_radius=16)
        self.painel_entrada.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        self.painel_saida = ctk.CTkFrame(corpo, fg_color=PANEL, border_width=1, border_color=BORDER, corner_radius=16)
        self.painel_saida.grid(row=0, column=1, sticky="nsew", padx=(12, 0))

        ctk.CTkLabel(self.painel_entrada, text="Parâmetros", font=("Arial", 18, "bold"), text_color=ORANGE).pack(anchor="w", padx=24, pady=(24, 16))
        self.criar_campos()

        ctk.CTkLabel(self.painel_saida, text="Resultado", font=("Arial", 18, "bold"), text_color=ORANGE).pack(anchor="w", padx=24, pady=(24, 10))
        self.status = ctk.CTkLabel(self.painel_saida, text="Pronto para executar.", text_color=MUTED, anchor="w")
        self.status.pack(fill="x", padx=24, pady=(0, 10))
        self.resultado = ctk.CTkTextbox(self.painel_saida, fg_color=BG, border_width=1, border_color=BORDER, text_color=TEXT, font=("Consolas", 12))
        self.resultado.pack(fill="both", expand=True, padx=24, pady=(0, 24))

    def entrada(self, placeholder, show=None):
        campo = ctk.CTkEntry(self.painel_entrada, height=42, placeholder_text=placeholder, show=show,
                             fg_color=BG, border_color=BORDER, text_color=TEXT)
        campo.pack(fill="x", padx=24, pady=7)
        return campo

    def criar_campos(self):
        f = self.ferramenta
        if f == "Ping":
            self.host = self.entrada("Host ou IP, ex.: 127.0.0.1")
        elif f == "Consulta DNS":
            self.host = self.entrada("Domínio, ex.: example.com")
        elif f == "Scanner de Portas":
            ctk.CTkLabel(self.painel_entrada, text="Use somente em sistemas próprios ou autorizados.",
                         text_color="#F1C40F", wraplength=330, justify="left").pack(anchor="w", padx=24, pady=(0, 8))
            self.host = self.entrada("Host ou IP")
            self.porta_inicio = self.entrada("Porta inicial, ex.: 1")
            self.porta_fim = self.entrada("Porta final, ex.: 100")
        elif f == "Hash de Texto":
            self.algoritmo = ctk.CTkOptionMenu(self.painel_entrada, values=["SHA-256", "SHA-512"])
            self.algoritmo.pack(fill="x", padx=24, pady=7)
            self.texto = ctk.CTkTextbox(self.painel_entrada, height=180, fg_color=BG, border_width=1, border_color=BORDER)
            self.texto.pack(fill="x", padx=24, pady=7)
        elif f == "Hash de Arquivo":
            self.algoritmo = ctk.CTkOptionMenu(self.painel_entrada, values=["SHA-256", "SHA-512"])
            self.algoritmo.pack(fill="x", padx=24, pady=7)
            self.label_arquivo = ctk.CTkLabel(self.painel_entrada, text="Nenhum arquivo selecionado", text_color=MUTED, wraplength=330)
            self.label_arquivo.pack(padx=24, pady=10)
            ctk.CTkButton(self.painel_entrada, text="Selecionar arquivo", fg_color="#303844", command=self.selecionar_arquivo).pack(fill="x", padx=24, pady=7)
        elif f == "Comparar Hashes":
            self.hash1 = self.entrada("Primeiro hash")
            self.hash2 = self.entrada("Segundo hash")
        elif f == "Analisador de Senha":
            self.senha = self.entrada("Senha para análise", show="●")
            ctk.CTkLabel(self.painel_entrada, text="A senha é analisada somente em memória e não é salva.", text_color=MUTED, wraplength=330).pack(padx=24, pady=8)
        elif f == "Informações do Sistema":
            ctk.CTkLabel(self.painel_entrada, text="Nenhum parâmetro é necessário.", text_color=MUTED).pack(padx=24, pady=20)
        elif f == "Gerador de Relatório":
            self.titulo_relatorio = self.entrada("Título do relatório")
            self.observacoes = ctk.CTkTextbox(self.painel_entrada, height=180, fg_color=BG, border_width=1, border_color=BORDER)
            self.observacoes.pack(fill="x", padx=24, pady=7)

        self.botao_executar = ctk.CTkButton(self.painel_entrada, text="Executar", height=44, fg_color=RED, hover_color=RED_DARK, command=self.executar)
        self.botao_executar.pack(fill="x", padx=24, pady=(22, 8))
        ctk.CTkButton(self.painel_entrada, text="Limpar resultado", height=38, fg_color="transparent", border_width=1, border_color=BORDER, command=self.limpar_resultado).pack(fill="x", padx=24, pady=8)

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(parent=self)
        if caminho:
            self.arquivo_selecionado = caminho
            self.label_arquivo.configure(text=caminho)

    def coletar_dados(self):
        """Lê os widgets na thread da interface e devolve somente dados Python."""
        f = self.ferramenta
        if f in ("Ping", "Consulta DNS"):
            return {"host": self.host.get()}
        if f == "Scanner de Portas":
            return {
                "host": self.host.get(),
                "inicio": self.porta_inicio.get(),
                "fim": self.porta_fim.get(),
            }
        if f == "Hash de Texto":
            return {"texto": self.texto.get("1.0", "end-1c"), "algoritmo": self.algoritmo.get()}
        if f == "Hash de Arquivo":
            return {"arquivo": self.arquivo_selecionado, "algoritmo": self.algoritmo.get()}
        if f == "Comparar Hashes":
            return {"hash1": self.hash1.get(), "hash2": self.hash2.get()}
        if f == "Analisador de Senha":
            return {"senha": self.senha.get()}
        if f == "Gerador de Relatório":
            return {
                "titulo": self.titulo_relatorio.get(),
                "observacoes": self.observacoes.get("1.0", "end-1c"),
            }
        return {}

    def executar(self):
        dados = self.coletar_dados()
        self.botao_executar.configure(state="disabled", text="Executando...")
        self.status.configure(text="Processando...", text_color=ORANGE)
        threading.Thread(target=self._executar_thread, args=(dados,), daemon=True).start()

    def _executar_thread(self, dados):
        try:
            f = self.ferramenta
            if f == "Ping":
                r = self.controller.executar_ping(dados["host"])
            elif f == "Consulta DNS":
                r = self.controller.executar_dns(dados["host"])
            elif f == "Scanner de Portas":
                r = self.controller.executar_port_scan(dados["host"], dados["inicio"], dados["fim"])
            elif f == "Hash de Texto":
                r = self.controller.hash_texto(dados["texto"], dados["algoritmo"])
            elif f == "Hash de Arquivo":
                r = self.controller.hash_arquivo(dados["arquivo"], dados["algoritmo"])
            elif f == "Comparar Hashes":
                r = self.controller.comparar_hashes(dados["hash1"], dados["hash2"])
            elif f == "Analisador de Senha":
                r = self.controller.analisar_senha(dados["senha"])
            elif f == "Informações do Sistema":
                r = self.controller.informacoes_sistema()
            elif f == "Gerador de Relatório":
                r = self.controller.gerar_relatorio(dados["titulo"], dados["observacoes"])
            else:
                return
            self.after(0, lambda: self.mostrar_resultado(r))
        except Exception as erro:
            mensagem = str(erro)
            self.after(0, lambda: self.mostrar_erro(mensagem))

    def mostrar_resultado(self, r):
        self.resultado.delete("1.0", "end")
        texto = r.saida if r.saida else r.mensagem
        self.resultado.insert("1.0", texto)
        self.status.configure(text=r.mensagem, text_color=GREEN if r.sucesso else RED)
        self.botao_executar.configure(state="normal", text="Executar")
        if self.ferramenta == "Gerador de Relatório" and r.sucesso:
            self.exportar_relatorio(r.saida)

    def mostrar_erro(self, erro):
        self.status.configure(text=f"Erro inesperado: {erro}", text_color=RED)
        self.botao_executar.configure(state="normal", text="Executar")

    def exportar_relatorio(self, conteudo):
        caminho = filedialog.asksaveasfilename(parent=self, defaultextension=".txt", filetypes=[("Arquivo de texto", "*.txt")], title="Salvar relatório")
        if caminho:
            try:
                with open(caminho, "w", encoding="utf-8") as arquivo:
                    arquivo.write(conteudo)
                messagebox.showinfo("Relatório", "Relatório salvo com sucesso.", parent=self)
            except OSError as erro:
                messagebox.showerror("Relatório", f"Não foi possível salvar: {erro}", parent=self)

    def limpar_resultado(self):
        self.resultado.delete("1.0", "end")
        self.status.configure(text="Pronto para executar.", text_color=MUTED)

    def fechar(self):
        try:
            self.grab_release()
        except ctk.TclError:
            pass
        self.destroy()
        if self.dashboard.winfo_exists():
            self.dashboard.deiconify()
            try:
                self.dashboard.state("zoomed")
            except ctk.TclError:
                pass
            self.dashboard.lift()
            self.dashboard.focus_force()
