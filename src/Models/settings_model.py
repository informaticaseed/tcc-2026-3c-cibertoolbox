import json
from pathlib import Path


class SettingsModel:
    """Persistência simples das preferências do CiberToolBox em JSON."""

    DEFAULTS = {
        "escala_interface": 1.0,
        "animacoes": True,
        "abrir_maximizado": True,
        "max_portas_scan": 128,
        "timeout_porta": 0.25,
        "color_settings": None
    }

    def __init__(self):
        self.arquivo = Path(__file__).resolve().parents[2] / "data" / "settings.json"
        self.arquivo.parent.mkdir(parents=True, exist_ok=True)

    def carregar(self):
        dados = self.DEFAULTS.copy()
        if self.arquivo.exists():
            try:
                salvo = json.loads(self.arquivo.read_text(encoding="utf-8"))
                if isinstance(salvo, dict):
                    dados.update(salvo)
            except (OSError, json.JSONDecodeError):
                pass
        return dados

    def salvar(self, dados):
        novo = self.DEFAULTS.copy()
        novo.update(dados)
        self.arquivo.write_text(
            json.dumps(novo, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )
        return novo

    def restaurar_padrao(self):
        return self.salvar(self.DEFAULTS.copy())
