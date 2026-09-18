# Relatório — Laboratório Estatístico MovieLens

## 1. Identificação

- **Autora:** Océlia Assis de Sousa
- **RA/DRT:** 72650579
- **Modalidade:** trabalho individual
- **Disciplina:** Matemática e Estatística para Computação
- **Dataset:** [MovieLens Latest Small — dados crus oficiais](https://files.grouplens.org/datasets/movielens/ml-latest-small.zip)

## 2. Dataset e justificativa

O MovieLens foi escolhido por ser público, documentado e representar comportamento real de usuários. A versão utilizada reúne 100.836 avaliações de **9.724 filmes avaliados**, feitas por 610 usuários entre 1996 e 2018. O catálogo original contém **9.742 filmes**; 18 deles não possuem avaliação nessa tabela. O tema permite investigar dispersão, associação e distribuições com uma escala adequada para simulações.

A unidade de análise é uma avaliação. Os dados originais (`ratings.csv` e `movies.csv`) são unidos por `movieId`. Foram derivadas as variáveis ano do filme, ano da avaliação, gênero principal, quantidade de gêneros e faixa de avaliação. IDs são disponibilizados para exploração, mas devem ser interpretados como identificadores, não como grandezas quantitativas.

As variáveis usadas diretamente nas análises atendem aos requisitos mínimos:

| Tipo | Variáveis |
|---|---|
| Numéricas | `rating`, `ano_filme`, `ano_avaliacao`, `quantidade_generos` |
| Categóricas | `title`, `genres`, `genero_principal`, `faixa_avaliacao` |

A base preparada possui **100.836 registros**, **11 colunas**, **4 variáveis categóricas** e **7 colunas numéricas** no total. Identificadores e timestamp permanecem disponíveis para rastreabilidade, mas não são tratados como grandezas nas interpretações estatísticas.

O marcador `(no genres listed)` significa ausência de gênero listado. Para `quantidade_generos`, ele recebe **zero**, e não um: são 47 avaliações de 34 filmes. O campo categórico preserva o marcador original. O cache é invalidado quando mudam os CSVs ou as regras de preparação.

## 3. Núcleo estatístico próprio

O arquivo `src/minhastats.py` converte entradas em listas e executa explicitamente somas, ordenação, contagens e interpolações. Nenhuma função pronta de estatística é usada nos valores apresentados ao usuário.

Na refatoração, `app.py` passou a cuidar somente da configuração, carga, escolha da rota e tratamento de erros. `src/paginas/` reúne as oito telas; `src/ui/` centraliza layout, formatação, gráficos e carregamento; `src/analises.py` oferece funções testáveis para frequências, IQR, simulações, densidades e resultados da regressão. As funções de análise independem do Streamlit.

Nas medidas numéricas, entradas vazias, não numéricas, NaN e infinitos são rejeitados pelo núcleo. Iteradores são materializados uma vez para evitar consumo indevido. A média usa `math.fsum` para a soma em ponto flutuante. CV com média zero, Pearson com variável constante e R² com Y constante são recusados com mensagens explícitas. As funções categóricas possuem tratamento próprio de ausentes, descrito abaixo.

Para observações \(x_1,\ldots,x_n\):

### Tendência central

$$\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i$$

A mediana é o elemento central dos dados ordenados; para tamanho par, é a média dos dois centrais. A moda reúne os valores que atingem a maior frequência.

### Frequências e moda categórica

Para uma categoria \(c\), o núcleo percorre as observações e incrementa um dicionário:

$$n_c=\sum_{i=1}^{N}\mathbf{1}(x_i=c),\qquad f_c=\frac{n_c}{N},\qquad
M=\{c:n_c=\max_j n_j\}.$$

`frequencias_categoricas` calcula as contagens; `moda_categorica` retorna todas as categorias
de frequência máxima. A ordenação é decrescente por frequência e, em empates, preserva a ordem
da primeira ocorrência. Se todas as categorias empatam, todas são modais, conforme a convenção
de `statistics.multimode`; a tela informa que não há moda única.

`None` e `NaN` são agrupados como ausentes. Na preparação, Pandas apenas identifica os marcadores
`pd.NA`/`NaT` e os converte para `None`; não calcula contagens nem modas. Os ausentes são incluídos
no denominador \(N\) e recebem um rótulo visual distinto de qualquer categoria literal existente.
A tabela marca todas as modas na coluna `Modal`, mesmo quando o gráfico limita a exibição a 20 categorias.

`frequencias_relativas` calcula \(n_i/N\), e `frequencias_acumuladas` calcula
\(F_k=\sum_{i=1}^{k}n_i\) para as classes numéricas ordenadas. Não se atribui frequência
acumulada a gêneros nominais, pois não há ordem natural entre eles.

### Dispersão

$$A=x_{\max}-x_{\min}$$

$$\sigma^2=\frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n},\qquad
s^2=\frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1}$$

