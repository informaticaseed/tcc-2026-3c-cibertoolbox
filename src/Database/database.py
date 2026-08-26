import sqlite3
from pathlib import Path


class Database:
    """
    Responsável pela conexão e criação inicial
    do banco SQLite do CiberToolBox.
    """

    def __init__(self):
        self.caminho_banco = (
            Path(__file__).resolve().parents[2]
            / "data"
            / "cibertoolbox.db"
        )

        self.caminho_banco.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.criar_tabelas()

    def conectar(self):
        conexao = sqlite3.connect(
            self.caminho_banco
        )

        conexao.row_factory = sqlite3.Row

        return conexao

    def criar_tabelas(self):
        with self.conectar() as conexao:
            cursor = conexao.cursor()

            # ================================================
            # USUÁRIOS
            # ================================================

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT NOT NULL UNIQUE,
                    senha_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    ativo INTEGER NOT NULL DEFAULT 1
                )
                """
            )

            # ================================================
            # HISTÓRICO
            # ================================================

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS historico_ferramentas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    ferramenta TEXT NOT NULL,

                    categoria TEXT,

                    entrada TEXT,

                    sucesso INTEGER NOT NULL,

                    mensagem TEXT,

                    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            conexao.commit()