# import platform
# import subprocess


# class PingTool:

#     def executar(self, host):
#         parametro = "-n" if platform.system() == "Windows" else "-c"

#         comando = [
#             "ping",
#             parametro,
#             "4",
#             host
#         ]

#         try:
#             resultado = subprocess.run(
#                 comando,
#                 capture_output=True,
#                 text=True,
#                 timeout=15
#             )

#             return {
#                 "sucesso": resultado.returncode == 0,
#                 "saida": resultado.stdout or resultado.stderr
#             }

#         except subprocess.TimeoutExpired:
#             return {
#                 "sucesso": False,
#                 "saida": "Tempo limite excedido."
#             }

#         except OSError as erro:
#             return {
#                 "sucesso": False,
#                 "saida": f"Erro ao executar Ping: {erro}"
#             }