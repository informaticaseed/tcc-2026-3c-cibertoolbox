from pathlib import Path


# ============================================================
# CAMINHOS DO PROJETO
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"

MASCOTE_DIR = IMAGES_DIR / "mascote"
ICONS_DIR = IMAGES_DIR / "icons"


# ============================================================
# IMAGENS
# ============================================================

MASCOTE_PRINCIPAL = MASCOTE_DIR / "mascote_principal.png"

ICON_FERRAMENTAS = ICONS_DIR / "ferramentas.png"
ICON_SERVICOS = ICONS_DIR / "servicos.png"
ICON_CONFIGURACOES = ICONS_DIR / "configuracoes.png"


# ============================================================
# CORES
# ============================================================

BG_DARK = "#090C10"
BG_SECONDARY = "#11151B"
BG_CARD = "#181D25"

BUTTON_DARK = "#171C24"
BUTTON_HOVER = "#222A35"

RED_MAIN = "#F23838"
RED_DARK = "#9E2424"
RED_GLOW = "#FF4B3E"

ORANGE_MAIN = "#FF781F"
ORANGE_LIGHT = "#FFA43A"
ORANGE_HOVER = "#D97512"
TEXT_LIGHT = "#F5F7FA"
TEXT_SECONDARY = "#9DA5B0"

GREEN_STATUS = "#2ED573"

BORDER_DARK = "#303640"

CARD_DARK = "#242424"
CARD_LIGHT = "#313131"
RED_HOVER = "#A83C3C"

TEXT_MUTED = "#B8B8B8"
