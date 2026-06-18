# Guia do Aluno — Como trabalhar toda semana

**LTP3 + QP3 · CEMIC 2026**

---

## O que você faz toda semana (resumo rápido)

```
Segunda → Abra Issues da semana
Durante → Trabalhe e faça commits
Sexta   → Abra 1 Pull Request linkando as Issues
```

---

## Passo 1 — Abrir Issues no início da semana

1. Acesse o seu repositório no GitHub
2. Clique em **Issues → New issue**
3. Escolha o template **"Tarefa Semanal"**
4. Preencha todos os campos
5. Clique em **Submit new issue**

> Cada integrante deve abrir pelo menos 1 Issue por semana.
> A Issue é a prova de que você planejou o seu trabalho.

---

## Passo 2 — Trabalhe e faça commits

```bash
git add .
git commit -m "descrição do que você fez"
git push
```

> Cada integrante deve fazer pelo menos 1 commit por semana.
> O professor vê automaticamente quem commitou na aba Actions.

---

## Passo 3 — Abrir o Pull Request na sexta

1. Acesse o repositório → **Pull requests → New pull request**
2. Base: `main` ← Compare: sua branch de trabalho
3. O template de PR aparece automaticamente — **preencha todos os campos**
4. Para linkar com as Issues, escreva no corpo do PR:
   ```
   Closes #12
   Closes #15
   Closes #17
   ```
5. Clique em **Create pull request**

> "Closes #N" faz a Issue fechar automaticamente quando o PR for aprovado.

---

## Como registrar um impedimento

Se o grupo travou em algo:

1. Issues → New issue → template **"Impedimento"**
2. Preencha o que está bloqueando e o que já tentaram
3. O professor recebe o alerta no painel dele

---

## O que o professor avalia toda semana

| Critério | Como evidenciar |
|----------|----------------|
| Planejou | Issues abertas com template preenchido |
| Trabalhou | Commits no histórico |
| Entregou | PR semanal aberto e linkado às Issues |
| Colaborou | Commits de todos os integrantes |
| Comunicou impedimentos | Issue de impedimento aberta |

---

## Dicas importantes

- **Não espere a sexta para fazer o primeiro commit** — distribua ao longo da semana
- **PR sem Issue linkada = entrega incompleta** — sempre use `Closes #N`
- **Issue sem responsável = ninguém sabe de quem é** — sempre preencha o campo "Responsável"
- **O professor vê tudo automaticamente** — não precisa mandar mensagem no WhatsApp dizendo que entregou