Os desvios padrão são as raízes das respectivas variâncias. O coeficiente de variação amostral é:

$$CV=\frac{s}{|\bar{x}|}\times100\%$$

### Percentis e quartis

Para percentil \(p\), ordenam-se os dados e calcula-se \(h=(n-1)p/100\). Quando \(h\) não é inteiro, usa-se interpolação linear entre as posições vizinhas. Os quartis são \(P_{25}\), \(P_{50}\) e \(P_{75}\). Outliers ficam abaixo de \(Q_1-1{,}5IQR\) ou acima de \(Q_3+1{,}5IQR\), com \(IQR=Q_3-Q_1\).

### Covariância e correlação

$$s_{xy}=\frac{\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y})}{n-1}$$

$$r=\frac{s_{xy}}{s_xs_y}$$

### Regressão linear simples

O modelo é \(\hat{y}=b_0+b_1x\), com:

$$b_1=\frac{\sum(x_i-\bar{x})(y_i-\bar{y})}{\sum(x_i-\bar{x})^2},\qquad
b_0=\bar{y}-b_1\bar{x}$$

$$R^2=1-\frac{\sum(y_i-\hat{y}_i)^2}{\sum(y_i-\bar{y})^2}$$

## 4. Validação

A suíte em `tests/` confronta as medidas com NumPy, SciPy, Pandas ou `statistics`. Foram definidos `rel=1e-10` e `abs=1e-12` para acomodar pequenas diferenças de ponto flutuante. Contagens e modas são comparadas exatamente. Casos inválidos (amostra vazia, percentil fora da faixa, variância com uma observação e variável constante) também são testados.

Comando de validação:

```bash
pytest
```

Resultado da revisão em 13/09/2026: **147 testes aprovados**. O detalhamento e o ambiente estão em [docs/VALIDACAO.md](docs/VALIDACAO.md). A suíte inclui testes do núcleo, das análises, da preparação dos dados, das oito rotas e de estados interativos.

A revisão corrigiu uma lacuna da versão anterior: as frequências categóricas e a categoria modal
ainda eram derivadas de `Pandas.value_counts()`. Agora as contagens, proporções e modas vêm de
funções próprias. Foram acrescentados 56 testes categóricos e 10 testes de análise/interface,
incluindo ausentes, empates e verificações que falham se as telas voltarem a usar `value_counts`
ou histogramas com agregação automática. Os números das três descobertas permaneceram iguais.

| Grupo validado | Referência |
|---|---|
| Média, mediana, amplitude, variâncias e desvios | NumPy |
| Moda, incluindo empates | SciPy e `statistics.multimode` |
| Frequências e moda categóricas, incluindo ausentes e empates | Pandas e `statistics.multimode` |
| Frequências relativas e acumuladas | NumPy |
| Percentis e quartis | NumPy |
| Coeficiente de variação | SciPy |
| Covariância e correlação de Pearson | NumPy e SciPy |
| Regressão linear e R² | SciPy/NumPy |
| Frequências e densidades Normal, Exponencial e Uniforme próprias | NumPy e SciPy |

