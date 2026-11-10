# Pesquisa pública sem depender do PC

Este monitor consulta três buscas públicas do 99Freelas e até seis páginas de anúncios por execução, alternando dados/planilhas e sites/páginas. Salva títulos, links e contagem pública de propostas em Markdown e JSON. Usa somente a biblioteca padrão do Python; não usa API de IA, login, credenciais pessoais ou assinatura.

Não envia propostas, mensagens ou candidaturas, não recebe pagamentos, não pesquisa e-mails e não atua como agente de IA permanente. Resultado de filtro não confirma contratação, gratuidade de todos os custos do projeto ou elegibilidade. Estrutura e disponibilidade das páginas podem mudar. Uma falha total termina com código diferente de zero, e falhas parciais ficam no relatório. Os resultados precisam ser lidos por Du ou em uma próxima tarefa Codex para preparar as propostas.

## Local

```bash
python3 automacao/buscar.py --saida relatorios
```

## GitHub

O workflow `.github/workflows/oportunidades.yml` pode executar ao publicar alterações no monitor na branch main, manualmente e diariamente às 12:17 UTC (09:17 em São Paulo). Horários do GitHub podem atrasar; não é serviço com disponibilidade garantida. O agendamento depende de Actions habilitado, workflow na branch padrão e regras do GitHub. Repositórios públicos inativos podem ter schedules desabilitados pelo GitHub.

A execução foi limitada a repositórios com visibilidade public e ao runner padrão ubuntu-latest, para não usar minutos pagos de repositórios privados. Actions em runners padrão de repositórios públicos é gratuito; não ativar runners premium ou serviços pagos. Os resultados ficam como artefato `oportunidades` por sete dias. Não há envio automático por e-mail ou alteração de arquivos do repositório pelo workflow. Relatórios são públicos quando disponibilizados em um repositório público: só contêm informação pública dos anúncios.

Para interromper, desabilitar o workflow em Actions. Não adicionar senhas, cookies, perfis de navegador, informações bancárias ou documentos pessoais ao código, aos artefatos ou aos relatórios.

## Limite de independência

A coleta agendada não depende do computador de Du. Operar contas de freelancer exige uma sessão autenticada acessível no ambiente de execução. Esta configuração não autentica a conta nem transfere o login do computador pessoal. As propostas continuam sujeitas à revisão previamente solicitada por Du.
