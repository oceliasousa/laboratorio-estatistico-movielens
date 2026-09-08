# SISTEMATIZACAO_MEC_OceliaAssisDeSousa

## Identificação

- **Autora:** Océlia Assis de Sousa
- **RA/DRT:** 72650579
- **Modalidade:** trabalho individual

## Links obrigatórios

- **Dados crus:** https://files.grouplens.org/datasets/movielens/ml-latest-small.zip
- **Solução pública:** aguardando criação e publicação.
- **Vídeo (acesso liberado):** aguardando gravação e publicação.

## Resumo executivo

O Laboratório Estatístico MovieLens analisa 100.836 avaliações reais de 9.742 filmes. A solução implementa, sem funções estatísticas prontas, medidas de tendência central e dispersão, percentis, covariância, correlação e regressão linear. Os resultados são validados automaticamente contra NumPy e SciPy. A interface Streamlit oferece estatística descritiva, gráficos, outliers por IQR, Lei dos Grandes Números, Teorema Central do Limite, distribuições teóricas e regressão com predição.

As três descobertas principais foram: (1) as notas têm média 3,5016 e mediana 3,5; (2) Ação é o gênero principal com maior volume, somando 30.635 avaliações; e (3) ano do filme apresenta associação linear muito fraca com nota (r = −0,0840), portanto explica pouco da avaliação individual.

O script `scripts/gerar_pdf_entrega.py` gera uma prévia e, após receber as URLs do repositório e do vídeo, cria o PDF definitivo no padrão solicitado. Antes do envio, todos os links devem ser testados em uma janela anônima.
