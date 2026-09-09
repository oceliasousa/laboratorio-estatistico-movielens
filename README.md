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

Cada observação analisada é uma avaliação. A base de avaliações inclui **9.724 filmes distintos**; os **9.742 filmes** se referem ao catálogo original. Além das colunas originais, `src/dados.py` deriva `ano_filme`, `ano_avaliacao`, `genero_principal`, `quantidade_generos` e `faixa_avaliacao`. São 11 colunas preparadas, quatro variáveis numéricas de análise e quatro categóricas. IDs não contam como grandezas. Há 18 avaliações sem ano do filme, removidas somente nas análises que usam essa coluna.

## Funcionalidades

- núcleo próprio com média, mediana, moda, amplitude, variâncias, desvios, percentis, quartis, CV, covariância, Pearson e regressão por mínimos quadrados;
- tabela de frequência, histograma, boxplot, barras, IQR e interpretação automática;
- Monte Carlo para Lei dos Grandes Números e Teorema Central do Limite;
- ajuste visual das distribuições Normal, Exponencial e Uniforme;
- correlação, reta, equação, R² e predição interativa;
- testes automatizados comparados com NumPy e SciPy.

## Instalação e execução

Use Python 3.9 a 3.12 com as versões fixadas em `requirements.txt`. A validação local desta refatoração usou Python 3.9. Python 3.13 ou posterior não foi validado com essas dependências.

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

A tolerância adotada é `rel=1e-10` e `abs=1e-12`. Percentis usam interpolação linear, igual ao padrão do NumPy. Variância/covariância populacional usam divisor `N`; as amostrais, `N-1`. Veja o resultado e o escopo em [Validação](docs/VALIDACAO.md).

## Estrutura

```text
sistematizacao/
├── app.py                    # ponto de entrada e tratamento de erros
├── src/
│   ├── dados.py              # preparação reprodutível
│   ├── minhastats.py         # núcleo matemático próprio
│   ├── analises.py           # frequências, IQR, simulação, ajuste e regressão
│   ├── config.py             # caminhos e configuração compartilhada
│   ├── rotas.py              # registro das oito páginas
│   ├── paginas/              # uma tela por arquivo
│   └── ui/                   # layout, gráficos, formatação e carregamento
├── tests/                    # núcleo, análises, dados e integração das telas
├── styles.css               # estilos e regras responsivas
├── docs/images/             # capturas reais da aplicação
├── data/                     # arquivos crus MovieLens
├── RELATORIO.md
└── requirements.txt
```

## Capturas de tela

### Evidência dos testes automatizados

![Resultado dos testes automatizados](docs/images/testes-pytest.png)

Capturas feitas após a refatoração em 09/09/2026:

![Tela inicial](docs/images/inicio.png)
![Estatística descritiva](docs/images/descritiva.png)
![Correlação e regressão](docs/images/regressao.png)

As oito telas estão documentadas no [relatório](RELATORIO.md).

## Onde editar

Textos de cada tela: `src/paginas/`. Cabeçalho, navegação e rodapé: `src/ui/layout.py`.
Mensagens de carregamento: `src/ui/carregamento.py`. Cores e dimensões: `styles.css`.
Fórmulas: `src/minhastats.py`; análises reutilizáveis: `src/analises.py`.

## Vídeo

**Link da demonstração (3–5 min):** aguardando gravação e publicação.

## PDF de entrega

Uma prévia é gerada sem os links externos:

```bash
python scripts/gerar_pdf_entrega.py
```

Antes de gerar o PDF ou a imagem dos testes, instale as dependências auxiliares:

```bash
python -m pip install -r requirements-entrega.txt
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
Os ajustes contínuos são aproximações de variáveis discretizadas. O primeiro gênero listado
é uma convenção, não uma classificação principal oficial. A licença original acompanha `data/README.txt`.

## O que falta para entregar

Publicar um repositório público, gravar/publicar o vídeo de 3 a 5 minutos,
informar os dois links e gerar o PDF definitivo. Depois, verificar o acesso aos links
em janela anônima e anexar o PDF no ambiente da disciplina dentro do prazo.
Veja [CHECKLIST_ENTREGA.md](CHECKLIST_ENTREGA.md). Nenhuma publicação foi realizada automaticamente.
