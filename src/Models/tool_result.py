from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolResult:
    sucesso: bool
    mensagem: str
    saida: str = ""
    dados: dict[str, Any] = field(default_factory=dict)
