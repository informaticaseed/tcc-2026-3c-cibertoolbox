import platform
import shlex
import subprocess
from src.Models.tool_result import ToolResult


class PingTool:
    """Ping com parâmetros extras controlados, sem usar shell=True."""

    WINDOWS_FLAGS = {"-t", "-a", "-4", "-6", "-f"}
    WINDOWS_VALUE_FLAGS = {"-n", "-l", "-w", "-i"}
    UNIX_FLAGS = {"-4", "-6", "-n"}
    UNIX_VALUE_FLAGS = {"-c", "-s", "-W", "-i"}

    def _validar_parametros(self, parametros):
        if not parametros.strip():
            return []

        try:
            tokens = shlex.split(parametros, posix=False)
        except ValueError as erro:
            raise ValueError(f"Parâmetros inválidos: {erro}")

        windows = platform.system() == "Windows"
        flags = self.WINDOWS_FLAGS if windows else self.UNIX_FLAGS
        value_flags = self.WINDOWS_VALUE_FLAGS if windows else self.UNIX_VALUE_FLAGS
        resultado = []
        i = 0

        while i < len(tokens):
            token = tokens[i]
            if token in flags:
                resultado.append(token)
                i += 1
                continue
            if token in value_flags:
                if i + 1 >= len(tokens):
                    raise ValueError(f"O parâmetro {token} precisa de um valor.")
                valor = tokens[i + 1]
                # Apenas números para parâmetros de contagem/tamanho/tempo/TTL.
                if not valor.isdigit():
                    raise ValueError(f"O valor de {token} deve ser numérico.")
                resultado.extend([token, valor])
                i += 2
                continue
            raise ValueError(
                f"Parâmetro não permitido: {token}. Use somente opções básicas de diagnóstico."
            )
        return resultado

    def executar(self, host, parametros=""):
        try:
            extras = self._validar_parametros(parametros)
        except ValueError as erro:
            return ToolResult(False, str(erro))

        windows = platform.system() == "Windows"
        # Se o usuário não informou contagem nem -t, usamos 4 pacotes por padrão.
        if windows:
            tem_contagem = "-n" in extras or "-t" in extras
            padrao = [] if tem_contagem else ["-n", "4"]
        else:
            tem_contagem = "-c" in extras
            padrao = [] if tem_contagem else ["-c", "4"]

        comando = ["ping", *padrao, *extras, host]

        try:
            resultado = subprocess.run(
                comando,
                capture_output=True,
                text=True,
                timeout=12,
                encoding=None,
                errors="replace",
                shell=False,
            )
            saida = (resultado.stdout or resultado.stderr or "Sem saída.").strip()
            return ToolResult(
                sucesso=resultado.returncode == 0,
                mensagem="Ping concluído." if resultado.returncode == 0 else "O host não respondeu ao Ping.",
                saida=saida,
            )
        except subprocess.TimeoutExpired as erro:
            parcial = erro.stdout or erro.stderr or ""
            if isinstance(parcial, bytes):
                parcial = parcial.decode(errors="replace")
            return ToolResult(
                True,
                "Ping interrompido após 12 segundos para não prender a interface.",
                (parcial or "Comando contínuo executado até o limite de segurança.").strip(),
            )
        except OSError as erro:
            return ToolResult(False, f"Não foi possível executar o comando Ping: {erro}")
