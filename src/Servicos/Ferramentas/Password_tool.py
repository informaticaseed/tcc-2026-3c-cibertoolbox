import re
from src.Models.tool_result import ToolResult


class PasswordTool:
    def analisar(self, senha):
        criterios = {
            "12 ou mais caracteres": len(senha) >= 12,
            "letra minúscula": bool(re.search(r"[a-z]", senha)),
            "letra maiúscula": bool(re.search(r"[A-Z]", senha)),
            "número": bool(re.search(r"\d", senha)),
            "caractere especial": bool(re.search(r"[^A-Za-z0-9]", senha)),
        }
        comuns = {"123456", "password", "senha", "admin", "qwerty", "12345678"}
        previsivel = senha.lower() in comuns or bool(re.search(r"(1234|abcd|qwerty)", senha.lower()))
        pontos = sum(criterios.values()) - (1 if previsivel else 0)
        pontos = max(0, pontos)
        if pontos <= 2:
            nivel = "Fraca"
        elif pontos <= 4:
            nivel = "Média"
        else:
            nivel = "Forte"

        linhas = [f"Classificação: {nivel}", "", "Critérios:"]
        for nome, ok in criterios.items():
            linhas.append(f"  {'OK' if ok else 'FALTA'} - {nome}")
        if previsivel:
            linhas.append("\nALERTA - A senha contém um padrão previsível ou muito comum.")
        linhas.append("\nA senha analisada não é armazenada pelo CiberToolBox.")
        return ToolResult(True, f"Senha classificada como {nivel}.", "\n".join(linhas), {"nivel": nivel, "pontos": pontos})
