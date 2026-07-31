import math

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageOps

from config import (
    BG_DARK,
    BG_SECONDARY,
    BG_CARD,
    BUTTON_DARK,
    BUTTON_HOVER,
    RED_MAIN,
    RED_DARK,
    RED_GLOW,
    ORANGE_MAIN,
    ORANGE_LIGHT,
    TEXT_LIGHT,
    TEXT_SECONDARY,
    GREEN_STATUS,
    BORDER_DARK,
    MASCOTE_PRINCIPAL,
    ICON_FERRAMENTAS,
    ICON_SERVICOS,
    ICON_CONFIGURACOES,
)


class ClientView(ctk.CTkToplevel):
    """
    Tela principal do CiberToolBox.

    A tela utiliza CTkToplevel porque a janela de login já é
    a janela principal da aplicação.
    """

    def __init__(self, janela_login):
        super().__init__(janela_login)

        self.janela_login = janela_login

        self.menu_aberto = False
        self.animacao_em_execucao = False
        self.pulsacao_ativa = True
        self.pulsacao_passo = 0

        self.title("CiberToolBox")
        self.geometry("1366x768")
        self.minsize(1100, 680)
        self.configure(fg_color=BG_DARK)

        try:
            self.state("zoomed")
        except ctk.TclError:
            pass

        self.protocol(
            "WM_DELETE_WINDOW",
            self.fechar_programa
        )

        self.carregar_imagens()
        self.criar_layout()
        self.iniciar_pulsacao()

    # ========================================================
    # IMAGENS
    # ========================================================

    def carregar_imagem_circular(
        self,
        caminho,
        tamanho,
        margem=0,
    ):
        """
        Carrega qualquer imagem e aplica um recorte circular.

        Isso elimina o fundo quadrado visual, mesmo quando
        a imagem original não possui transparência.
        """

        try:
            imagem = Image.open(caminho).convert("RGBA")

            largura, altura = tamanho

            tamanho_quadrado = min(
                imagem.width,
                imagem.height
            )

            imagem = ImageOps.fit(
                imagem,
                (
                    tamanho_quadrado,
                    tamanho_quadrado,
                ),
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.5),
            )

            imagem = imagem.resize(
                (
                    largura,
                    altura,
                ),
                Image.Resampling.LANCZOS,
            )

            mascara = Image.new(
                "L",
                (
                    largura,
                    altura,
                ),
                0,
            )

            desenho = ImageDraw.Draw(mascara)

            desenho.ellipse(
                (
                    margem,
                    margem,
                    largura - margem,
                    altura - margem,
                ),
                fill=255,
            )

            imagem.putalpha(mascara)

            return ctk.CTkImage(
                light_image=imagem,
                dark_image=imagem,
                size=tamanho,
            )

        except (FileNotFoundError, OSError) as erro:
            print(
                f"Não foi possível carregar a imagem "
                f"{caminho}: {erro}"
            )
            return None

    def carregar_imagem_transparente(
        self,
        caminho,
        tamanho,
    ):
        """
        Carrega um PNG transparente sem aplicar recorte.
        """

        try:
            imagem = Image.open(caminho).convert("RGBA")

            return ctk.CTkImage(
                light_image=imagem,
                dark_image=imagem,
                size=tamanho,
            )

        except (FileNotFoundError, OSError) as erro:
            print(
                f"Não foi possível carregar a imagem "
                f"{caminho}: {erro}"
            )
            return None

    def carregar_imagens(self):
        self.mascote_img = self.carregar_imagem_circular(
            MASCOTE_PRINCIPAL,
            (300, 300),
            margem=3,
        )

        # Os ícones também recebem recorte circular.
        # Isso evita o quadrado de fundo das imagens.
        self.icon_ferramentas = self.carregar_imagem_circular(
            ICON_FERRAMENTAS,
            (68, 68),
            margem=3,
        )

        self.icon_servicos = self.carregar_imagem_circular(
            ICON_SERVICOS,
            (68, 68),
            margem=3,
        )

        self.icon_configuracoes = self.carregar_imagem_circular(
            ICON_CONFIGURACOES,
            (68, 68),
            margem=3,
        )

    # ========================================================
    # LAYOUT GERAL
    # ========================================================

    def criar_layout(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.criar_barra_superior()
        self.criar_conteudo()
        self.criar_barra_inferior()

    def criar_barra_superior(self):
        self.barra_superior = ctk.CTkFrame(
            self,
            height=70,
            corner_radius=0,
            fg_color=BG_SECONDARY,
            border_width=1,
            border_color=BORDER_DARK,
        )
        self.barra_superior.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        self.barra_superior.grid_columnconfigure(
            1,
            weight=1,
        )

        simbolo_logo = ctk.CTkLabel(
            self.barra_superior,
            text="▣",
            font=("Arial", 22, "bold"),
            text_color=RED_MAIN,
            width=35,
        )
        simbolo_logo.grid(
            row=0,
            column=0,
            padx=(28, 5),
            pady=16,
        )

        titulo_logo = ctk.CTkLabel(
            self.barra_superior,
            text="CiberToolBox",
            font=("Arial", 19, "bold"),
            text_color=TEXT_LIGHT,
        )
        titulo_logo.grid(
            row=0,
            column=1,
            sticky="w",
            pady=16,
        )

        status = ctk.CTkLabel(
            self.barra_superior,
            text="●  Sistema protegido",
            font=("Arial", 13),
            text_color=GREEN_STATUS,
            fg_color=BG_CARD,
            corner_radius=18,
            padx=18,
            pady=8,
        )
        status.grid(
            row=0,
            column=2,
            padx=28,
            pady=14,
        )

    def criar_conteudo(self):
        self.conteudo = ctk.CTkFrame(
            self,
            fg_color=BG_DARK,
            corner_radius=0,
        )
        self.conteudo.grid(
            row=1,
            column=0,
            sticky="nsew",
        )

        self.conteudo.grid_rowconfigure(
            1,
            weight=1,
        )
        self.conteudo.grid_columnconfigure(
            0,
            weight=1,
        )

        self.criar_cabecalho()
        self.criar_area_interativa()

    def criar_cabecalho(self):
        cabecalho = ctk.CTkFrame(
            self.conteudo,
            fg_color="transparent",
        )
        cabecalho.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(25, 5),
        )

        titulo = ctk.CTkLabel(
            cabecalho,
            text="CIBERTOOLBOX",
            font=("Consolas", 38, "bold"),
            text_color=TEXT_LIGHT,
        )
        titulo.pack()

        subtitulo = ctk.CTkLabel(
            cabecalho,
            text=(
                "Seu kit de ferramentas para "
                "um mundo mais seguro."
            ),
            font=("Arial", 14),
            text_color=TEXT_SECONDARY,
        )
        subtitulo.pack(pady=(6, 0))

    def criar_area_interativa(self):
        self.area_interativa = ctk.CTkFrame(
            self.conteudo,
            fg_color="transparent",
            height=530,
        )
        self.area_interativa.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=30,
            pady=(0, 10),
        )

        self.area_interativa.grid_propagate(False)

        self.criar_aneis_decorativos()
        self.criar_mascote()
        self.criar_botoes_animados()

        self.instrucao = ctk.CTkLabel(
            self.area_interativa,
            text="Clique no mascote para abrir o menu",
            font=("Arial", 13),
            text_color=TEXT_SECONDARY,
        )
        self.instrucao.place(
            relx=0.5,
            rely=0.95,
            anchor="center",
        )

    def criar_barra_inferior(self):
        self.barra_inferior = ctk.CTkFrame(
            self,
            height=58,
            corner_radius=0,
            fg_color=BG_SECONDARY,
            border_width=1,
            border_color=BORDER_DARK,
        )
        self.barra_inferior.grid(
            row=2,
            column=0,
            sticky="ew",
        )

        self.barra_inferior.grid_columnconfigure(
            0,
            weight=1,
        )

        mensagem = ctk.CTkLabel(
            self.barra_inferior,
            text=(
                "◇  Pronto para proteger. "
                "Pronto para explorar."
            ),
            font=("Arial", 13),
            text_color=TEXT_SECONDARY,
        )
        mensagem.grid(
            row=0,
            column=0,
            sticky="w",
            padx=28,
            pady=17,
        )

        versao = ctk.CTkLabel(
            self.barra_inferior,
            text="v0.2.0",
            font=("Consolas", 12),
            text_color=TEXT_SECONDARY,
        )
        versao.grid(
            row=0,
            column=1,
            padx=28,
            pady=17,
        )

    # ========================================================
    # MASCOTE
    # ========================================================

    def criar_aneis_decorativos(self):
        self.anel_luz = ctk.CTkFrame(
            self.area_interativa,
            width=390,
            height=390,
            corner_radius=195,
            fg_color=RED_DARK,
        )
        self.anel_luz.place(
            relx=0.5,
            rely=0.50,
            anchor="center",
        )

        self.anel_externo = ctk.CTkFrame(
            self.anel_luz,
            width=375,
            height=375,
            corner_radius=187,
            fg_color=RED_MAIN,
        )
        self.anel_externo.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
        )

        self.anel_medio = ctk.CTkFrame(
            self.anel_externo,
            width=359,
            height=359,
            corner_radius=179,
            fg_color="#272D35",
        )
        self.anel_medio.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
        )

        self.anel_interno = ctk.CTkFrame(
            self.anel_medio,
            width=340,
            height=340,
            corner_radius=170,
            fg_color=BG_CARD,
        )
        self.anel_interno.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
        )

    def criar_mascote(self):
        if self.mascote_img is not None:
            self.botao_mascote = ctk.CTkButton(
                self.anel_interno,
                text="",
                image=self.mascote_img,
                width=320,
                height=320,
                corner_radius=160,
                fg_color="transparent",
                hover_color="#222833",
                border_width=0,
                command=self.alternar_menu,
            )
        else:
            self.botao_mascote = ctk.CTkButton(
                self.anel_interno,
                text="MASCOTE\n\nClique aqui",
                width=320,
                height=320,
                corner_radius=160,
                fg_color=BG_CARD,
                hover_color="#222833",
                text_color=ORANGE_LIGHT,
                font=("Arial", 20, "bold"),
                command=self.alternar_menu,
            )

        self.botao_mascote.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
        )

    # ========================================================
    # BOTÕES CIRCULARES
    # ========================================================

    def criar_botao_circular(
        self,
        imagem,
        texto,
        comando,
    ):
        """
        Cria um botão realmente circular.

        Como largura e altura são iguais, o corner_radius
        deve ser exatamente a metade.
        """

        return ctk.CTkButton(
            self.area_interativa,
            text=texto,
            image=imagem,
            compound="top",
            width=170,
            height=170,
            corner_radius=85,
            fg_color=BUTTON_DARK,
            hover_color=BUTTON_HOVER,
            border_width=4,
            border_color=RED_MAIN,
            text_color=TEXT_LIGHT,
            font=("Arial", 15, "bold"),
            command=comando,
        )

    def criar_botoes_animados(self):
        self.botao_ferramentas = self.criar_botao_circular(
            self.icon_ferramentas,
            "Ferramentas",
            self.abrir_ferramentas,
        )

        self.botao_servicos = self.criar_botao_circular(
            self.icon_servicos,
            "Serviços",
            self.abrir_servicos,
        )

        self.botao_configuracoes = self.criar_botao_circular(
            self.icon_configuracoes,
            "Configurações",
            self.abrir_configuracoes,
        )

        self.botoes_animados = {
            self.botao_ferramentas: {
                "destino": (0.23, 0.50),
            },
            self.botao_servicos: {
                "destino": (0.77, 0.50),
            },
            self.botao_configuracoes: {
                "destino": (0.50, 0.86),
            },
        }

        for botao in self.botoes_animados:
            botao.place(
                relx=0.5,
                rely=0.50,
                anchor="center",
            )
            botao.lower()

        self.anel_luz.lift()

    # ========================================================
    # ANIMAÇÃO
    # ========================================================

    def alternar_menu(self):
        if self.animacao_em_execucao:
            return

        if self.menu_aberto:
            self.fechar_menu()
        else:
            self.abrir_menu()

    def abrir_menu(self):
        self.menu_aberto = True
        self.animacao_em_execucao = True

        self.instrucao.configure(
            text=(
                "Selecione uma opção ou clique "
                "novamente no mascote"
            )
        )

        for botao in self.botoes_animados:
            botao.lift()

        self.anel_luz.lift()

        self.animar_botoes(
            abrindo=True,
            passo=0,
            total_passos=24,
        )

    def fechar_menu(self):
        self.menu_aberto = False
        self.animacao_em_execucao = True

        self.animar_botoes(
            abrindo=False,
            passo=0,
            total_passos=24,
        )

    def animar_botoes(
        self,
        abrindo,
        passo,
        total_passos,
    ):
        origem_x = 0.5
        origem_y = 0.50

        progresso = passo / total_passos

        # Curva de suavização.
        progresso_suave = (
            progresso
            * progresso
            * (3 - 2 * progresso)
        )

        for botao, dados in self.botoes_animados.items():
            destino_x, destino_y = dados["destino"]

            if abrindo:
                x = origem_x + (
                    destino_x - origem_x
                ) * progresso_suave

                y = origem_y + (
                    destino_y - origem_y
                ) * progresso_suave

            else:
                x = destino_x + (
                    origem_x - destino_x
                ) * progresso_suave

                y = destino_y + (
                    origem_y - destino_y
                ) * progresso_suave

            botao.place(
                relx=x,
                rely=y,
                anchor="center",
            )

        if passo < total_passos:
            self.after(
                15,
                lambda: self.animar_botoes(
                    abrindo,
                    passo + 1,
                    total_passos,
                ),
            )
            return

        self.animacao_em_execucao = False
        self.anel_luz.lift()

        if not abrindo:
            for botao in self.botoes_animados:
                botao.lower()

            self.instrucao.configure(
                text="Clique no mascote para abrir o menu"
            )

    # ========================================================
    # PULSAÇÃO DO ANEL
    # ========================================================

    def iniciar_pulsacao(self):
        if not self.pulsacao_ativa:
            return

        intensidade = (
            math.sin(self.pulsacao_passo / 8) + 1
        ) / 2

        if intensidade > 0.5:
            cor = RED_MAIN
        else:
            cor = RED_DARK

        self.anel_luz.configure(
            fg_color=cor
        )

        self.pulsacao_passo += 1

        self.after(
            90,
            self.iniciar_pulsacao,
        )

    # ========================================================
    # AÇÕES
    # ========================================================

    def abrir_ferramentas(self):
        self.criar_janela_aviso(
            "Ferramentas",
            (
                "Aqui serão adicionados Ping, Hash, DNS, "
                "Scanner de Portas e outras ferramentas."
            ),
        )

    def abrir_servicos(self):
        self.criar_janela_aviso(
            "Serviços",
            (
                "Aqui serão adicionados Histórico, "
                "Relatórios, Jogos e Ajuda."
            ),
        )

    def abrir_configuracoes(self):
        self.criar_janela_aviso(
            "Configurações",
            (
                "Aqui serão adicionados temas, cores, "
                "perfil e preferências."
            ),
        )

    def criar_janela_aviso(
        self,
        titulo,
        mensagem,
    ):
        janela = ctk.CTkToplevel(self)

        janela.title(titulo)
        janela.geometry("470x250")
        janela.resizable(False, False)
        janela.configure(fg_color=BG_DARK)

        janela.transient(self)
        janela.grab_set()

        titulo_label = ctk.CTkLabel(
            janela,
            text=titulo,
            font=("Arial", 24, "bold"),
            text_color=ORANGE_MAIN,
        )
        titulo_label.pack(
            pady=(30, 15)
        )

        mensagem_label = ctk.CTkLabel(
            janela,
            text=mensagem,
            font=("Arial", 14),
            text_color=TEXT_LIGHT,
            wraplength=390,
            justify="center",
        )
        mensagem_label.pack(
            padx=30,
            pady=10,
        )

        botao_fechar = ctk.CTkButton(
            janela,
            text="Fechar",
            width=140,
            height=36,
            fg_color=RED_MAIN,
            hover_color=RED_DARK,
            command=janela.destroy,
        )
        botao_fechar.pack(
            pady=15
        )

    # ========================================================
    # ENCERRAMENTO
    # ========================================================

    def fechar_programa(self):
        self.pulsacao_ativa = False
        self.janela_login.destroy()