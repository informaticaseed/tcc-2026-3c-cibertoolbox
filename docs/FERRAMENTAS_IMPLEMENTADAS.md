# Ferramentas implementadas nesta versão

- Ping com parâmetros básicos validados.
- Consulta DNS.
- Scanner TCP controlado.
- Nmap com opções de inventário/diagnóstico permitidas.
- Scapy: diagnóstico ICMP simples.
- Análise Web passiva: cabeçalhos HTTP de segurança e TLS.
- Hash de texto e arquivo.
- Comparação de hashes.
- Criptografia de arquivos com senha (`.ctb`).
- Descriptografia de arquivos `.ctb`.
- Analisador de senha.
- Informações do sistema.
- Gerador de relatório.

## Dependências

As bibliotecas Python ficam em `requirements.txt`.

O Nmap é um programa externo e precisa estar instalado no sistema e disponível no PATH. Em Windows, o Scapy pode precisar do Npcap e de privilégios adequados para envio de pacotes.

## Uso responsável

Ferramentas de rede e auditoria devem ser usadas em máquinas próprias, laboratórios ou ambientes com autorização expressa. A versão do Nmap bloqueia scripts NSE, spoofing e opções evasivas para manter o escopo defensivo/educacional do projeto.
