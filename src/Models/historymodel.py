from src.Database.database import Database


class HistoryModel:
    """
    Responsável pelos dados do histórico
    das ferramentas.
    """

    def __init__(self):
        self.database = Database()

    # ========================================================
    # REGISTRAR
    # ========================================================

    def registrar(
        self,
        ferramenta,
        categoria,
        entrada,
        sucesso,
        mensagem,
    ):
        with self.database.conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute(
                """
                INSERT INTO historico_ferramentas (
                    ferramenta,
                    categoria,
                    entrada,
                    sucesso,
                    mensagem
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    ferramenta,
                    categoria,
                    entrada,
                    1 if sucesso else 0,
                    mensagem,
                ),
            )

            conexao.commit()

            return cursor.lastrowid

    # ========================================================
    # LISTAR
    # ========================================================

    def listar(self, limite=100):
        with self.database.conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    ferramenta,
                    categoria,
                    entrada,
                    sucesso,
                    mensagem,
                    criado_em
                FROM historico_ferramentas
                ORDER BY id DESC
                LIMIT ?
                """,
                (limite,),
            )

            return [
                dict(linha)
                for linha in cursor.fetchall()
            ]

    # ========================================================
    # BUSCAR
    # ========================================================

    def buscar(self, texto):
        texto = texto.strip()

        if not texto:
            return self.listar()

        termo = f"%{texto}%"

        with self.database.conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    ferramenta,
                    categoria,
                    entrada,
                    sucesso,
                    mensagem,
                    criado_em
                FROM historico_ferramentas
                WHERE
                    ferramenta LIKE ?
                    OR categoria LIKE ?
                    OR entrada LIKE ?
                ORDER BY id DESC
                """,
                (
                    termo,
                    termo,
                    termo,
                ),
            )

            return [
                dict(linha)
                for linha in cursor.fetchall()
            ]

    # ========================================================
    # APAGAR HISTÓRICO
    # ========================================================

    def limpar(self):
        with self.database.conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute(
                """
                DELETE FROM historico_ferramentas
                """
            )

            conexao.commit()