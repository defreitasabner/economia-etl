# Economia ETL

## Preparando ambiente
Crie um ambiente virtual com a ferramenta nativa do Python:
```bash
python -m venv .venv
```
Ative o ambiente virtual:

- **Linux/macOS:**
  ```bash
  source .venv/bin/activate
  ```
- **Windows:**
  ```bat
  .venv\Scripts\activate
  ```

Instale as dependências no ambiente virtual:
```bash
pip install -r requirements.txt
```

---

## Pipelines de ETL
Para executar as pipelines basta executar o seguinte comando:
```bash
python cli.py --domain <dominio> --dataset <dataset> --tier <tier> [--debug]
```
Argumentos da CLI:

- `--domain` (obrigatório): domínio para execução do pipeline.
- `--dataset` (obrigatório): dataset para execução do pipeline.
- `--tier` (obrigatório): camada da arquitetura medalhão (`bronze`, `silver`, `gold`).
- `--debug` (opcional): habilita logging detalhado.

Exemplos:

```bash
python cli.py --domain bcb --dataset atas --tier bronze
python cli.py --domain bcb --dataset comunicados --tier bronze --debug
```

Para consultar todas as opções:

```bash
python cli.py --help
```

---

## Domínios disponíveis

### BCB — Banco Central do Brasil
O domínio **BCB** agrupa dados públicos do Banco Central do Brasil, incluindo conteúdos do COPOM via [API pública do BCB](https://www.bcb.gov.br/conteudo/dadosabertos/BCBDeinf/elements_copom.html#/).

Datasets implementados no pipeline:

| Dataset | Descrição |
|---------|-----------|
| `atas`  | Atas das reuniões do COPOM com os detalhes de cada reunião |
| `comunicados` | Comunicados do COPOM com os detalhes de cada reunião |

Dataset configurado (em evolução):

| Dataset | Status |
|---------|--------|
| `selic` | Configuração disponível em `config/domains/bcb.yaml`, ainda sem extrator registrado |

---

## Arquitetura em medalhão
A arquitetura em medalhão organiza o processamento de dados em camadas incrementais de qualidade e refinamento:

- **Bronze:** ingestão bruta dos dados da fonte, com o mínimo de tratamento.
- **Silver:** dados limpos, padronizados e preparados para consumo analítico.
- **Gold:** dados agregados e modelados para casos de negócio e indicadores finais.

Esse padrão facilita rastreabilidade, reprocessamento e evolução das transformações ao longo do tempo.

### Cobertura de pipelines por dataset e tier

| Domínio | Dataset | Bronze | Silver | Gold |
|---------|---------|--------|--------|------|
| `bcb` | `atas`  | ✅     | ❌     | ❌   |
| `bcb` | `comunicados`  | ✅     | ❌     | ❌   |
| `bcb` | `selic`  | ❌     | ❌     | ❌   |

## Fonte de dados
