import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.Models.tool_result import ToolResult


class PortScanTool:
    def _testar_porta(self, host, porta, timeout):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            return porta if sock.connect_ex((host, porta)) == 0 else None

    def executar(self, host, porta_inicial, porta_final, limite=128, timeout=0.25):
        quantidade = porta_final - porta_inicial + 1
        if quantidade > limite:
            return ToolResult(False, f"Intervalo muito grande. O limite atual é {limite} portas.")

        portas = range(porta_inicial, porta_final + 1)
        abertas = []
        try:
            with ThreadPoolExecutor(max_workers=min(32, quantidade)) as executor:
                futuros = [executor.submit(self._testar_porta, host, p, timeout) for p in portas]
                for futuro in as_completed(futuros):
                    porta = futuro.result()
                    if porta is not None:
                        abertas.append(porta)
            abertas.sort()
            if abertas:
                saida = "Portas TCP abertas:\n" + "\n".join(f"  - {p}" for p in abertas)
            else:
                saida = "Nenhuma porta aberta foi encontrada no intervalo informado."
            return ToolResult(True, "Varredura concluída.", saida, {"portas_abertas": abertas})
        except socket.gaierror as erro:
            return ToolResult(False, f"Host inválido ou não resolvido: {erro}")
        except OSError as erro:
            return ToolResult(False, f"Erro de rede durante a varredura: {erro}")
