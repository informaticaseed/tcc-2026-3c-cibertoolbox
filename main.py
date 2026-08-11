# main.py
import sys
import subprocess
import os

def verificar_e_instalar_requisitos():
    caminho_requirements = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if not os.path.exists(caminho_requirements):
        return

    with open(caminho_requirements, "r", encoding="utf-8") as f:
        requisitos = [linha.strip() for ip, linha in enumerate(f) if linha.strip() and not linha.startswith("#")]
    pacotes_ausentes = []
    for requisito in requisitos:
        nome_pacote = requisito.split("==")[0].split(">=")[0].strip()
        mapa_importacao = {
            "pillow": "PIL",
            "customtkinter": "customtkinter",
        }
        nome_import = mapa_importacao.get(nome_pacote.lower(), nome_pacote.lower().replace("-", "_"))
        try:
            __import__(nome_import)
        except ImportError:
            pacotes_ausentes.append(requisito)

    if pacotes_ausentes:
        print("=" * 60)
        print("DEPENDÊNCIAS DO REQUIREMENTS.TXT AUSENTES!")
        print(f"Instalando: {', '.join(pacotes_ausentes)}")
        print("Por favor, aguarde...")
        print("=" * 60)
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", caminho_requirements])
            print("\nTodos os requisitos do sistema foram instalados!\n")
        except subprocess.CalledProcessError as e:
            print(f"\nErro ao tentar instalar pelo requirements.txt: {e}")
            sys.exit(1)

verificar_e_instalar_requisitos()
from src import iniciar_programa

if __name__ == "__main__":
    iniciar_programa()
