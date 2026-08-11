import socket
from src.Models.tool_result import ToolResult


class DnsTool:
    def executar(self, host):
        try:
            nome, aliases, ips = socket.gethostbyname_ex(host)
            saida = [f"Host consultado: {host}", f"Nome canônico: {nome}"]
            if aliases:
                saida.append("Aliases: " + ", ".join(aliases))
            saida.append("Endereços IP:")
            saida.extend(f"  - {ip}" for ip in ips)
            return ToolResult(True, "Consulta DNS concluída.", "\n".join(saida), {"ips": ips})
        except socket.gaierror as erro:
            return ToolResult(False, f"Não foi possível resolver o domínio: {erro}")
