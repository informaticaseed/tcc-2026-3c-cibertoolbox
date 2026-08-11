import os
import platform
import socket
from src.Models.tool_result import ToolResult


class SystemTool:
    def executar(self):
        dados = {
            "Sistema": platform.system(),
            "Versão": platform.version(),
            "Release": platform.release(),
            "Arquitetura": platform.machine(),
            "Processador": platform.processor() or "Não informado",
            "Nome da máquina": socket.gethostname(),
            "Python": platform.python_version(),
            "Usuário": os.environ.get("USERNAME") or os.environ.get("USER") or "Não informado",
        }
        saida = "\n".join(f"{chave}: {valor}" for chave, valor in dados.items())
        return ToolResult(True, "Informações do sistema coletadas.", saida, dados)
