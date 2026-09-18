# Checklist de conformidade e entrega

Este arquivo separa o que já está implementado do que exige uma ação da autora antes do envio.

## Implementação concluída

- [x] Dataset público real com 100.836 registros.
- [x] Pelo menos quatro variáveis numéricas e duas categóricas.
- [x] Arquivos crus preservados em `data/` e preparação reproduzível em `src/dados.py`.
- [x] Média, mediana, moda e amplitude próprias.
- [x] Moda categórica e frequências próprias, com empates e ausentes validados.
- [x] Variância e desvio padrão amostral e populacional próprios.
- [x] Percentis, quartis e coeficiente de variação próprios.
- [x] Covariância e correlação de Pearson próprias.
- [x] Regressão linear por mínimos quadrados própria, com R² e predição.
- [x] Testes contra NumPy/SciPy com tolerância relativa `1e-10` e absoluta `1e-12`.
- [x] Tabela de frequência para variáveis numéricas e categóricas.
- [x] Histograma, boxplot e gráfico de barras.
- [x] Detecção de outliers pela regra de 1,5 × IQR.
- [x] Interpretação automática de assimetria.
- [x] Simulação da Lei dos Grandes Números com parâmetros interativos.
- [x] Simulação do Teorema Central do Limite com tamanho e repetições ajustáveis.
- [x] Sobreposição das distribuições Normal, Exponencial e Uniforme.
- [x] Diagrama de dispersão, reta, equação, Pearson, R² e predição.
- [x] Alerta de que correlação não implica causalidade.
- [x] Três descobertas baseadas nos resultados do dataset.
- [x] `README.md`, `RELATORIO.md`, `requirements.txt` e roteiro do vídeo.
- [x] Interface separada do núcleo estatístico.

## Ações obrigatórias da autora antes da entrega

- [x] Preencher nome completo e RA/DRT no `README.md`.
- [x] Preencher identificação no `RELATORIO.md`.
- [x] Iniciar o repositório Git local e organizar o histórico em commits.
- [ ] Criar um repositório público no GitHub ou GitLab.
- [x] Registrar núcleo, aplicação e documentação em commits separados.
- [ ] Substituir o campo do repositório pelo endereço público definitivo.
- [x] Adicionar capturas ou GIF da aplicação ao `README.md`.
- [x] Inserir a evidência dos testes aprovados no relatório.
- [x] Inserir capturas atuais das oito telas no README e no relatório.
- [ ] Gravar o vídeo de 3 a 5 minutos com demonstração e explicação do núcleo.
- [ ] Publicar o vídeo como não listado ou liberar o acesso no Drive.
- [ ] Preencher o link do vídeo no `README.md`, `RELATORIO.md` e PDF final.
- [x] Gerar e revisar visualmente a prévia do PDF de entrega.
- [ ] Gerar o PDF definitivo após informar os links externos.
- [ ] Testar dataset, repositório e vídeo em uma janela anônima.
- [ ] Confirmar que a autora sabe explicar funções, fórmulas e módulos.
- [ ] Confirmar o prazo no ambiente da disciplina (o enunciado trouxe `[DATA/HORA]`).
- [ ] Anexar o PDF definitivo e confirmar o envio no ambiente virtual.

## Revisão da refatoração — 09/09/2026

- [x] Separação de páginas, análises, dados, gráficos e carregamento.
- [x] Dataset validado por condições reais, com 9.724 filmes avaliados e 9.742 no catálogo.
- [x] Tabela e histograma compartilham classes; boxplot usa quartis próprios.
- [x] Histogramas do início, descobertas e TCL recebem contagens/densidades próprias, sem agregação automática do Plotly.
- [x] NaN, infinitos, iteradores e variáveis constantes cobertos por testes.
- [x] Documentação e três descobertas consistentes com os números da aplicação.
- [x] Versões diretas fixadas e dependências auxiliares documentadas.

Detalhamento dos resultados em `docs/VALIDACAO.md`. O histórico local existe;
a avaliação acadêmica de autoria e desenvolvimento real permanece a cargo do professor.

## Comandos de verificação

```bash
source .venv/bin/activate
pytest
streamlit run app.py
```

O trabalho não deve ser considerado pronto para envio enquanto houver itens pendentes na seção anterior.
