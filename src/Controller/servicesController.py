
from src.Models.historymodel import HistoryModel


class ServicesController:
    """
    Coordena as funcionalidades disponíveis
    na área de Serviços.
    """

    def __init__(self):
        self.history_model = HistoryModel()

    # ========================================================
    # HISTÓRICO
    # ========================================================

    def listar_historico(self):
        return self.history_model.listar()

    def buscar_historico(self, texto):
        return self.history_model.buscar(texto)

    def limpar_historico(self):
        self.history_model.limpar()

    # ========================================================
    # REGISTRAR EXECUÇÃO
    # ========================================================

    def registrar_execucao(
        self,
        ferramenta,
        categoria,
        entrada,
        resultado,
    ):
        # Nunca registrar senha.
        if ferramenta == "Analisador de Senha":
            entrada = "[conteúdo não armazenado]"

        if ferramenta in (
            "Criptografar Arquivo",
            "Descriptografar Arquivo",
        ):
            # Aqui deverá chegar somente o caminho,
            # nunca a senha.
            entrada = entrada or "Arquivo não informado"

        return self.history_model.registrar(
            ferramenta=ferramenta,
            categoria=categoria,
            entrada=entrada,
            sucesso=resultado.sucesso,
            mensagem=resultado.mensagem,
        )