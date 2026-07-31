class Verification:

    def __init__(self):
        self.__user = "ADMIN"
        self.__senha = "admin"

    def checar_credenciais(self, usuario, senha):
        return (
            usuario == self.__user
            and senha == self.__senha
        )