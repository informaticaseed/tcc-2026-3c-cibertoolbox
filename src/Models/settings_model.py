import json
from pathlib import Path


class SettingsModel:
    """
    Persistência simples das preferências
    do CiberToolBox em arquivo JSON.
    """

    DEFAULTS = {
        "escala_interface": 1.0,
        "animacoes": True,
        "abrir_maximizado": True,

        # Configurações das ferramentas
        "max_portas_scan": 128,
        "timeout_porta": 0.25,

        # Aparência
        "cor_destaque": "Vermelho",
        "tema_fundo": "Escuro",
    }

    # ========================================================
    # INICIALIZAÇÃO
    # ========================================================

    def __init__(self):
        self.arquivo = (
            Path(__file__).resolve().parents[2]
            / "data"
            / "settings.json"
        )

        self.arquivo.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    # ========================================================
    # CARREGAR
    # ========================================================

    def carregar(self):
        """
        Carrega as configurações salvas.

        Caso o arquivo ainda não exista ou esteja inválido,
        utiliza os valores padrão.
        """

        dados = self.DEFAULTS.copy()

        if self.arquivo.exists():
            try:
                salvo = json.loads(
                    self.arquivo.read_text(
                        encoding="utf-8"
                    )
                )

                if isinstance(salvo, dict):
                    dados.update(salvo)

            except (
                OSError,
                json.JSONDecodeError,
            ):
                pass

        return dados

    # ========================================================
    # SALVAR
    # ========================================================

    def salvar(self, dados):
        """
        Salva as configurações no arquivo settings.json.
        """

        novo = self.DEFAULTS.copy()

        novo.update(dados)

        self.arquivo.write_text(
            json.dumps(
                novo,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return novo

    # ========================================================
    # RESTAURAR
    # ========================================================

    def restaurar_padrao(self):
        """
        Restaura todas as configurações padrão.
        """

        return self.salvar(
            self.DEFAULTS.copy()
        )

    # ========================================================
    # TEMA
    # ========================================================

    def obter_tema(self):
        """
        Converte as preferências de aparência
        em cores que podem ser usadas pelas Views.
        """

        dados = self.carregar()

        # ----------------------------------------------------
        # CORES PRINCIPAIS
        # ----------------------------------------------------

        cores_destaque = {
            "Vermelho": "#F23838",
            "Laranja": "#FF781F",
            "Azul": "#3498DB",
            "Verde": "#2ED573",
            "Roxo": "#9B59B6",
        }

        # ----------------------------------------------------
        # CORES DE HOVER
        # ----------------------------------------------------

        cores_hover = {
            "Vermelho": "#A92525",
            "Laranja": "#C95E10",
            "Azul": "#2471A3",
            "Verde": "#1E9E56",
            "Roxo": "#71368A",
        }

        # ----------------------------------------------------
        # TEMAS DE FUNDO
        # ----------------------------------------------------

        temas_fundo = {
            "Escuro": {
                "bg": "#090C10",
                "secundario": "#11151B",
                "card": "#181D25",
                "painel": "#0F1319",
                "card_hover": "#222A35",
                "border": "#303640",
            },

            "Preto": {
                "bg": "#000000",
                "secundario": "#090909",
                "card": "#121212",
                "painel": "#080808",
                "card_hover": "#202020",
                "border": "#292929",
            },

            "Cinza": {
                "bg": "#16181C",
                "secundario": "#202329",
                "card": "#292D34",
                "painel": "#1D2025",
                "card_hover": "#343941",
                "border": "#3B414B",
            },
        }

        # ----------------------------------------------------
        # CONFIGURAÇÕES ESCOLHIDAS PELO USUÁRIO
        # ----------------------------------------------------

        nome_cor = dados.get(
            "cor_destaque",
            "Vermelho"
        )

        nome_fundo = dados.get(
            "tema_fundo",
            "Escuro"
        )

        fundo = temas_fundo.get(
            nome_fundo,
            temas_fundo["Escuro"]
        )

        # ----------------------------------------------------
        # RETORNO PADRONIZADO
        # ----------------------------------------------------

        return {
            "destaque": cores_destaque.get(
                nome_cor,
                "#F23838"
            ),

            "hover": cores_hover.get(
                nome_cor,
                "#A92525"
            ),

            "bg": fundo["bg"],

            "secundario":
                fundo["secundario"],

            "card":
                fundo["card"],

            "painel":
                fundo["painel"],

            "card_hover":
                fundo["card_hover"],

            "border":
                fundo["border"],

            "texto":
                "#F5F7FA",

            "texto_secundario":
                "#9DA5B0",

            "verde":
                "#2ED573",

            "amarelo":
                "#F1C40F",
        }