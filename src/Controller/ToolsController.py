# class ToolsController:

#     def __init__(self, ping_tool):
#         self.ping_tool = ping_tool

#     def executar_ping(self, host):
#         if not host:
#             return {
#                 "sucesso": False,
#                 "mensagem": "Informe um host."
#             }

#         return self.ping_tool.executar(host)