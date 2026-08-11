import shlex
import shutil
import subprocess
from src.Models.tool_result import ToolResult


class NmapTool:
    """Wrapper educacional do Nmap com opções limitadas a inventário/diagnóstico."""

    FLAGS = {"-Pn", "-n", "-sV", "--version-light", "-F", "-T2", "-T3", "-T4", "-6"}
    VALUE_FLAGS = {"-p", "--top-ports"}

    def _validar(self, parametros):
        try:
            tokens = shlex.split(parametros or "", posix=False)
        except ValueError as erro:
            raise ValueError(f"Parâmetros inválidos: {erro}")

        saida = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token in self.FLAGS:
                saida.append(token)
                i += 1
                continue
            if token in self.VALUE_FLAGS:
                if i + 1 >= len(tokens):
                    raise ValueError(f"{token} precisa de um valor.")
                valor = tokens[i + 1]
                # Porta(s): números, vírgula e hífen. top-ports: apenas número.
                if token == "--top-ports" and not valor.isdigit():
                    raise ValueError("--top-ports aceita apenas um número.")
                if token == "-p" and any(c not in "0123456789,-" for c in valor):
                    raise ValueError("-p aceita somente portas numéricas, vírgulas e intervalos.")
                saida.extend([token, valor])
                i += 2
                continue
            raise ValueError(
                f"Opção Nmap não permitida: {token}. Scripts NSE, spoofing e técnicas evasivas não são habilitados neste protótipo."
            )
        return saida

    def executar(self, alvo, parametros=""):
        if not alvo.strip():
            return ToolResult(False, "Informe um host ou IP.")
        executavel = shutil.which("nmap")
        if not executavel:
            return ToolResult(False, "Nmap não foi encontrado no PATH. Instale o Nmap no Windows e reinicie o CiberToolBox.")
        try:
            extras = self._validar(parametros)
        except ValueError as erro:
            return ToolResult(False, str(erro))

        if not extras:
            extras = ["-T3", "--top-ports", "20"]
        try:
            processo = subprocess.run(
                [executavel, *extras, alvo.strip()],
                capture_output=True,
                text=True,
                timeout=60,
                errors="replace",
                shell=False,
            )
            saida = (processo.stdout or processo.stderr or "Sem saída.").strip()
            return ToolResult(processo.returncode == 0, "Nmap concluído." if processo.returncode == 0 else "Nmap retornou um erro.", saida)
        except subprocess.TimeoutExpired:
            return ToolResult(False, "A execução do Nmap excedeu 60 segundos.")
        except OSError as erro:
            return ToolResult(False, f"Não foi possível executar o Nmap: {erro}")
