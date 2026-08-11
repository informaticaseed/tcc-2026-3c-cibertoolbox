import base64
import os
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from src.Models.tool_result import ToolResult


class CryptoTool:
    MAGIC = b"CTB1"
    ITERACOES = 390_000

    def _chave(self, senha, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.ITERACOES,
        )
        return base64.urlsafe_b64encode(kdf.derive(senha.encode("utf-8")))

    def criptografar(self, caminho, senha):
        if not caminho:
            return ToolResult(False, "Selecione um arquivo.")
        if len(senha) < 8:
            return ToolResult(False, "Use uma senha com pelo menos 8 caracteres.")

        origem = Path(caminho)
        if not origem.is_file():
            return ToolResult(False, "Arquivo não encontrado.")

        try:
            dados = origem.read_bytes()
            salt = os.urandom(16)
            token = Fernet(self._chave(senha, salt)).encrypt(dados)
            destino = origem.with_name(origem.name + ".ctb")
            destino.write_bytes(self.MAGIC + salt + token)
            return ToolResult(True, "Arquivo criptografado com sucesso.", str(destino))
        except OSError as erro:
            return ToolResult(False, f"Falha ao acessar o arquivo: {erro}")

    def descriptografar(self, caminho, senha):
        if not caminho:
            return ToolResult(False, "Selecione um arquivo .ctb.")
        if not senha:
            return ToolResult(False, "Informe a senha usada na criptografia.")

        origem = Path(caminho)
        if not origem.is_file():
            return ToolResult(False, "Arquivo não encontrado.")

        try:
            conteudo = origem.read_bytes()
            if len(conteudo) < 20 or conteudo[:4] != self.MAGIC:
                return ToolResult(False, "Este arquivo não possui o formato CiberToolBox (.ctb).")
            salt = conteudo[4:20]
            token = conteudo[20:]
            dados = Fernet(self._chave(senha, salt)).decrypt(token)
            nome = origem.name[:-4] if origem.name.endswith(".ctb") else origem.name + ".dec"
            destino = origem.with_name(nome)
            if destino.exists():
                destino = origem.with_name(nome + ".decrypted")
            destino.write_bytes(dados)
            return ToolResult(True, "Arquivo descriptografado com sucesso.", str(destino))
        except InvalidToken:
            return ToolResult(False, "Senha incorreta ou arquivo alterado/corrompido.")
        except OSError as erro:
            return ToolResult(False, f"Falha ao acessar o arquivo: {erro}")
