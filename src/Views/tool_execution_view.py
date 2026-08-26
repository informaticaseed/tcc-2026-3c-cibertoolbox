import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox

from src.Controller.ToolsController import ToolsController
from src.Models.settings_model import SettingsModel


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
YELLOW = "#F1C40F"


def aplicar_tema_salvo():
    global BG, CARD, PANEL, BORDER, TEXT, MUTED, RED, RED_DARK, ORANGE, GREEN, YELLOW
    tema = SettingsModel().obter_tema()
    BG = tema["bg"]
    CARD = tema["card"]
    PANEL = tema["painel"]
    BORDER = tema["border"]
    TEXT = tema["texto"]
    MUTED = tema["texto_secundario"]
    RED = tema["destaque"]
    RED_DARK = tema["hover"]
    ORANGE = tema["destaque"]
    GREEN = tema["verde"]
    YELLOW = tema["amarelo"]


class ToolExecutionView(ctk.CTkToplevel):
    def __init__(self, dashboard, ferramenta):
        super().__init__(dashboard)
        from src.Controller.servicesController import ServicesController
        aplicar_tema_salvo()
        self.dashboard = dashboard
        self.ferramenta = ferramenta
        self.controller = ToolsController()
        self.services_controller = ServicesController()
        self.arquivo_selecionado = ""

        self.title(f"CiberToolBox - {ferramenta}")
        self.geometry("1100x700")
        self.minsize(930, 620)
        self.configure(fg_color=BG)
        self.protocol("WM_DELETE_WINDOW", self.fechar)

        self.dashboard.withdraw()
        try:
            self.state("zoomed")
        except ctk.TclError:
            pass

        self.criar_layout()
        self.after(80, self.trazer_para_frente)

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
        ctk.CTkButton(
            topo,
            text="← Voltar",
            width=100,
            fg_color="transparent",
            hover_color=CARD,
            command=self.fechar,
        ).pack(side="left", padx=22, pady=16)
        ctk.CTkLabel(
            topo,
            text=self.ferramenta,
            font=("Arial", 24, "bold"),
            text_color=TEXT,
        ).pack(side="left", padx=12)

        corpo = ctk.CTkFrame(self, fg_color="transparent")
        corpo.pack(fill="both", expand=True, padx=30, pady=25)
        corpo.grid_columnconfigure(0, weight=2)
        corpo.grid_columnconfigure(1, weight=3)
        corpo.grid_rowconfigure(0, weight=1)

        self.painel_entrada = ctk.CTkScrollableFrame(
            corpo, fg_color=CARD, border_width=1, border_color=BORDER, corner_radius=16
        )
        self.painel_entrada.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        self.painel_saida = ctk.CTkFrame(
            corpo, fg_color=PANEL, border_width=1, border_color=BORDER, corner_radius=16
        )
        self.painel_saida.grid(row=0, column=1, sticky="nsew", padx=(12, 0))

        ctk.CTkLabel(
            self.painel_entrada,
            text="Parâmetros",
            font=("Arial", 18, "bold"),
            text_color=ORANGE,
        ).pack(anchor="w", padx=24, pady=(24, 16))
        self.criar_campos()

        ctk.CTkLabel(
            self.painel_saida,
            text="Resultado",
            font=("Arial", 18, "bold"),
            text_color=ORANGE,
        ).pack(anchor="w", padx=24, pady=(24, 10))

        self.status = ctk.CTkLabel(
            self.painel_saida,
            text="Pronto para executar.",
            text_color=MUTED,
            anchor="w",
        )
        self.status.pack(fill="x", padx=24, pady=(0, 10))

        self.resultado = ctk.CTkTextbox(
            self.painel_saida,
            fg_color=BG,
            border_width=1,
            border_color=BORDER,
            text_color=TEXT,
            font=("Consolas", 12),
        )
        self.resultado.pack(fill="both", expand=True, padx=24, pady=(0, 24))

    def entrada(self, placeholder, show=None):
        campo = ctk.CTkEntry(
            self.painel_entrada,
            height=42,
            placeholder_text=placeholder,
            show=show,
            fg_color=BG,
            border_color=BORDER,
            text_color=TEXT,
        )
        campo.pack(fill="x", padx=24, pady=7)
        return campo

    def aviso(self, texto):
        ctk.CTkLabel(
            self.painel_entrada,
            text=texto,
            text_color=YELLOW,
            wraplength=330,
            justify="left",
        ).pack(anchor="w", padx=24, pady=(0, 8))

    def seletor_arquivo(self, texto="Selecionar arquivo"):
        self.label_arquivo = ctk.CTkLabel(
            self.painel_entrada,
            text="Nenhum arquivo selecionado",
            text_color=MUTED,
            wraplength=330,
        )
        self.label_arquivo.pack(padx=24, pady=10)
        ctk.CTkButton(
            self.painel_entrada,
            text=texto,
            fg_color="#303844",
            command=self.selecionar_arquivo,
        ).pack(fill="x", padx=24, pady=7)

    def criar_campos(self):
        f = self.ferramenta

        if f == "Ping":
            self.host = self.entrada("Host ou IP, ex.: 127.0.0.1")
            self.parametros = self.entrada("Parâmetros opcionais, ex.: -t ou -n 8 ou -l 1024")
            ctk.CTkLabel(
                self.painel_entrada,
                text=(
                    "Windows: -t, -a, -4, -6, -n, -l, -w e -i.\n"
                    "Linux/macOS: -4, -6, -n, -c, -s, -W e -i.\n"
                    "Os parâmetros são validados antes da execução."
                ),
                text_color=MUTED,
                justify="left",
                wraplength=330,
            ).pack(anchor="w", padx=24, pady=8)

        elif f == "Consulta DNS":
            self.host = self.entrada("Domínio, ex.: example.com")

        elif f == "Scanner de Portas":
            self.aviso("Use somente em sistemas próprios ou em ambientes onde você possui autorização.")
            self.host = self.entrada("Host ou IP")
            self.porta_inicio = self.entrada("Porta inicial, ex.: 1")
            self.porta_fim = self.entrada("Porta final, ex.: 100")

        elif f == "Nmap":
            self.aviso("Nmap é executado apenas com opções básicas de inventário/diagnóstico. Scripts NSE e técnicas evasivas ficam bloqueados.")
            self.host = self.entrada("Host ou IP, ex.: 127.0.0.1")
            self.parametros = self.entrada("Ex.: -sV --version-light --top-ports 20")
            ctk.CTkLabel(
                self.painel_entrada,
                text="Permitidos: -Pn, -n, -sV, --version-light, -F, -T2/-T3/-T4, -6, -p e --top-ports.",
                text_color=MUTED,
                wraplength=330,
                justify="left",
            ).pack(anchor="w", padx=24, pady=8)

        elif f == "Scapy - Diagnóstico ICMP":
            self.aviso("Diagnóstico simples com um pacote ICMP. Em Windows, Scapy pode exigir Npcap e privilégios adequados.")
            self.host = self.entrada("Host ou IP")

        elif f == "Análise de Vulnerabilidade Web":
            self.aviso("Checagem passiva de cabeçalhos HTTP e TLS. Não realiza exploração de vulnerabilidades.")
            self.url = self.entrada("URL, ex.: https://example.com")

        elif f == "Hash de Texto":
            self.algoritmo = ctk.CTkOptionMenu(self.painel_entrada, values=["SHA-256", "SHA-512"])
            self.algoritmo.pack(fill="x", padx=24, pady=7)
            self.texto = ctk.CTkTextbox(self.painel_entrada, height=180, fg_color=BG, border_width=1, border_color=BORDER)
            self.texto.pack(fill="x", padx=24, pady=7)

        elif f == "Hash de Arquivo":
            self.algoritmo = ctk.CTkOptionMenu(self.painel_entrada, values=["SHA-256", "SHA-512"])
            self.algoritmo.pack(fill="x", padx=24, pady=7)
            self.seletor_arquivo()

        elif f == "Comparar Hashes":
            self.hash1 = self.entrada("Primeiro hash")
            self.hash2 = self.entrada("Segundo hash")

        elif f == "Criptografar Arquivo":
            self.aviso("O arquivo original é preservado. Será criado um novo arquivo com extensão .ctb.")
            self.seletor_arquivo()
            self.senha = self.entrada("Senha de criptografia (mínimo 8 caracteres)", show="●")
            self.confirmacao = self.entrada("Repita a senha", show="●")

        elif f == "Descriptografar Arquivo":
            self.aviso("Selecione um arquivo .ctb criado pelo CiberToolBox e informe a mesma senha.")
            self.seletor_arquivo("Selecionar arquivo .ctb")
            self.senha = self.entrada("Senha de descriptografia", show="●")

        elif f == "Analisador de Senha":
            self.senha = self.entrada("Senha para análise", show="●")
            ctk.CTkLabel(
                self.painel_entrada,
                text="A senha é analisada somente em memória e não é salva.",
                text_color=MUTED,
                wraplength=330,
            ).pack(padx=24, pady=8)

        elif f == "Informações do Sistema":
            ctk.CTkLabel(self.painel_entrada, text="Nenhum parâmetro é necessário.", text_color=MUTED).pack(padx=24, pady=20)

        elif f == "Gerador de Relatório":
            self.titulo_relatorio = self.entrada("Título do relatório")
            self.observacoes = ctk.CTkTextbox(self.painel_entrada, height=180, fg_color=BG, border_width=1, border_color=BORDER)
            self.observacoes.pack(fill="x", padx=24, pady=7)

        self.botao_executar = ctk.CTkButton(
            self.painel_entrada,
            text="Executar",
            height=44,
            fg_color=RED,
            hover_color=RED_DARK,
            command=self.executar,
        )
        self.botao_executar.pack(fill="x", padx=24, pady=(22, 8))

        ctk.CTkButton(
            self.painel_entrada,
            text="Limpar resultado",
            height=38,
            fg_color="transparent",
            border_width=1,
            border_color=BORDER,
            command=self.limpar_resultado,
        ).pack(fill="x", padx=24, pady=8)

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(parent=self)
        if caminho:
            self.arquivo_selecionado = caminho
            self.label_arquivo.configure(text=caminho)

    def coletar_dados(self):
        f = self.ferramenta
        if f == "Ping":
            return {"host": self.host.get(), "parametros": self.parametros.get()}
        if f == "Consulta DNS":
            return {"host": self.host.get()}
        if f == "Scanner de Portas":
            return {"host": self.host.get(), "inicio": self.porta_inicio.get(), "fim": self.porta_fim.get()}
        if f == "Nmap":
            return {"host": self.host.get(), "parametros": self.parametros.get()}
        if f == "Scapy - Diagnóstico ICMP":
            return {"host": self.host.get()}
        if f == "Análise de Vulnerabilidade Web":
            return {"url": self.url.get()}
        if f == "Hash de Texto":
            return {"texto": self.texto.get("1.0", "end-1c"), "algoritmo": self.algoritmo.get()}
        if f == "Hash de Arquivo":
            return {"arquivo": self.arquivo_selecionado, "algoritmo": self.algoritmo.get()}
        if f == "Comparar Hashes":
            return {"hash1": self.hash1.get(), "hash2": self.hash2.get()}
        if f == "Criptografar Arquivo":
            return {"arquivo": self.arquivo_selecionado, "senha": self.senha.get(), "confirmacao": self.confirmacao.get()}
        if f == "Descriptografar Arquivo":
            return {"arquivo": self.arquivo_selecionado, "senha": self.senha.get()}
        if f == "Analisador de Senha":
            return {"senha": self.senha.get()}
        if f == "Gerador de Relatório":
            return {"titulo": self.titulo_relatorio.get(), "observacoes": self.observacoes.get("1.0", "end-1c")}
        return {}

    def executar(self):
        dados = self.coletar_dados()
        if self.ferramenta == "Criptografar Arquivo" and dados["senha"] != dados["confirmacao"]:
            self.mostrar_erro("As senhas não coincidem.")
            return

        self.botao_executar.configure(state="disabled", text="Executando...")
        self.status.configure(text="Processando...", text_color=ORANGE)
        threading.Thread(target=self._executar_thread, args=(dados,), daemon=True).start()
    def mostrar_resultado(self, r):
        self.resultado.delete("1.0", "end")
        texto = r.saida if r.saida else r.mensagem
        self.resultado.insert("1.0", texto)
        self.status.configure(text=r.mensagem, text_color=GREEN if r.sucesso else RED)
        self.botao_executar.configure(state="normal", text="Executar")
        self.registrar_no_historico(r)
        if self.ferramenta == "Gerador de Relatório" and r.sucesso:
            self.exportar_relatorio(r.saida)
    def _executar_thread(self, dados):
        try:
            f = self.ferramenta
            if f == "Ping":
                r = self.controller.executar_ping(dados["host"], dados["parametros"])
            elif f == "Consulta DNS":
                r = self.controller.executar_dns(dados["host"])
            elif f == "Scanner de Portas":
                r = self.controller.executar_port_scan(dados["host"], dados["inicio"], dados["fim"])
            elif f == "Nmap":
                r = self.controller.executar_nmap(dados["host"], dados["parametros"])
            elif f == "Scapy - Diagnóstico ICMP":
                r = self.controller.executar_scapy(dados["host"])
            elif f == "Análise de Vulnerabilidade Web":
                r = self.controller.analisar_vulnerabilidade_web(dados["url"])
            elif f == "Hash de Texto":
                r = self.controller.hash_texto(dados["texto"], dados["algoritmo"])
            elif f == "Hash de Arquivo":
                r = self.controller.hash_arquivo(dados["arquivo"], dados["algoritmo"])
            elif f == "Comparar Hashes":
                r = self.controller.comparar_hashes(dados["hash1"], dados["hash2"])
            elif f == "Criptografar Arquivo":
                r = self.controller.criptografar_arquivo(dados["arquivo"], dados["senha"])
            elif f == "Descriptografar Arquivo":
                r = self.controller.descriptografar_arquivo(dados["arquivo"], dados["senha"])
            elif f == "Analisador de Senha":
                r = self.controller.analisar_senha(dados["senha"])
            elif f == "Informações do Sistema":
                r = self.controller.informacoes_sistema()
            elif f == "Gerador de Relatório":
                r = self.controller.gerar_relatorio(dados["titulo"], dados["observacoes"])
            else:
                return
            self.after(0, lambda resultado=r: self.mostrar_resultado(resultado))
        except Exception as erro:
            mensagem = str(erro)
            self.after(0, lambda: self.mostrar_erro(mensagem))
    def registrar_no_historico(
        self,
        resultado
        ):
            try:
                dados = self.coletar_dados()

                categoria = self.obter_categoria()

                entrada = self.obter_entrada_historico(
                    dados
                )

                self.services_controller.registrar_execucao(
                    ferramenta=self.ferramenta,
                    categoria=categoria,
                    entrada=entrada,
                    resultado=resultado,
                )

            except Exception as erro:
                # O histórico não deve impedir
                # a ferramenta de funcionar.
                print(
                    "Erro ao registrar histórico:",
                    erro
                )
    def obter_categoria(self):
        categorias = {
            "Ping": "Rede",
            "Consulta DNS": "Rede",
            "Scanner de Portas": "Rede",
            "Scapy - Diagnóstico ICMP": "Rede",

            "Nmap": "Auditoria",
            "Análise de Vulnerabilidade Web":
                "Auditoria",

            "Hash de Texto": "Integridade",
            "Hash de Arquivo": "Integridade",
            "Comparar Hashes": "Integridade",

            "Criptografar Arquivo":
                "Criptografia",

            "Descriptografar Arquivo":
                "Criptografia",

            "Analisador de Senha":
                "Credenciais",

            "Informações do Sistema":
                "Sistema",
        }

        return categorias.get(
            self.ferramenta,
            "Outros"
        )
    def obter_entrada_historico(
        self,
        dados
    ):
        # Nunca registrar senha.
        if self.ferramenta == "Analisador de Senha":
            return "[não armazenado]"

        if self.ferramenta in (
            "Criptografar Arquivo",
            "Descriptografar Arquivo",
        ):
            return dados.get(
                "arquivo",
                ""
            )

        if self.ferramenta == "Ping":
            return dados.get(
                "host",
                ""
            )

        if self.ferramenta == "Consulta DNS":
            return dados.get(
                "host",
                ""
            )

        if self.ferramenta == "Scanner de Portas":
            return (
                f"{dados.get('host', '')} | "
                f"{dados.get('inicio', '')}-"
                f"{dados.get('fim', '')}"
            )

        if self.ferramenta == "Nmap":
            return dados.get(
                "host",
                ""
            )

        if (
            self.ferramenta
            == "Scapy - Diagnóstico ICMP"
        ):
            return dados.get(
                "host",
                ""
            )

        if (
            self.ferramenta
            == "Análise de Vulnerabilidade Web"
        ):
            return dados.get(
                "url",
                ""
            )

        if self.ferramenta == "Hash de Arquivo":
            return dados.get(
                "arquivo",
                ""
            )

        # Não salvar o texto do Hash de Texto.
        if self.ferramenta == "Hash de Texto":
            return "[texto não armazenado]"

        return ""
    def mostrar_erro(self, erro):
        self.status.configure(text=f"Erro: {erro}", text_color=RED)
        if hasattr(self, "botao_executar"):
            self.botao_executar.configure(state="normal", text="Executar")

    def exportar_relatorio(self, conteudo):
        caminho = filedialog.asksaveasfilename(
            parent=self,
            defaultextension=".txt",
            filetypes=[("Arquivo de texto", "*.txt")],
            title="Salvar relatório",
        )
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