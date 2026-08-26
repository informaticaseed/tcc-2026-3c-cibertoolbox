import customtkinter as ctk
from tkinter import messagebox
from src.Views.tool_execution_view import ToolExecutionView
from src.Models.settings_model import SettingsModel


# ============================================================
# CORES
# ============================================================

BG_PRINCIPAL = "#080B0F"
BG_LATERAL = "#10141A"
BG_CARD = "#151A22"
BG_CARD_HOVER = "#1D2430"
BG_PAINEL = "#0F1319"

VERMELHO = "#FF3B3B"
VERMELHO_ESCURO = "#A92525"
LARANJA = "#FF7A1A"
VERDE = "#2ED573"
AMARELO = "#F1C40F"

TEXTO = "#F4F6F8"
TEXTO_SECUNDARIO = "#9CA4AF"
BORDA = "#2B323D"

def aplicar_tema_salvo():
    """Aplica o tema salvo às constantes usadas por esta dashboard."""
    global BG_PRINCIPAL, BG_LATERAL, BG_CARD, BG_CARD_HOVER, BG_PAINEL
    global VERMELHO, VERMELHO_ESCURO, LARANJA, VERDE, AMARELO
    global TEXTO, TEXTO_SECUNDARIO, BORDA

    tema = SettingsModel().obter_tema()
    BG_PRINCIPAL = tema["bg"]
    BG_LATERAL = tema["secundario"]
    BG_CARD = tema["card"]
    BG_CARD_HOVER = tema["card_hover"]
    BG_PAINEL = tema["painel"]
    VERMELHO = tema["destaque"]
    VERMELHO_ESCURO = tema["hover"]
    LARANJA = tema["destaque"]
    VERDE = tema["verde"]
    AMARELO = tema["amarelo"]
    TEXTO = tema["texto"]
    TEXTO_SECUNDARIO = tema["texto_secundario"]
    BORDA = tema["border"]


