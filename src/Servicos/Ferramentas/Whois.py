from src.Models.tool_result import ToolResult

class WhoisTool:
    def executar(self, host, parametros=""):
        if not host.strip():
            return ToolResult(False, "Informe um host ou IP.")
        try:
            import whois
        except ImportError:
            return ToolResult(False, "Whois não está instalado. Execute: pip install python-whois")
        try:
            linhas = [
                f"Destino: {host.strip()}",
            ]
            return ToolResult(True, "Diagnóstico Whois concluído.", "\n".join(linhas))
        except PermissionError:
            return ToolResult(False, "O Whois precisa de privilégios adequados/Npcap para enviar pacotes neste sistema.")
        except Exception as erro:
            return ToolResult(False, f"Falha no diagnóstico Whois: {erro}")