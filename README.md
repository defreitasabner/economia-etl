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
python cli.py --domain bcb --dataset atas --tier silver
python cli.py --domain bcb --dataset comunicados --tier bronze --debug
```

Para consultar todas as opções:

```bash
python cli.py --help
```

---

## Pipelines disponíveis

### Domínio `bcb`

Datasets disponíveis:

| Dataset | Descrição |
|---------|-----------|
| `atas` | Atas das reuniões do COPOM |
| `comunicados` | Comunicados do COPOM |
| `selic` | Série diária da taxa Selic |

Cobertura por tier:

| Domínio | Dataset | Bronze | Silver | Gold |
|---------|---------|--------|--------|------|
| `bcb` | `atas`  | ✅     | ✅     | ❌   |
| `bcb` | `comunicados`  | ✅     | ✅     | ❌   |
| `bcb` | `selic`  | ✅     | ✅     | ❌   |

Exemplos adicionais:

```bash
python cli.py --domain bcb --dataset comunicados --tier silver
python cli.py --domain bcb --dataset selic --tier bronze
```
