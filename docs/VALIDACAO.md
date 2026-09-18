# Validação — revisão de 13/09/2026

Comando executado: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -p no:cacheprovider -ra`.
Resultado: **147 testes aprovados**, em 23,68 segundos no ambiente local.
As opções de cache não alteram os testes; `python -m pytest` executa a mesma suíte.

## Escopo

- Todas as medidas exigidas, comparadas com NumPy/SciPy; modas empatadas comparadas com `statistics.multimode`.
- Variâncias e covariâncias amostral/populacional; CV com média positiva e negativa; iteradores.
- Rejeição de dados vazios, tipos inválidos, NaN, infinito, média zero, pares incompatíveis e variáveis constantes.
- Frequências e densidades próprias comparadas com NumPy/SciPy.
- Frequências/modas categóricas comparadas com Pandas e `statistics.multimode`: empates,
  categorias únicas, Unicode, iteradores, None/NaN, pd.NA/NaT e rótulos literais de ausência.
- Frequências relativas e acumuladas próprias, incluindo classes de frequência zero.
- Proteção contra regressão: telas testadas com `value_counts` e `px.histogram` bloqueados;
  histogramas recebem contagens próprias e os dados enviados aos gráficos são conferidos.
- A tela categórica chama as funções próprias e preserva todas as modas em empates.
- Simulações reproduzíveis, contagem total e densidades normalizadas.
- Dados reais, junção sem perda silenciosa de avaliações e validação de estrutura.
- Oito rotas, rota desconhecida, variável categórica e regressão inválida.

Tolerância de comparação numérica: `rel=1e-10`, `abs=1e-12`.
Contagens e modas usam igualdade exata. Proporções incluem os ausentes no denominador.
Testes de Monte Carlo usam margens explícitas para resultados aleatórios com semente fixa;
o teste de valor publicado de correlação usa tolerância de arredondamento de `1e-4`.

## Ambiente efetivamente executado

Python 3.9; Streamlit 1.50.0; Pandas 2.3.3; NumPy 2.0.2; SciPy 1.13.1;
Plotly 6.9.0; pytest 8.4.2. Dependências diretas fixadas em `requirements.txt`.
O teste foi feito no ambiente virtual local, não em todas as versões/sistemas operacionais.

## Conferência no navegador

Capturas das oito rotas atualizadas em 13/09/2026 em `docs/images/`, além do estado
categórico de Descritiva (`descritiva-categorica.png`). Durante a navegação, foi medido
quadro a quadro se o conteúdo aparecia antes do carregamento. Também foram verificados
conclusão da máscara, presença dos gráficos e disponibilidade da navegação móvel.
As capturas são evidência visual; a suíte Streamlit não substitui testes de interação
de todos os botões da barra do Plotly ou de acessibilidade completa.

## Correções desta revisão

A versão anterior tinha 81 testes, mas não verificava a origem dos cálculos categóricos.
Os usos analíticos de `value_counts` e `cumsum` foram substituídos por funções próprias,
assim como a agregação dos histogramas de início, descobertas e TCL. Foram adicionados
56 testes categóricos e 10 testes de análise/interface. A revisão não alterou os dados crus
nem os valores publicados das três descobertas.

## Limites da validação

Os resultados locais não comprovam publicação pública, permissões do vídeo ou envio
da atividade. Esses itens permanecem no `CHECKLIST_ENTREGA.md`. Não se afirma que o
dataset seja representativo de todos os espectadores nem que ajustes visuais comprovem
uma distribuição teórica.
