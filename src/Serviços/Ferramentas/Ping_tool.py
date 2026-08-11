import platform
import subprocess
from src.Models.tool_result import ToolResult


class PingTool:
    def executar(self, host):
        parametro = "-n" if platform.system() == "Windows" else "-c"
        comando = ["ping", parametro, "4", host]
        try:
            resultado = subprocess.run(
                comando, capture_output=True, text=True, timeout=15,
                encoding=None, errors="replace"
            )
            saida = (resultado.stdout or resultado.stderr or "Sem saída.").strip()
            return ToolResult(
                sucesso=resultado.returncode == 0,
                mensagem="Ping concluído." if resultado.returncode == 0 else "O host não respondeu ao Ping.",
                saida=saida,
            )
        except subprocess.TimeoutExpired:
            return ToolResult(False, "Tempo limite do Ping excedido.")
        except OSError as erro:
            return ToolResult(False, f"Não foi possível executar o comando Ping: {erro}")
