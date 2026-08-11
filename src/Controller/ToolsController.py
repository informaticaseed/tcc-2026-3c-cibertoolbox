from src.Models.tool_result import ToolResult
from src.Models.settings_model import SettingsModel
from src.Servicos.Ferramentas.Ping_tool import PingTool
from src.Servicos.Ferramentas.Dns_tool import DnsTool
from src.Servicos.Ferramentas.PortScan import PortScanTool
from src.Servicos.Ferramentas.Hash_tool import HashTool
from src.Servicos.Ferramentas.Password_tool import PasswordTool
from src.Servicos.Ferramentas.System_tool import SystemTool
from src.Servicos.Ferramentas.Report_tool import ReportTool
from src.Servicos.Ferramentas.Crypto_tool import CryptoTool
from src.Servicos.Ferramentas.Nmap_tool import NmapTool
from src.Servicos.Ferramentas.Vulnerability_tool import VulnerabilityTool
from src.Servicos.Ferramentas.Scapy_tool import ScapyTool


class ToolsController:
    """Coordena as solicitações da View e delega a lógica aos serviços."""

    def __init__(self):
        self.ping_tool = PingTool()
        self.dns_tool = DnsTool()
        self.port_tool = PortScanTool()
        self.hash_tool = HashTool()
        self.password_tool = PasswordTool()
        self.system_tool = SystemTool()
        self.report_tool = ReportTool()
        self.crypto_tool = CryptoTool()
        self.nmap_tool = NmapTool()
        self.vulnerability_tool = VulnerabilityTool()
        self.scapy_tool = ScapyTool()
        self.settings_model = SettingsModel()

    def executar_ping(self, host, parametros=""):
        host = host.strip()
        if not host:
            return ToolResult(False, "Informe um host ou endereço IP.")
        return self.ping_tool.executar(host, parametros)

    def executar_dns(self, host):
        host = host.strip()
        if not host:
            return ToolResult(False, "Informe um domínio.")
        return self.dns_tool.executar(host)

    def executar_port_scan(self, host, porta_inicial, porta_final):
        host = host.strip()
        if not host:
            return ToolResult(False, "Informe um host ou endereço IP.")
        try:
            inicio, fim = int(porta_inicial), int(porta_final)
        except ValueError:
            return ToolResult(False, "As portas devem ser números inteiros.")
        if not (1 <= inicio <= 65535 and 1 <= fim <= 65535):
            return ToolResult(False, "As portas devem estar entre 1 e 65535.")
        if inicio > fim:
            return ToolResult(False, "A porta inicial não pode ser maior que a final.")
        cfg = self.settings_model.carregar()
        return self.port_tool.executar(
            host, inicio, fim,
            limite=int(cfg.get("max_portas_scan", 128)),
            timeout=float(cfg.get("timeout_porta", 0.25)),
        )

    def hash_texto(self, texto, algoritmo):
        if not texto:
            return ToolResult(False, "Digite algum texto para calcular o hash.")
        return self.hash_tool.texto(texto, algoritmo)

    def hash_arquivo(self, caminho, algoritmo):
        return self.hash_tool.arquivo(caminho, algoritmo)

    def comparar_hashes(self, hash_1, hash_2):
        if not hash_1.strip() or not hash_2.strip():
            return ToolResult(False, "Informe os dois hashes para comparar.")
        return self.hash_tool.comparar(hash_1, hash_2)

    def analisar_senha(self, senha):
        if not senha:
            return ToolResult(False, "Digite uma senha para analisar.")
        return self.password_tool.analisar(senha)

    def informacoes_sistema(self):
        return self.system_tool.executar()

    def gerar_relatorio(self, titulo, observacoes):
        return self.report_tool.gerar(titulo, observacoes)

    def criptografar_arquivo(self, caminho, senha):
        return self.crypto_tool.criptografar(caminho, senha)

    def descriptografar_arquivo(self, caminho, senha):
        return self.crypto_tool.descriptografar(caminho, senha)

    def executar_nmap(self, alvo, parametros=""):
        return self.nmap_tool.executar(alvo, parametros)

    def analisar_vulnerabilidade_web(self, endereco):
        return self.vulnerability_tool.analisar(endereco)

    def executar_scapy(self, alvo):
        return self.scapy_tool.executar(alvo)
