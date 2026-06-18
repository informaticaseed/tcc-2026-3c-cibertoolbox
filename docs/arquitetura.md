# Arquitetura do Sistema

**Grupo:** (nome do grupo)
**Última atualização:** (data)

---

## Diagrama de arquitetura

> Cole aqui o link da imagem, foto ou diagrama em texto.

```
Usuário
   ↓
[Tela HTML — templates/]
   ↓
[app.py — rotas Flask]
   ↓
[repositorio.py — acesso ao banco]
   ↓
[banco.db — SQLite]
```

---

## Separação de camadas

| Camada | Arquivo | Responsabilidade |
|--------|---------|-----------------|
| Web | `app.py` | Rotas e renderização |
| Dados | `repositorio.py` | Todo o SQL |
| Templates | `templates/` | HTML ao usuário |
| Testes | `tests/` | Testes automáticos |

---

## Decisões técnicas

Ver pasta `docs/decisoes/` para os registros de decisão (ADR).
