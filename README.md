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
python cli.py <domínio> <dataset> <tier> <opções>
```
O domínio é correspondente a um dos [domínios disponíveis](#domínios-disponíveis) e cada domínio possui um conjunto de datasets presentes na tabela na explicação de cada domínio. O tier é referente à [arquitetura em medalhão](#arquitetura-em-medalhão). As opções são específicas para cada padrão e podem ser consultadas através da opção `--help`.

---

## Domínios disponíveis

### COPOM — Comitê de Política Monetária
O domínio **COPOM** agrupa os dados do Comitê de Política Monetária do Banco Central do Brasil, disponibilizados via [API pública do BCB](https://www.bcb.gov.br/conteudo/dadosabertos/BCBDeinf/elements_copom.html#/). Os datasets disponíveis para esse domínio são:

| Dataset | Descrição |
|---------|-----------|
| `atas`  | Atas das reuniões do COPOM com os detalhes de cada reunião |

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
| `copom` | `atas`  | ✅     | ❌     | ❌   |