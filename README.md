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
python cli.py --domain bcb --dataset atas --tier silver
python cli.py --domain bcb --dataset comunicados --tier bronze --debug
```

Para consultar todas as opções:

```bash
python cli.py --help
```

## Pipelines disponíveis

### Domínio `bcb`

Datasets disponíveis:

| Dataset | Descrição |
|---------|-----------|
| `atas` | Atas das reuniões do COPOM |
| `comunicados` | Comunicados do COPOM |
| `selic` | Série mensal da taxa Selic |
| `pib` | Série mensal do PIB |
| `cambio` | Série de câmbio |
| `ipca` | Série do IPCA |

Cobertura por tier:

| Domínio | Dataset | Bronze | Silver | Gold |
|---------|---------|--------|--------|------|
| `bcb` | `atas`  | ✅     | ✅     | ❌   |
| `bcb` | `comunicados`  | ✅     | ✅     | ❌   |
| `bcb` | `selic`  | ✅     | ✅     | ❌   |
| `bcb` | `pib`  | ✅     | ✅     | ❌   |
| `bcb` | `cambio`  | ✅     | ✅     | ❌   |
| `bcb` | `ipca`  | ✅     | ✅     | ❌   |

Exemplos adicionais:

```bash
python cli.py --domain bcb --dataset comunicados --tier silver
python cli.py --domain bcb --dataset selic --tier bronze
python cli.py --domain bcb --dataset pib --tier bronze
python cli.py --domain bcb --dataset ipca --tier silver
```

## Execução em lote por tier

Existem scripts shell para executar todos os datasets de todos os domínios de uma vez para um tier específico:

- `scripts/run_all_bronze.sh`
- `scripts/run_all_silver.sh`

Como os scripts fazem `cd ..` internamente, execute-os a partir do diretório `scripts`:

```bash
cd scripts
./run_all_bronze.sh
./run_all_silver.sh
```

## Fontes
- [API Copom do BCB](https://www.bcb.gov.br/conteudo/dadosabertos/BCBDeinf/elements_copom.html#/)
- [Sistema Gerenciador de Séries Temporais do BCB - SGS](https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries)