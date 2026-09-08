# Laboratório Estatístico Interativo — MovieLens

Aplicação Streamlit desenvolvida para a Sistematização de **Matemática e Estatística para Computação**. O projeto transforma mais de 100 mil avaliações reais de filmes em um laboratório de estatística descritiva, simulação, distribuições e regressão.

## Autora

- **Nome:** Océlia Assis de Sousa
- **RA/DRT:** 72650579
- **Modalidade:** trabalho individual

## Dataset

- Dados crus: [MovieLens Latest Small — arquivo oficial](https://files.grouplens.org/datasets/movielens/ml-latest-small.zip)
- Página do dataset: [MovieLens Latest — GroupLens](https://grouplens.org/datasets/movielens/latest/)
- Versão: `ml-latest-small`, gerada em 26/09/2018
- Dados crus: 100.836 avaliações, 9.742 filmes, 610 usuários e 3.683 aplicações de tags
- Licença e descrição originais: [`data/README.txt`](data/README.txt)

Cada observação analisada é uma avaliação. Além das colunas originais, `src/dados.py` deriva `ano_filme`, `ano_avaliacao`, `genero_principal`, `quantidade_generos` e `faixa_avaliacao`. Assim, a base preparada possui pelo menos quatro variáveis numéricas e duas categóricas.

## Funcionalidades

- núcleo próprio com média, mediana, moda, amplitude, variâncias, desvios, percentis, quartis, CV, covariância, Pearson e regressão por mínimos quadrados;
- tabela de frequência, histograma, boxplot, barras, IQR e interpretação automática;
- Monte Carlo para Lei dos Grandes Números e Teorema Central do Limite;
- ajuste visual das distribuições Normal, Exponencial e Uniforme;
- correlação, reta, equação, R² e predição interativa;
- testes automatizados comparados com NumPy e SciPy.

## Instalação e execução

É recomendado Python 3.10 ou superior.

```bash
cd sistematizacao
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
streamlit run app.py
```

O navegador abrirá em `http://localhost:8501`.

## Testes

```bash
pytest
```

A tolerância adotada é `rel=1e-10` e `abs=1e-12`. Percentis usam interpolação linear, igual ao padrão do NumPy. Variância/covariância populacional usam divisor `N`; as amostrais, `N-1`.

## Estrutura

```text
sistematizacao/
├── app.py                    # interface Streamlit
├── src/
│   ├── dados.py              # preparação reprodutível
│   └── minhastats.py         # núcleo matemático próprio
├── tests/test_minhastats.py  # validação NumPy/SciPy
├── data/                     # arquivos crus MovieLens
├── RELATORIO.md
└── requirements.txt
```

## Capturas de tela

### Evidência dos testes automatizados

![Doze testes automatizados aprovados](docs/images/testes-pytest.png)

Ainda é necessário salvar ao menos uma captura atual da aplicação em
`docs/images/tela-aplicacao.png` para completar a evidência visual exigida.

## Vídeo

**Link da demonstração (3–5 min):** aguardando gravação e publicação.

## PDF de entrega

Uma prévia é gerada sem os links externos:

```bash
python scripts/gerar_pdf_entrega.py
```

Depois de publicar o repositório e o vídeo, gere o arquivo definitivo:

```bash
python scripts/gerar_pdf_entrega.py \
  --repositorio "URL_PUBLICA_DO_REPOSITORIO" \
  --video "URL_PUBLICA_OU_NAO_LISTADA_DO_VIDEO"
```

O arquivo final será salvo em
`output/pdf/SISTEMATIZACAO_MEC_OceliaAssisDeSousa.pdf`.

## Aviso analítico

Os resultados descrevem apenas esta amostra do MovieLens. Associação estatística não demonstra causalidade.
