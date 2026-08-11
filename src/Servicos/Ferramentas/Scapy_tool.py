from src.Models.tool_result import ToolResult


class ScapyTool:
    """Diagnóstico ICMP simples com Scapy."""

    def executar(self, alvo):
        if not alvo.strip():
            return ToolResult(False, "Informe um host ou IP.")
        try:
            from scapy.all import ICMP, IP, sr1
        except ImportError:
            return ToolResult(False, "Scapy não está instalado. Execute: pip install scapy")

        try:
            pacote = IP(dst=alvo.strip()) / ICMP()
            resposta = sr1(pacote, timeout=3, verbose=False)
            if resposta is None:
                return ToolResult(False, "Nenhuma resposta ICMP recebida.")
            linhas = [
                f"Destino: {alvo.strip()}",
                f"Resumo: {resposta.summary()}",
                f"Origem da resposta: {resposta.src if hasattr(resposta, 'src') else 'N/D'}",
                f"TTL: {resposta.ttl if hasattr(resposta, 'ttl') else 'N/D'}",
            ]
            return ToolResult(True, "Diagnóstico Scapy concluído.", "\n".join(linhas))
        except PermissionError:
            return ToolResult(False, "O Scapy precisa de privilégios adequados/Npcap para enviar pacotes neste sistema.")
        except Exception as erro:
            return ToolResult(False, f"Falha no diagnóstico Scapy: {erro}")
