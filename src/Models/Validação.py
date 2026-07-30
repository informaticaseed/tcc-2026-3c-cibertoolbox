class Verification:
    def __init__(self):
        # Dados do "banco de dados" ou mockados
        self.__user__ = "ADMIN"
        self.__senha__ = "ADMIN"

    def checar_credenciais(self, usuario, senha):
        # Lógica pura de validação
        if usuario == self.__user__ and senha == self.__senha__:
            return True
        return False