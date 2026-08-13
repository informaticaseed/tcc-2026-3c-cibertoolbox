import customtkinter as ctk
from PIL import Image, ImageDraw, ImageEnhance, ImageOps
from src.Views.tools_view import ToolsView
from src.Views.config_view import ConfigView
from src.Models.settings_model import SettingsModel
from config import (
    BG_DARK,
    BG_SECONDARY,
    TEXT_LIGHT,
    TEXT_SECONDARY,
    GREEN_STATUS,
    RED_MAIN,
    BORDER_DARK,
    MASCOTE_PRINCIPAL,
    ICON_FERRAMENTAS,
    ICON_SERVICOS,
    ICON_CONFIGURACOES,
)


class ClientView(ctk.CTkToplevel):
    """
    Tela principal do CiberToolBox.

    O mascote e os três ícones funcionam como botões.
    Não são utilizados frames como moldura, evitando fundos
    quadrados e círculos deformados.
    """

    def __init__(self, janela_login):
        super().__init__(janela_login)

        self.janela_login = janela_login
        self.settings_model = SettingsModel()
<<<<<<< HEAD
        self.carregar_tema()
=======
>>>>>>> 52a040516716f02d3008580be22adbccae3ec55d

        self.menu_aberto = False
        self.animacao_em_execucao = False

        self.title("CiberToolBox")
        self.geometry("1366x768")
        self.minsize(1050, 650)
        self.configure(fg_color=BG_DARK)

        settings = self.settings_model.carregar()
        ctk.set_widget_scaling(float(settings.get("escala_interface", 1.0)))
        if settings.get("abrir_maximizado", True):
            try:
                self.state("zoomed")
            except ctk.TclError:
                pass

        self.protocol(
            "WM_DELETE_WINDOW",
            self.fechar_programa,
        )

        self.carregar_imagens()
        self.criar_layout()

    # ========================================================
    # TEMA E CONFIGURAÇÕES
    # ========================================================

    def carregar_tema(self):
        """Atualiza as cores usadas por esta View a partir das preferências salvas."""
        global BG_DARK, BG_SECONDARY, TEXT_LIGHT, TEXT_SECONDARY
        global GREEN_STATUS, RED_MAIN, BORDER_DARK

        tema = self.settings_model.obter_tema()
        BG_DARK = tema["bg"]
        BG_SECONDARY = tema["secundario"]
        TEXT_LIGHT = tema["texto"]
        TEXT_SECONDARY = tema["texto_secundario"]
        GREEN_STATUS = tema["verde"]
        RED_MAIN = tema["destaque"]
        BORDER_DARK = tema["border"]
        self.cor_hover_tema = tema["hover"]

    def aplicar_configuracoes(self):
        """Recarrega escala/tema e reconstrói a tela sem criar outro mainloop."""
        self.carregar_tema()
        settings = self.settings_model.carregar()
        ctk.set_widget_scaling(float(settings.get("escala_interface", 1.0)))
        self.configure(fg_color=BG_DARK)
        self.menu_aberto = False
        self.animacao_em_execucao = False

        for widget in self.winfo_children():
            widget.destroy()

        self.criar_layout()

    # ========================================================
    # CARREGAMENTO DAS IMAGENS
    # ========================================================

    def preparar_imagem_circular(
        self,
        caminho,
        tamanho,
        zoom=1.0,
        deslocamento_x=0,
        deslocamento_y=0,
    ):
        """
        Prepara uma imagem circular e permite movimentar o conteúdo
        dentro da área do botão.

        deslocamento_x:
            valor positivo  -> move para a direita
            valor negativo  -> move para a esquerda

        deslocamento_y:
            valor positivo  -> move para baixo
            valor negativo  -> move para cima
        """

        try:
            imagem = Image.open(caminho).convert("RGBA")

            # Recorta a imagem original em formato quadrado.
            lado = min(imagem.width, imagem.height)

            esquerda = (imagem.width - lado) // 2
            topo = (imagem.height - lado) // 2

            imagem = imagem.crop(
                (
                    esquerda,
                    topo,
                    esquerda + lado,
                    topo + lado,
                )
            )

            # O zoom aproxima o conteúdo sem alterar o botão.
            if zoom > 1:
                novo_lado = int(lado / zoom)
                margem = (lado - novo_lado) // 2

                imagem = imagem.crop(
                    (
                        margem,
                        margem,
                        margem + novo_lado,
                        margem + novo_lado,
                    )
                )

            # Redimensiona o desenho para o tamanho definido.
            imagem = ImageOps.fit(
                imagem,
                tamanho,
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.5),
            )

            # Cria a máscara circular.
            mascara = Image.new(
                "L",
                tamanho,
                0,
            )

            desenho = ImageDraw.Draw(mascara)

            desenho.ellipse(
                (
                    0,
                    0,
                    tamanho[0] - 1,
                    tamanho[1] - 1,
                ),
                fill=255,
            )

            imagem.putalpha(mascara)

            # Cria uma área transparente do mesmo tamanho.
            tela_transparente = Image.new(
                "RGBA",
                tamanho,
                (0, 0, 0, 0),
            )

            # Cola a imagem deslocada dentro dessa área.
            tela_transparente.alpha_composite(
                imagem,
                dest=(
                    deslocamento_x,
                    deslocamento_y,
                ),
            )

            return tela_transparente

        except (FileNotFoundError, OSError) as erro:
            print(
                f"Erro ao carregar a imagem '{caminho}': {erro}"
            )
            return None

    def criar_ctk_image(
        self,
        caminho,
        tamanho,
        zoom=1.0,
        brilho=1.0,
        deslocamento_x=0,
        deslocamento_y=0,
    ):
        imagem = self.preparar_imagem_circular(
            caminho=caminho,
            tamanho=tamanho,
            zoom=zoom,
            deslocamento_x=deslocamento_x,
            deslocamento_y=deslocamento_y,
        )

        if imagem is None:
            return None

        if brilho != 1.0:
            canal_alpha = imagem.getchannel("A")

            imagem_rgb = imagem.convert("RGB")

            imagem_rgb = ImageEnhance.Brightness(
                imagem_rgb
            ).enhance(brilho)

            imagem_rgb.putalpha(canal_alpha)
            imagem = imagem_rgb

        return ctk.CTkImage(
            light_image=imagem,
            dark_image=imagem,
            size=tamanho,
        )

    def carregar_imagens(self):
    # ========================================================
    # MASCOTE
    # ========================================================

        self.mascote_normal = self.criar_ctk_image(
            MASCOTE_PRINCIPAL,
            tamanho=(255, 255),
            zoom=1.95,
            brilho=1.0,

            # Posição da imagem dentro do botão:
            deslocamento_x=0,
            deslocamento_y=-2,
        )

        self.mascote_hover = self.criar_ctk_image(
            MASCOTE_PRINCIPAL,
            tamanho=(285, 285),
            zoom=2.0,
            brilho=1.10,
            deslocamento_x=0,
            deslocamento_y=7,
        )

        # ========================================================
        # FERRAMENTAS
        # ========================================================

        self.ferramentas_normal = self.criar_ctk_image(
            ICON_FERRAMENTAS,
            tamanho=(135, 140),
            zoom=1.25,
            brilho=1.0,
            deslocamento_x=0,
            deslocamento_y=-4,
        )

        self.ferramentas_hover = self.criar_ctk_image(
            ICON_FERRAMENTAS,
            tamanho=(140, 140),
            zoom=1.55,
            brilho=1.12,
            deslocamento_x=0,
            deslocamento_y=-4,
        )

        # ========================================================
        # SERVIÇOS
        # ========================================================

        self.servicos_normal = self.criar_ctk_image(
            ICON_SERVICOS,
            tamanho=(135, 135),
            zoom=1.25,
            brilho=1.0,
            deslocamento_x=0,
            deslocamento_y=-3,
        )

        self.servicos_hover = self.criar_ctk_image(
            ICON_SERVICOS,
            tamanho=(140, 140),
            zoom=1.55,
            brilho=1.12,
            deslocamento_x=0,
            deslocamento_y=-3,
        )

        # ========================================================
        # CONFIGURAÇÕES
        # ========================================================

        self.configuracoes_normal = self.criar_ctk_image(
            ICON_CONFIGURACOES,
            tamanho=(135, 135),
            zoom=1.25,
            brilho=1.0,
            deslocamento_x=0,
            deslocamento_y=-2,
        )

        self.configuracoes_hover = self.criar_ctk_image(
            ICON_CONFIGURACOES,
            tamanho=(140, 140),
            zoom=1.55,
            brilho=1.12,
            deslocamento_x=0,
            deslocamento_y=-2,
        )

    # ========================================================
    # LAYOUT PRINCIPAL
    # ========================================================

    def criar_layout(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.criar_barra_superior()
        self.criar_conteudo()
        self.criar_barra_inferior()

    def criar_barra_superior(self):
        barra = ctk.CTkFrame(
            self,
            height=70,
            corner_radius=0,
            fg_color=BG_SECONDARY,
            border_width=1,
            border_color=BORDER_DARK,
        )
        barra.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        barra.grid_columnconfigure(1, weight=1)

        simbolo = ctk.CTkLabel(
            barra,
            text="▣",
            font=("Arial", 21, "bold"),
            text_color=RED_MAIN,
            width=35,
        )
        simbolo.grid(
            row=0,
            column=0,
            padx=(28, 5),
            pady=16,
        )

        nome = ctk.CTkLabel(
            barra,
            text="CiberToolBox",
            font=("Arial", 19, "bold"),
            text_color=TEXT_LIGHT,
        )
        nome.grid(
            row=0,
            column=1,
            sticky="w",
            pady=16,
        )

        status = ctk.CTkLabel(
            barra,
            text="●  Sistema protegido",
            font=("Arial", 13),
            text_color=GREEN_STATUS,
            fg_color="#171C24",
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

        self.conteudo.grid_rowconfigure(1, weight=1)
        self.conteudo.grid_columnconfigure(0, weight=1)

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
            pady=(20, 0),
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
            text="Seu kit de ferramentas para um mundo mais seguro.",
            font=("Arial", 14),
            text_color=TEXT_SECONDARY,
        )
        subtitulo.pack(pady=(5, 0))

    def criar_area_interativa(self):
        self.area_interativa = ctk.CTkFrame(
            self.conteudo,
            fg_color="transparent",
        )
        self.area_interativa.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(5, 0),
        )

        self.criar_mascote()
        self.criar_botoes_menu()
        self.criar_instrucao()

    def criar_barra_inferior(self):
        barra = ctk.CTkFrame(
            self,
            height=55,
            corner_radius=0,
            fg_color=BG_SECONDARY,
            border_width=1,
            border_color=BORDER_DARK,
        )
        barra.grid(
            row=2,
            column=0,
            sticky="ew",
        )

        barra.grid_columnconfigure(0, weight=1)

        mensagem = ctk.CTkLabel(
            barra,
            text="◇  Pronto para proteger. Pronto para explorar.",
            font=("Arial", 13),
            text_color=TEXT_SECONDARY,
        )
        mensagem.grid(
            row=0,
            column=0,
            sticky="w",
            padx=28,
            pady=15,
        )

        versao = ctk.CTkLabel(
            barra,
            text="v0.3.0",
            font=("Consolas", 12),
            text_color=TEXT_SECONDARY,
        )
        versao.grid(
            row=0,
            column=1,
            padx=28,
            pady=15,
        )

    # ========================================================
    # MASCOTE
    # ========================================================

    def criar_mascote(self):
        self.botao_mascote = ctk.CTkButton(
            self.area_interativa,
            text="",
            image=self.mascote_normal,
            width=255,
            height=255,
            corner_radius=0,
            fg_color="transparent",
            hover_color=BG_DARK,
            border_width=0,
            command=self.alternar_menu,
        )

        self.botao_mascote.place(
            relx=0.5,
            rely=0.30,
            anchor="center",
        )

        self.botao_mascote.bind(
            "<Enter>",
            lambda evento: self.mascote_entrou(),
        )

        self.botao_mascote.bind(
            "<Leave>",
            lambda evento: self.mascote_saiu(),
        )

    def mascote_entrou(self):
        if self.mascote_hover is not None:
            self.botao_mascote.configure(
                image=self.mascote_hover
            )

    def mascote_saiu(self):
        if self.mascote_normal is not None:
            self.botao_mascote.configure(
                image=self.mascote_normal
            )

    # ========================================================
    # BOTÕES COM IMAGEM INTEIRA
    # ========================================================

    def criar_botao_imagem(
        self,
        imagem_normal,
        imagem_hover,
        comando,
    ):
        botao = ctk.CTkButton(
            self.area_interativa,
            text="",
            image=imagem_normal,
            width=145,
            height=145,
            corner_radius=0,
            fg_color="transparent",
            hover_color=BG_DARK,
            border_width=0,
            command=comando,
        )

        botao.bind(
            "<Enter>",
            lambda evento: botao.configure(
                image=imagem_hover
            ),
        )

        botao.bind(
            "<Leave>",
            lambda evento: botao.configure(
                image=imagem_normal
            ),
        )

        return botao

    def criar_botoes_menu(self):
        self.botao_ferramentas = self.criar_botao_imagem(
            self.ferramentas_normal,
            self.ferramentas_hover,
            self.abrir_ferramentas,
        )

        self.botao_servicos = self.criar_botao_imagem(
            self.servicos_normal,
            self.servicos_hover,
            self.abrir_servicos,
        )

        self.botao_configuracoes = self.criar_botao_imagem(
            self.configuracoes_normal,
            self.configuracoes_hover,
            self.abrir_configuracoes,
        )

        self.label_ferramentas = self.criar_nome_botao(
            "Ferramentas"
        )

        self.label_servicos = self.criar_nome_botao(
            "Serviços"
        )

        self.label_configuracoes = self.criar_nome_botao(
            "Configurações"
        )

        self.elementos_animados = {
            self.botao_ferramentas: {
                "origem": (0.5, 0.46),
                "destino": (0.28, 0.46),
            },
            self.label_ferramentas: {
                "origem": (0.5, 0.46),
                "destino": (0.28, 0.64),
            },

            self.botao_servicos: {
                "origem": (0.5, 0.46),
                "destino": (0.72, 0.46),
            },
            self.label_servicos: {
                "origem": (0.5, 0.46),
                "destino": (0.72, 0.64),
            },

            self.botao_configuracoes: {
                "origem": (0.5, 0.46),
                "destino": (0.5, 0.76),
            },
            self.label_configuracoes: {
                "origem": (0.5, 0.46),
                "destino": (0.5, 0.91),
            },
        }

        for elemento, dados in self.elementos_animados.items():
            origem_x, origem_y = dados["origem"]

            elemento.place(
                relx=origem_x,
                rely=origem_y,
                anchor="center",
            )

            elemento.lower()

        self.botao_mascote.lift()

    def criar_nome_botao(self, texto):
        return ctk.CTkLabel(
            self.area_interativa,
            text=texto,
            font=("Arial", 15, "bold"),
            text_color=TEXT_LIGHT,
            fg_color="transparent",
        )

    def criar_instrucao(self):
        self.instrucao = ctk.CTkLabel(
            self.area_interativa,
            text="Clique no mascote para abrir o menu",
            font=("Arial", 13),
            text_color=TEXT_SECONDARY,
        )
        self.instrucao.place(
            relx=0.5,
            rely=0.97,
            anchor="center",
        )

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
            text="Escolha uma opção ou clique novamente no mascote"
        )

        for elemento in self.elementos_animados:
            elemento.lift()

        self.botao_mascote.lift()

        total = 22 if self.settings_model.carregar().get("animacoes", True) else 1
        self.animar_elementos(
            abrindo=True,
            passo=0,
            total_passos=total,
        )

    def fechar_menu(self):
        self.menu_aberto = False
        self.animacao_em_execucao = True

        total = 22 if self.settings_model.carregar().get("animacoes", True) else 1
        self.animar_elementos(
            abrindo=False,
            passo=0,
            total_passos=total,
        )

    def animar_elementos(
        self,
        abrindo,
        passo,
        total_passos,
    ):
        progresso = passo / total_passos

        # Curva suave de aceleração e desaceleração.
        progresso_suave = (
            progresso
            * progresso
            * (3 - 2 * progresso)
        )

        for elemento, dados in self.elementos_animados.items():
            origem_x, origem_y = dados["origem"]
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

            elemento.place(
                relx=x,
                rely=y,
                anchor="center",
            )

        self.botao_mascote.lift()

        if passo < total_passos:
            self.after(
                16,
                lambda: self.animar_elementos(
                    abrindo,
                    passo + 1,
                    total_passos,
                ),
            )
            return

        self.animacao_em_execucao = False

        if not abrindo:
            for elemento in self.elementos_animados:
                elemento.lower()

            self.botao_mascote.lift()

            self.instrucao.configure(
                text="Clique no mascote para abrir o menu"
            )

    # ========================================================
    # AÇÕES DOS BOTÕES
    # ========================================================

    def abrir_ferramentas(self):
        ToolsView(self)
        """
        Essa area de abrir ferramentas são as mesmas dos serviços
        são padronizados com a função mostrar_mensagem usando os parametros comuns
        como Titulo, Mensagem
        onde todas as telas são iguais.       
        """

    def abrir_servicos(self):
        self.mostrar_mensagem(
            "Serviços",
            (
                "Nesta área serão disponibilizados histórico, "
                "relatórios, ajuda e jogos."
            ),
        )

    def abrir_configuracoes(self):
        ConfigView(self)

    def mostrar_mensagem(
        self,
        titulo,
        mensagem,
    ):
        janela = ctk.CTkToplevel(self)

        janela.title(titulo)
        janela.geometry("460x240")
        janela.resizable(False, False)
        janela.configure(fg_color=BG_DARK)
        janela.transient(self)
        janela.grab_set()

        titulo_label = ctk.CTkLabel(
            janela,
            text=titulo,
            font=("Arial", 23, "bold"),
            text_color=RED_MAIN,
        )
        titulo_label.pack(
            pady=(28, 15)
        )

        mensagem_label = ctk.CTkLabel(
            janela,
            text=mensagem,
            font=("Arial", 14),
            text_color=TEXT_LIGHT,
            wraplength=380,
            justify="center",
        )
        mensagem_label.pack(
            padx=30,
            pady=10,
        )

        fechar = ctk.CTkButton(
            janela,
            text="Fechar",
            width=140,
            height=36,
            fg_color=RED_MAIN,
            hover_color=self.cor_hover_tema,
            command=janela.destroy,
        )
        fechar.pack(
            pady=15
        )

    # ========================================================
    # ENCERRAMENTO
    # ========================================================

    def fechar_programa(self):
        self.janela_login.destroy()