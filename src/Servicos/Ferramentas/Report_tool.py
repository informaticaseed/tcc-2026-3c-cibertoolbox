from datetime import datetime
from src.Models.tool_result import ToolResult


class ReportTool:
    def gerar(self, titulo, observacoes):
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        titulo = titulo.strip() or "Relatório CiberToolBox"
        linhas = [
            "CIBERTOOLBOX - RELATÓRIO",
            "=" * 50,
            f"Título: {titulo}",
            f"Gerado em: {agora}",
            "=" * 50,
            "",
            "Observações:",
            observacoes.strip() or "Sem observações.",
            "",
            "Aviso: este relatório não deve conter senhas ou credenciais sensíveis.",
        ]
        texto = "\n".join(linhas) + "\n"
        return ToolResult(True, "Relatório preparado para exportação.", texto)
