# Report Automation Bot

Automação de ponta a ponta de uma rotina comum em times de dados/BI: gerar
uma base de dados de vendas, transformá-la em um relatório Excel formatado e
(opcionalmente) distribuí-lo por e-mail. O objetivo deste projeto é
demonstrar, com código real e executável, como uma tarefa manual repetitiva
(abrir sistema, exportar planilha, formatar, enviar por e-mail) pode ser
substituída por um script confiável e versionado.

O domínio usado é um **varejo fictício**: produtos, clientes e pedidos
gerados sinteticamente com [Faker](https://faker.readthedocs.io/). Nenhum
dado real é utilizado.

## O que este projeto demonstra

- Modelagem e povoamento de um banco de dados relacional (SQLite) a partir
  de dados sintéticos gerados com Faker.
- Consultas SQL via `pandas` para agregações de negócio (totais, top
  produtos, detalhamento por pedido).
- Geração de relatório Excel formatado programaticamente com `openpyxl`:
  múltiplas abas, cabeçalhos em negrito, largura de coluna ajustada e um
  gráfico de barras.
- Um exemplo de automação de envio de e-mail via `smtplib`, com um modo
  **dry-run seguro por padrão** — nada é enviado de verdade a menos que
  credenciais SMTP reais sejam fornecidas explicitamente.
- Teste de sanidade automatizado do relatório gerado.

## Estrutura do repositório

```
automacao-relatorios/
├── requirements.txt
├── src/
│   ├── generate_db.py    # cria sales.db (SQLite) com dados sinteticos via Faker
│   ├── build_report.py   # gera relatorio_vendas.xlsx a partir do sales.db
│   └── email_report.py   # (dry-run por padrao) demonstra o envio do relatorio por e-mail
└── tests/
    └── test_report.py    # valida que o Excel gerado tem as abas e dados esperados
```

## Como executar

```bash
# 1. instalar dependências
pip install -r requirements.txt

# 2. gerar o banco de dados sintético (cria src/sales.db)
python src/generate_db.py

# 3. gerar o relatório Excel (cria src/relatorio_vendas.xlsx)
python src/build_report.py

# 4. (opcional) simular o envio por e-mail — modo dry-run, não envia nada de verdade
python src/email_report.py

# 5. rodar os testes
python -m unittest tests/test_report.py -v
```

## Detalhes de cada script

### `src/generate_db.py`

Cria um banco SQLite (`sales.db`) com três tabelas — `products`,
`customers` e `orders` — populadas com dados fictícios gerados pelo Faker
(nomes, e-mails, categorias de produto, datas e valores). O volume de dados
é parametrizável no topo do script.

### `src/build_report.py`

Lê o `sales.db` com `pandas`, calcula métricas de negócio (receita total,
número de pedidos, top produtos por receita) e gera um arquivo Excel com:

- **Aba "Resumo"**: totais gerais e ranking dos produtos mais vendidos, com
  cabeçalhos em negrito, colunas com largura ajustada ao conteúdo e um
  gráfico de barras dos top produtos.
- **Aba "Detalhe"**: todos os pedidos, um por linha, com dados de cliente e
  produto já unidos (join) para facilitar a leitura.

### `src/email_report.py`

Função `send_report(...)` que demonstra como o relatório seria enviado por
e-mail via `smtplib`, lendo host/usuário/senha/destinatário de variáveis de
ambiente (`SMTP_HOST`, `SMTP_USER`, `SMTP_PASSWORD`, `REPORT_RECIPIENT`).
**Por segurança, o padrão é `dry_run=True`**: o script apenas imprime no
console o que seria enviado (destinatário, assunto, anexo). O envio real só
acontece se o script for chamado com `--send` (ou `dry_run=False`
diretamente na função) **e** as variáveis de ambiente de SMTP estiverem
presentes — caso contrário, ele recusa o envio e explica o motivo. Isso
garante que ninguém rode este repositório e dispare e-mails por acidente.

## Habilidades demonstradas

- Python para automação de rotinas de analista de dados/BI.
- Modelagem de dados relacional simples (SQLite) e geração de dados
  sintéticos realistas com Faker.
- Manipulação e agregação de dados com `pandas`.
- Geração de relatórios Excel formatados programaticamente (`openpyxl`).
- Boas práticas de segurança em automação (nunca enviar e-mails de verdade
  por padrão, credenciais via variáveis de ambiente, nunca hardcoded).
- Testes automatizados como parte do fluxo de entrega.

## Licença

Distribuído sob a licença MIT — veja [LICENSE](LICENSE).