Além dos testes do núcleo, as oito rotas da interface (`inicio`, `descritiva`, `simulacoes`, `distribuicoes`, `regressao`, `descobertas`, `dados` e `sobre`) foram executadas com o mecanismo de testes do Streamlit e não apresentaram exceções.

![Evidência dos testes automatizados](docs/images/testes-pytest.png)

## 5. Módulos da aplicação

### Módulo 0 — Dados

Exibe dimensões, variáveis, valores ausentes, prévia da base preparada e download de amostra.

### Módulo 1 — Núcleo estatístico

Documenta todas as funções estatísticas exigidas, as bibliotecas usadas como referência, a tolerância numérica dos testes e as fórmulas implementadas. A regressão linear própria é adicionada às medidas obrigatórias. Os resultados exibidos nas análises vêm de `src/minhastats.py`.

### Módulo 2 — Descritiva

O usuário seleciona uma variável. Para numéricas, vê as medidas próprias, frequências em classes, histograma, boxplot, assimetria de Pearson e outliers por IQR. Para categóricas, vê frequências absoluta/relativa, todas as categorias modais e gráfico de barras, calculados pelas funções próprias.

Tabela e histograma compartilham a mesma contagem própria e as mesmas bordas: classes fechadas à esquerda e abertas à direita, exceto a última, fechada dos dois lados. O boxplot recebe Q1, mediana, Q3 e bigodes já calculados pelo núcleo. A tabela categórica inclui todas as categorias; somente o gráfico limita a visualização às 20 mais frequentes. Para `rating`, Q1 = 3, Q3 = 4 e IQR = 1: há **4.181 observações** abaixo do limite inferior 1,5.

### Módulo 3 — Simulação

Na Lei dos Grandes Números, lançamentos de moeda mostram a frequência de caras convergindo para 0,5. No TCL, amostras com reposição de uma variável geram médias calculadas pelo núcleo próprio; tamanho, repetições e semente são controláveis.

A referência do TCL usa a média da população empírica e seu desvio populacional dividido por √n, em vez de ajustar a curva às próprias médias simuladas. Os resultados da simulação ficam em cache por dados e parâmetros. A proximidade da Normal pode ser examinada repetindo a simulação com n = 5, 30 e 100; não é uma garantia de aproximação perfeita para toda amostra.

### Módulo 4 — Distribuições

O histograma em densidade pode ser comparado às curvas Normal, Exponencial e Uniforme. Seus parâmetros são estimados a partir dos dados. A avaliação é visual e explicitamente apresentada como exploratória.

As densidades também são próprias, em `src/analises.py`:

$$f_N(x)=\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac12((x-\mu)/\sigma)^2}$$

$$f_E(x)=\frac{1}{\theta}e^{-(x-a)/\theta},\ x\ge a;\qquad f_U(x)=\frac{1}{b-a},\ a\le x\le b$$

Fora do suporte, as densidades Exponencial e Uniforme são zero. Na Normal, μ e σ vêm do núcleo. Na Exponencial deslocada, a é o mínimo e θ é a média de x − a. Na Uniforme, a e b são os extremos observados. Essas curvas aproximam variáveis discretas/discretizadas; não implicam que notas ou anos sejam tempos de espera ou medidas contínuas.

### Módulo 5 — Correlação e regressão

O usuário escolhe X e Y. Todos os pares válidos entram no cálculo próprio de Pearson e mínimos quadrados; até 5.000 pontos são amostrados somente para tornar o gráfico legível. A tela fornece equação, R², predição e o alerta de não causalidade.

### Módulo 6 — Relatório de descobertas

Reúne três conclusões calculadas a partir do mesmo conjunto de dados usado nos demais módulos. Cada descoberta apresenta indicadores numéricos, gráfico correspondente, evidências e uma interpretação que evita afirmações causais indevidas.

## 6. Três descobertas estatísticas

### 1. Ação e Comédia lideram em volume