# Constantes continuam simples, mas passam a respeitar Configurações.
class ToolsView(ctk.CTkToplevel):
    """
    Dashboard de ferramentas do CiberToolBox.

    Esta tela apresenta:
    - categorias;
    - pesquisa;
    - cartões;
    - painel de detalhes;
    - botão para executar a ferramenta.
    """

    def __init__(self, janela_principal):
        super().__init__(janela_principal)
        aplicar_tema_salvo()
        self.janela_principal = janela_principal
        self.categoria_atual = "Todas"
        self.ferramenta_selecionada = None
        self.cards_criados = []

        self.title("CiberToolBox - Ferramentas")
        self.geometry("1280x720")
        self.minsize(1050, 650)
        self.configure(fg_color=BG_PRINCIPAL)

        # A dashboard substitui visualmente a tela principal enquanto estiver aberta.
        self.janela_principal.withdraw()

        try:
            self.state("zoomed")
        except ctk.TclError:
            pass

        self.protocol("WM_DELETE_WINDOW", self.fechar_tela)

        self.ferramentas = self.criar_catalogo()

        self.criar_layout()
        self.mostrar_ferramentas()
        self.after(80, self.trazer_para_frente)

    def trazer_para_frente(self):
        self.lift()
        self.focus_force()
        try:
            self.attributes("-topmost", True)
            self.after(180, lambda: self.attributes("-topmost", False))
        except ctk.TclError:
            pass

    # ========================================================
    # CATÁLOGO
    # ========================================================

    def criar_catalogo(self):
        """Catálogo central das ferramentas exibidas na dashboard."""
        return [
            {
                "nome": "Ping", "icone": "PING", "categoria": "Rede",
                "descricao": "Verifica conectividade e aceita parâmetros básicos do comando Ping.",
                "explicacao": "Permite testar alcance e latência. Parâmetros extras são validados para evitar execução arbitrária.",
                "status": "Disponível", "cor_status": VERDE, "acao": self.executar_ping,
            },
            {
                "nome": "ConsultDNS", "icone": "DNS", "categoria": "Rede",
                "descricao": "Resolve nomes de domínio e apresenta endereços IP.",
                "explicacao": "Útil para diagnóstico de resolução de nomes e conectividade.",
                "status": "Disponível", "cor_status": VERDE, "acao": self.executar_dns,
            },
            {
                "nome": "ScanPort", "icone": "PORT", "categoria": "Rede",
                "descricao": "Analisa um intervalo controlado de portas TCP.",
                "explicacao": "Destinado a equipamentos próprios ou ambientes autorizados. O limite é configurável.",
                "status": "Disponível", "cor_status": VERDE, "acao": self.executar_scanner,
            },
            {
                "nome": "Nmap", "icone": "NMAP", "categoria": "Auditoria",
                "descricao": "Executa perfis básicos do Nmap com parâmetros controlados.",
                "explicacao": "Permite inventário de portas e identificação leve de serviços. Scripts NSE e opções evasivas ficam bloqueados no protótipo.",
                "status": "EM DESENVOLVIMENTO*", "cor_status": AMARELO, "acao": self.executar_nmap,
            },
            {
                "nome": "Scapy - Diagnóstico ICMP", "icone": "SCAPY", "categoria": "Rede",
                "descricao": "Envia um pacote ICMP simples e apresenta o resumo da resposta.",
                "explicacao": "Demonstra criação e análise de pacotes com Scapy para fins de diagnóstico.",
                "status": "Disponível", "cor_status": VERDE, "acao": self.executar_scapy,
            },
            {
                "nome": "Análise de Vulnerabilidade Web", "icone": "WEB", "categoria": "Auditoria",
                "descricao": "Verifica cabeçalhos HTTP de segurança e informações básicas de TLS.",
                "explicacao": "É uma checagem passiva de configuração. Não explora vulnerabilidades nem tenta obter acesso ao alvo.",
                "status": "Disponível", "cor_status": VERDE, "acao": self.executar_vulnerabilidade,
            },
            {
                "nome": "Hash de Texto", "icone": "HASH", "categoria": "Integridade",
                "descricao": "Calcula hashes SHA-256 e SHA-512 de textos.",
                "explicacao": "Funções hash ajudam a demonstrar integridade e comparação de conteúdo.",
                "status": "Disponível", "cor_status": VERDE, "acao": self.executar_hash,
            },
            {
                "nome": "Hash de Arquivo", "icone": "FILE", "categoria": "Integridade",
                "descricao": "Calcula o hash de um arquivo selecionado.",
                "explicacao": "Permite verificar se um arquivo foi alterado quando existe um hash de referência.",
                "status": "Disponível", "cor_status": VERDE, "acao": self.executar_hash_arquivo,
            },
            {
                "nome": "Comparar Hashes", "icone": "CMP", "categoria": "Integridade",
                "descricao": "Compara dois hashes para verificar se são idênticos.",
                "explicacao": "Útil para validação de integridade de arquivos e conteúdo.",
                "status": "Disponível", "cor_status": VERDE, "acao": self.executar_comparar_hashes,
            },
            {
                "nome": "Criptografar Arquivo", "icone": "LOCK", "categoria": "Criptografia",
                "descricao": "Criptografa um arquivo com senha e cria uma cópia .ctb.",
                "explicacao": "Usa derivação de chave por senha e criptografia autenticada. O arquivo original é mantido.",
                "status": "Disponível", "cor_status": VERDE, "acao": self.executar_criptografar,
            },
            {
                "nome": "Descriptografar Arquivo", "icone": "OPEN", "categoria": "Criptografia",
                "descricao": "Recupera um arquivo .ctb utilizando a senha correta.",
                "explicacao": "A descriptografia valida a integridade e falha caso a senha esteja incorreta ou o arquivo tenha sido alterado.",
                "status": "Disponível", "cor_status": VERDE, "acao": self.executar_descriptografar,
            },
            {
                "nome": "Analisador de Senha", "icone": "PASS", "categoria": "Credenciais",
                "descricao": "Avalia características básicas de uma senha.",
                "explicacao": "A senha é analisada apenas em memória e não é registrada no histórico.",
                "status": "Disponível", "cor_status": VERDE, "acao": self.executar_senha,
            },
            {
                "nome": "Informações do Sistema", "icone": "SYS", "categoria": "Sistema",
                "descricao": "Exibe informações básicas do computador.",
                "explicacao": "Apresenta dados úteis para inventário e diagnóstico do ambiente local.",
                "status": "Disponível", "cor_status": VERDE, "acao": self.executar_sistema,
            },
            {
                "nome": "Gerador de Relatório", "icone": "LOG", "categoria": "Sistema",
                "descricao": "Organiza observações em um relatório simples.",
                "explicacao": "Pode ser usado para registrar resultados sem incluir credenciais ou senhas.",
                "status": "Disponível", "cor_status": VERDE, "acao": self.executar_relatorio,
            },
        ]

    # ========================================================
    # LAYOUT
    # ========================================================

    def criar_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.criar_menu_lateral()
        self.criar_area_principal()

    def criar_menu_lateral(self):
        self.menu_lateral = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0,
            fg_color=BG_LATERAL,
            border_width=1,
            border_color=BORDA,
        )
        self.menu_lateral.grid(
            row=0,
            column=0,
            sticky="nsew",
        )
        self.menu_lateral.grid_propagate(False)

        titulo = ctk.CTkLabel(
            self.menu_lateral,
            text="CIBER TOOL",
            font=("Consolas", 22, "bold"),
            text_color=LARANJA,
        )
        titulo.pack(
            anchor="w",
            padx=25,
            pady=(28, 8),
        )

        subtitulo = ctk.CTkLabel(
            self.menu_lateral,
            text="Categorias",
            font=("Arial", 12),
            text_color=TEXTO_SECUNDARIO,
        )
        subtitulo.pack(
            anchor="w",
            padx=25,
            pady=(0, 20),
        )

        categorias = [
            ("Todas", "Visão geral"),
            ("Rede", "Conectividade"),
            ("Auditoria", "Nmap e análise"),
            ("Integridade", "Hash e arquivos"),
            ("Criptografia", "Proteção de arquivos"),
            ("Credenciais", "Senhas"),
            ("Sistema", "Diagnóstico"),
        ]

        self.botoes_categoria = {}

        for categoria, descricao in categorias:
            botao = ctk.CTkButton(
                self.menu_lateral,
                text=f"{categoria}\n{descricao}",
                width=190,
                height=58,
                anchor="w",
                fg_color="transparent",
                hover_color=BG_CARD_HOVER,
                text_color=TEXTO,
                font=("Arial", 13, "bold"),
                command=lambda valor=categoria: (
                    self.selecionar_categoria(valor)
                ),
            )
            botao.pack(
                padx=18,
                pady=5,
            )

            self.botoes_categoria[categoria] = botao

        self.destacar_categoria("Todas")

        espaco = ctk.CTkFrame(
            self.menu_lateral,
            fg_color="transparent",
        )
        espaco.pack(expand=True)

        aviso = ctk.CTkLabel(
            self.menu_lateral,
            text=(
                "MODO ÉTICO\n"
                "Use as ferramentas somente\n"
                "em ambientes autorizados."
            ),
            font=("Arial", 11),
            text_color=TEXTO_SECUNDARIO,
            justify="left",
        )
        aviso.pack(
            anchor="w",
            padx=25,
            pady=18,
        )

        voltar = ctk.CTkButton(
            self.menu_lateral,
            text="Voltar ao início",
            width=185,
            height=40,
            fg_color=VERMELHO,
            hover_color=VERMELHO_ESCURO,
            command=self.fechar_tela,
        )
        voltar.pack(
            padx=20,
            pady=(0, 22),
        )

    def criar_area_principal(self):
        self.area_principal = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=BG_PRINCIPAL,
        )
        self.area_principal.grid(
            row=0,
            column=1,
            sticky="nsew",
        )

        self.area_principal.grid_rowconfigure(1, weight=1)
        self.area_principal.grid_columnconfigure(0, weight=1)

        self.criar_cabecalho()
        self.criar_conteudo_dashboard()

    def criar_cabecalho(self):
        cabecalho = ctk.CTkFrame(
            self.area_principal,
            height=100,
            corner_radius=0,
            fg_color=BG_PRINCIPAL,
        )
        cabecalho.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=30,
            pady=(20, 0),
        )

        cabecalho.grid_columnconfigure(0, weight=1)

        textos = ctk.CTkFrame(
            cabecalho,
            fg_color="transparent",
        )
        textos.grid(
            row=0,
            column=0,
            sticky="w",
        )

        self.titulo_categoria = ctk.CTkLabel(
            textos,
            text="Todas as ferramentas",
            font=("Arial", 27, "bold"),
            text_color=TEXTO,
        )
        self.titulo_categoria.pack(anchor="w")

        self.resumo_categoria = ctk.CTkLabel(
            textos,
            text=(
                "Selecione uma ferramenta para visualizar "
                "informações e executá-la."
            ),
            font=("Arial", 13),
            text_color=TEXTO_SECUNDARIO,
        )
        self.resumo_categoria.pack(
            anchor="w",
            pady=(4, 0),
        )

        self.campo_pesquisa = ctk.CTkEntry(
            cabecalho,
            width=300,
            height=42,
            placeholder_text="Pesquisar ferramenta...",
            fg_color=BG_CARD,
            border_color=BORDA,
            text_color=TEXTO,
        )
        self.campo_pesquisa.grid(
            row=0,
            column=1,
            padx=(20, 0),
        )

        self.campo_pesquisa.bind(
            "<KeyRelease>",
            lambda evento: self.mostrar_ferramentas(),
        )

    def criar_conteudo_dashboard(self):
        self.conteudo_dashboard = ctk.CTkFrame(
            self.area_principal,
            fg_color="transparent",
        )
        self.conteudo_dashboard.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=30,
            pady=(10, 25),
        )

        self.conteudo_dashboard.grid_rowconfigure(0, weight=1)
        self.conteudo_dashboard.grid_columnconfigure(0, weight=3)
        self.conteudo_dashboard.grid_columnconfigure(1, weight=2)

        self.criar_area_cards()
        self.criar_painel_detalhes()

    def criar_area_cards(self):
        self.area_cards = ctk.CTkScrollableFrame(
            self.conteudo_dashboard,
            fg_color="transparent",
            corner_radius=0,
        )
        self.area_cards.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 15),
        )

        self.area_cards.grid_columnconfigure(0, weight=1)
        self.area_cards.grid_columnconfigure(1, weight=1)

    def criar_painel_detalhes(self):
        self.painel_detalhes = ctk.CTkFrame(
            self.conteudo_dashboard,
            fg_color=BG_PAINEL,
            corner_radius=16,
            border_width=1,
            border_color=BORDA,
        )
        self.painel_detalhes.grid(
            row=0,
            column=1,
            sticky="nsew",
        )

        self.label_icone_detalhe = ctk.CTkLabel(
            self.painel_detalhes,
            text="CTB",
            width=90,
            height=90,
            corner_radius=45,
            fg_color=BG_CARD,
            text_color=LARANJA,
            font=("Consolas", 19, "bold"),
        )
        self.label_icone_detalhe.pack(
            pady=(45, 18),
        )

        self.label_nome_detalhe = ctk.CTkLabel(
            self.painel_detalhes,
            text="Selecione uma ferramenta",
            font=("Arial", 22, "bold"),
            text_color=TEXTO,
        )
        self.label_nome_detalhe.pack(
            padx=25,
        )

        self.label_categoria_detalhe = ctk.CTkLabel(
            self.painel_detalhes,
            text="",
            font=("Arial", 12),
            text_color=LARANJA,
        )
        self.label_categoria_detalhe.pack(
            pady=(5, 20),
        )

        self.label_explicacao = ctk.CTkLabel(
            self.painel_detalhes,
            text=(
                "Escolha um dos cartões ao lado para saber "
                "o que a ferramenta faz e como utilizá-la."
            ),
            font=("Arial", 14),
            text_color=TEXTO_SECUNDARIO,
            justify="left",
            wraplength=330,
        )
        self.label_explicacao.pack(
            padx=35,
            pady=10,
            anchor="w",
        )

        self.label_status_detalhe = ctk.CTkLabel(
            self.painel_detalhes,
            text="Nenhuma ferramenta selecionada",
            font=("Arial", 12, "bold"),
            text_color=TEXTO_SECUNDARIO,
        )
        self.label_status_detalhe.pack(
            pady=20,
        )

        self.botao_executar = ctk.CTkButton(
            self.painel_detalhes,
            text="Selecionar ferramenta",
            width=240,
            height=46,
            fg_color=VERMELHO,
            hover_color=VERMELHO_ESCURO,
            state="disabled",
            command=self.executar_ferramenta_selecionada,
        )
        self.botao_executar.pack(
            pady=15,
        )

    # ========================================================
    # CARTÕES
    # ========================================================

    def mostrar_ferramentas(self):
        for widget in self.area_cards.winfo_children():
            widget.destroy()

        self.cards_criados.clear()

        pesquisa = self.campo_pesquisa.get().strip().lower()

        ferramentas_filtradas = []

        for ferramenta in self.ferramentas:
            categoria_valida = (
                self.categoria_atual == "Todas"
                or ferramenta["categoria"] == self.categoria_atual
            )

            pesquisa_valida = (
                not pesquisa
                or pesquisa in ferramenta["nome"].lower()
                or pesquisa in ferramenta["descricao"].lower()
            )

            if categoria_valida and pesquisa_valida:
                ferramentas_filtradas.append(ferramenta)

        if not ferramentas_filtradas:
            vazio = ctk.CTkLabel(
                self.area_cards,
                text="Nenhuma ferramenta encontrada.",
                font=("Arial", 15),
                text_color=TEXTO_SECUNDARIO,
            )
            vazio.grid(
                row=0,
                column=0,
                columnspan=2,
                pady=80,
            )
            return

        for indice, ferramenta in enumerate(ferramentas_filtradas):
            linha = indice // 2
            coluna = indice % 2

            card = self.criar_card(ferramenta)
            card.grid(
                row=linha,
                column=coluna,
                sticky="nsew",
                padx=8,
                pady=8,
            )

    def criar_card(self, ferramenta):
        card = ctk.CTkFrame(
            self.area_cards,
            height=190,
            fg_color=BG_CARD,
            corner_radius=14,
            border_width=1,
            border_color=BORDA,
        )
        card.grid_propagate(False)

        card.grid_columnconfigure(1, weight=1)

        icone = ctk.CTkLabel(
            card,
            text=ferramenta["icone"],
            width=65,
            height=65,
            corner_radius=32,
            fg_color=BG_PAINEL,
            text_color=LARANJA,
            font=("Consolas", 14, "bold"),
        )
        icone.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=18,
            pady=(20, 5),
        )

        nome = ctk.CTkLabel(
            card,
            text=ferramenta["nome"],
            font=("Arial", 17, "bold"),
            text_color=TEXTO,
        )
        nome.grid(
            row=0,
            column=1,
            sticky="sw",
            pady=(20, 0),
        )

        categoria = ctk.CTkLabel(
            card,
            text=ferramenta["categoria"],
            font=("Arial", 11),
            text_color=LARANJA,
        )
        categoria.grid(
            row=1,
            column=1,
            sticky="nw",
        )

        descricao = ctk.CTkLabel(
            card,
            text=ferramenta["descricao"],
            font=("Arial", 12),
            text_color=TEXTO_SECUNDARIO,
            wraplength=270,
            justify="left",
        )
        descricao.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="w",
            padx=18,
            pady=(10, 8),
        )

        status = ctk.CTkLabel(
            card,
            text=f"● {ferramenta['status']}",
            font=("Arial", 11, "bold"),
            text_color=ferramenta["cor_status"],
        )
        status.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="w",
            padx=18,
            pady=(0, 14),
        )

        widgets_clicaveis = [
            card,
            icone,
            nome,
            categoria,
            descricao,
            status,
        ]

        for widget in widgets_clicaveis:
            widget.bind(
                "<Button-1>",
                lambda evento, item=ferramenta: (
                    self.selecionar_ferramenta(item)
                ),
            )

            widget.bind(
                "<Enter>",
                lambda evento, quadro=card: (
                    quadro.configure(
                        fg_color=BG_CARD_HOVER,
                        border_color=VERMELHO,
                    )
                ),
            )

            widget.bind(
                "<Leave>",
                lambda evento, quadro=card: (
                    quadro.configure(
                        fg_color=BG_CARD,
                        border_color=BORDA,
                    )
                ),
            )

        self.cards_criados.append(card)

        return card

    # ========================================================
    # CATEGORIAS E SELEÇÃO
    # ========================================================

    def selecionar_categoria(self, categoria):
        self.categoria_atual = categoria
        self.destacar_categoria(categoria)

        if categoria == "Todas":
            self.titulo_categoria.configure(
                text="Todas as ferramentas"
            )
        else:
            self.titulo_categoria.configure(
                text=f"Ferramentas de {categoria}"
            )

        self.ferramenta_selecionada = None
        self.limpar_detalhes()
        self.mostrar_ferramentas()

    def destacar_categoria(self, categoria):
        for nome, botao in self.botoes_categoria.items():
            if nome == categoria:
                botao.configure(
                    fg_color="#2B1719",
                    text_color=VERMELHO,
                )
            else:
                botao.configure(
                    fg_color="transparent",
                    text_color=TEXTO,
                )

    def selecionar_ferramenta(self, ferramenta):
        self.ferramenta_selecionada = ferramenta

        self.label_icone_detalhe.configure(
            text=ferramenta["icone"]
        )

        self.label_nome_detalhe.configure(
            text=ferramenta["nome"]
        )

        self.label_categoria_detalhe.configure(
            text=ferramenta["categoria"]
        )

        self.label_explicacao.configure(
            text=ferramenta["explicacao"]
        )

        self.label_status_detalhe.configure(
            text=ferramenta["status"],
            text_color=ferramenta["cor_status"],
        )

        if ferramenta["acao"] is None:
            self.botao_executar.configure(
                text="Ainda não disponível",
                state="disabled",
                fg_color="#343A44",
            )
        else:
            self.botao_executar.configure(
                text="Abrir ferramenta",
                state="normal",
                fg_color=VERMELHO,
            )

    def limpar_detalhes(self):
        self.label_icone_detalhe.configure(text="CTB")
        self.label_nome_detalhe.configure(
            text="Selecione uma ferramenta"
        )
        self.label_categoria_detalhe.configure(text="")
        self.label_explicacao.configure(
            text=(
                "Escolha um dos cartões ao lado para saber "
                "o que a ferramenta faz e como utilizá-la."
            )
        )
        self.label_status_detalhe.configure(
            text="Nenhuma ferramenta selecionada",
            text_color=TEXTO_SECUNDARIO,
        )
        self.botao_executar.configure(
            text="Selecionar ferramenta",
            state="disabled",
            fg_color="#343A44",
        )

    # ========================================================
    # EXECUÇÃO
    # ========================================================

    def executar_ferramenta_selecionada(self):
        if self.ferramenta_selecionada is None:
            return

        acao = self.ferramenta_selecionada["acao"]

        if acao is not None:
            acao()

    def abrir_ferramenta(self, nome):
        ToolExecutionView(self, nome)

    def executar_ping(self):
        self.abrir_ferramenta("Ping")

    def executar_dns(self):
        self.abrir_ferramenta("Consulta DNS")

    def executar_scanner(self):
        self.abrir_ferramenta("Scanner de Portas")

    def executar_hash(self):
        self.abrir_ferramenta("Hash de Texto")

    def executar_hash_arquivo(self):
        self.abrir_ferramenta("Hash de Arquivo")

    def executar_comparar_hashes(self):
        self.abrir_ferramenta("Comparar Hashes")

    def executar_senha(self):
        self.abrir_ferramenta("Analisador de Senha")

    def executar_sistema(self):
        self.abrir_ferramenta("Informações do Sistema")

    def executar_relatorio(self):
        self.abrir_ferramenta("Gerador de Relatório")

    def executar_nmap(self):
        self.abrir_ferramenta("Nmap")

    def executar_scapy(self):
        self.abrir_ferramenta("Scapy - Diagnóstico ICMP")

    def executar_vulnerabilidade(self):
        self.abrir_ferramenta("Análise de Vulnerabilidade Web")

    def executar_criptografar(self):
        self.abrir_ferramenta("Criptografar Arquivo")

    def executar_descriptografar(self):
        self.abrir_ferramenta("Descriptografar Arquivo")

    # ========================================================
    # ENCERRAMENTO
    # ========================================================

    def fechar_tela(self):
        self.destroy()
        if self.janela_principal.winfo_exists():
            self.janela_principal.deiconify()
            try:
                self.janela_principal.state("zoomed")
            except ctk.TclError:
                pass
            self.janela_principal.lift()
            self.janela_principal.focus_force()
