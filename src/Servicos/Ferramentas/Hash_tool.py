import hashlib
from pathlib import Path
from src.Models.tool_result import ToolResult


class HashTool:
    ALGORITMOS = {"SHA-256": "sha256", "SHA-512": "sha512"}

    def _novo_hash(self, algoritmo):
        nome = self.ALGORITMOS.get(algoritmo, "sha256")
        return hashlib.new(nome)

    def texto(self, texto, algoritmo="SHA-256"):
        h = self._novo_hash(algoritmo)
        h.update(texto.encode("utf-8"))
        valor = h.hexdigest()
        return ToolResult(True, f"{algoritmo} calculado.", valor, {"hash": valor})

    def arquivo(self, caminho, algoritmo="SHA-256"):
        arquivo = Path(caminho)
        if not arquivo.is_file():
            return ToolResult(False, "Selecione um arquivo válido.")
        h = self._novo_hash(algoritmo)
        try:
            with arquivo.open("rb") as f:
                for bloco in iter(lambda: f.read(1024 * 1024), b""):
                    h.update(bloco)
            valor = h.hexdigest()
            saida = f"Arquivo: {arquivo.name}\nAlgoritmo: {algoritmo}\nHash: {valor}"
            return ToolResult(True, "Hash do arquivo calculado.", saida, {"hash": valor})
        except OSError as erro:
            return ToolResult(False, f"Não foi possível ler o arquivo: {erro}")

    def comparar(self, hash_1, hash_2):
        iguais = hash_1.strip().lower() == hash_2.strip().lower() and bool(hash_1.strip())
        return ToolResult(
            True,
            "Os hashes são iguais." if iguais else "Os hashes são diferentes.",
            "Integridade compatível." if iguais else "Os valores informados não correspondem.",
            {"iguais": iguais},
        )