Considerando o primeiro gênero listado, **Ação possui 30.635 avaliações** e **Comédia, 25.217**. Juntas, representam **55,39%** das 100.836 avaliações. O resultado mede volume de avaliações, não quantidade distinta de filmes ou preferência causal.

### 2. As avaliações se concentram entre 3 e 5

**81,09%** das notas estão entre 3 e 5 estrelas, inclusive. A nota média é **3,5016** e a mediana é **3,5** na escala de 0,5 a 5. O centro fica acima do ponto médio teórico (2,75), sem permitir concluir por que usuários selecionam ou avaliam filmes dessa maneira.

### 3. Ano de lançamento explica muito pouco da nota individual

A correlação de Pearson entre ano do filme e nota é **−0,0840**. O sinal é levemente negativo, mas a magnitude é muito pequena: uma regressão simples baseada apenas no ano tem poder explicativo baixo.

Na regressão de ano do filme para nota, **R² = 0,007064**, aproximadamente **0,71%** da variação das notas. Essas três descobertas são as mesmas apresentadas na tela Relatório de Descobertas e no resumo executivo.

## 7. Limitações e ética

- Os participantes do MovieLens não representam toda a população de espectadores.
- As observações não são independentes: cada usuário avalia vários filmes.
- `genero_principal` depende da ordem fornecida no arquivo.
- Correlação e regressão simples não estabelecem causalidade.
- IDs não devem receber interpretação métrica, embora permaneçam disponíveis para fins didáticos.
- CV em anos e notas é didático: essas escalas não possuem zero absoluto e não justificam comparação proporcional de dispersão.
- Índice de assimetria próximo de zero não comprova simetria; histogramas e boxplots complementam a interpretação.
- A validação por tipos e contagens não elimina problemas de representatividade ou dependência entre observações.

## 8. Evidências e reprodutibilidade

O resultado dos testes está registrado na Seção 4 e na imagem `docs/images/testes-pytest.png`. A execução pode ser reproduzida com os comandos documentados no `README.md`.

O repositório Git local possui commits separados para o núcleo estatístico e preparação dos dados, a aplicação Streamlit, a documentação e a validação final. Essa separação facilita a identificação da evolução técnica do projeto.

Materiais externos que ainda dependem de publicação:

- **Vídeo:** aguardando gravação e publicação.
- **Repositório público:** aguardando criação e publicação.
- **Capturas da aplicação:** registradas após a refatoração em `docs/images/`.

Depois que os links forem informados, o script `scripts/gerar_pdf_entrega.py` cria o arquivo definitivo `SISTEMATIZACAO_MEC_OceliaAssisDeSousa.pdf`. A prévia já foi gerada e revisada visualmente.

## 9. Capturas atuais dos módulos

As capturas abaixo foram atualizadas no navegador em 13/09/2026, após a revisão dos cálculos.

### Início

![Início](docs/images/inicio.png)

### Dados reais — módulo 0

![Dataset](docs/images/dados.png)

### Núcleo e documentação — módulo 1

![Documentação](docs/images/sobre.png)

### Descritiva — módulo 2

![Descritiva](docs/images/descritiva.png)

Estado categórico, com frequências próprias e identificação de todas as categorias modais:

![Frequências e moda categórica](docs/images/descritiva-categorica.png)

### Simulação — módulo 3

![Simulações](docs/images/simulacoes.png)

### Distribuições — módulo 4

![Distribuições](docs/images/distribuicoes.png)

### Regressão — módulo 5

![Regressão](docs/images/regressao.png)

### Descobertas — módulo 6

![Descobertas](docs/images/descobertas.png)

## 10. Situação da entrega

Os módulos técnicos, testes e evidências locais estão implementados. A entrega ainda exige publicação do repositório público, gravação/publicação do vídeo, preenchimento dos links e geração do PDF definitivo. A autora deve verificar os links em janela anônima, confirmar o prazo no ambiente virtual e efetuar o envio. O enunciado fornecido contém apenas o marcador `[DATA/HORA]`, sem prazo preenchido.
