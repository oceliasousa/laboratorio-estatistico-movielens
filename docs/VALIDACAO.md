# Validação da refatoração — 09/09/2026

Comando: `python -m pytest -q`. Resultado: **81 testes aprovados**.

## Escopo

- Todas as medidas exigidas, comparadas com NumPy/SciPy; modas empatadas comparadas com `statistics.multimode`.
- Variâncias e covariâncias amostral/populacional; CV com média positiva e negativa; iteradores.
- Rejeição de dados vazios, tipos inválidos, NaN, infinito, média zero, pares incompatíveis e variáveis constantes.
- Frequências e densidades próprias comparadas com NumPy/SciPy.
- Simulações reproduzíveis, contagem total e densidades normalizadas.
- Dados reais, junção sem perda silenciosa de avaliações e validação de estrutura.
- Oito rotas, rota desconhecida, variável categórica e regressão inválida.

Tolerância de comparação numérica: `rel=1e-10`, `abs=1e-12`.
Testes de Monte Carlo usam margens explícitas para resultados aleatórios com semente fixa;
o teste de valor publicado de correlação usa tolerância de arredondamento de `1e-4`.

## Ambiente efetivamente executado

Python 3.9; Streamlit 1.50.0; Pandas 2.3.3; NumPy 2.0.2; SciPy 1.13.1;
Plotly 6.9.0; pytest 8.4.2. Dependências diretas fixadas em `requirements.txt`.
O teste foi feito no ambiente virtual local, não em todas as versões/sistemas operacionais.

## Conferência no navegador

Capturas atuais das oito rotas em `docs/images/`. Durante a navegação, foi medido
quadro a quadro se o conteúdo aparecia antes do carregamento. Também foram verificados
conclusão da máscara, presença dos gráficos e disponibilidade da navegação móvel.
As capturas são evidência visual; a suíte Streamlit não substitui testes de interação
de todos os botões da barra do Plotly ou de acessibilidade completa.

## Limites da validação

Os resultados locais não comprovam publicação pública, permissões do vídeo ou envio
da atividade. Esses itens permanecem no `CHECKLIST_ENTREGA.md`. Não se afirma que o
dataset seja representativo de todos os espectadores nem que ajustes visuais comprovem
uma distribuição teórica.
