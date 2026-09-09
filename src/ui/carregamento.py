"""Carregamento do laboratório estatístico."""

import streamlit as st
import streamlit.components.v1 as components


def controlar_rolagem(pagina):
    """Retorna ao topo somente quando a rota da aplicação muda."""
    with st.container(key="scroll_controller"):
        components.html(
            f"""
            <script>
            (() => {{
              const appWindow = window.parent;
              const route = {pagina!r};
              const storageKey = "labestat-rota-atual";
              appWindow.history.scrollRestoration = "manual";

              const resetScroll = () => {{
                const document = appWindow.document;
                const containers = [
                  document.scrollingElement,
                  document.documentElement,
                  document.body,
                  document.querySelector('[data-testid="stAppViewContainer"]'),
                  document.querySelector('[data-testid="stMain"]')
                ];
                appWindow.scrollTo(0, 0);
                containers.forEach((container) => {{
                  if (!container) return;
                  container.scrollTop = 0;
                  if (typeof container.scrollTo === "function") container.scrollTo(0, 0);
                }});
              }};

              appWindow.__labestatResetScroll = resetScroll;

              if (!appWindow.__labestatScrollNavigationBound) {{
                appWindow.document.addEventListener("pointerdown", (event) => {{
                  const link = event.target.closest('a[href*="?page="]');
                  if (link) appWindow.__labestatResetScroll();
                }}, true);
                appWindow.addEventListener("beforeunload", () => {{
                  appWindow.__labestatResetScroll();
                }});
                appWindow.__labestatScrollNavigationBound = true;
              }}

              if (appWindow.sessionStorage.getItem(storageKey) !== route) {{
                appWindow.sessionStorage.setItem(storageKey, route);
                resetScroll();
              }}
            }})();
            </script>
            """,
            height=0,
            width=0,
        )


def iniciar_carregamento(pagina):
    """Exibe uma transição curta apenas ao abrir ou trocar de página."""
    titulos = {
        "inicio": "Preparando o laboratório",
        "descritiva": "Carregando estatística descritiva",
        "simulacoes": "Preparando as simulações",
        "distribuicoes": "Carregando distribuições teóricas",
        "regressao": "Calculando correlação e regressão",
        "descobertas": "Organizando as descobertas",
        "dados": "Carregando o dataset",
        "sobre": "Carregando a documentação",
    }
    titulo = titulos.get(pagina, "Carregando página")
    # O HTML chega antes do conteúdo. O iframe só coordena a conclusão;
    # sua inicialização assíncrona não deve decidir quando mostrar a máscara.
    st.markdown(
        f"""
        <div id="labestat-page-loader" role="status" aria-live="polite">
          <div class="loader-panel">
            <div class="loader-symbol" aria-hidden="true">∑</div>
            <div class="loader-copy">
              <strong>{titulo}</strong><span>LabEstat</span>
            </div>
            <div class="loader-track" aria-hidden="true"><i></i></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container(key="page_loader_start"):
        components.html(
            f"""
            <script>
            (() => {{
              const appWindow = window.parent;
              const document = appWindow.document;
              const route = {pagina!r};
              const firstRender = !appWindow.__labestatLoaderInitialized;
              const routeChanged = appWindow.__labestatLoaderRoute !== route;

              appWindow.__labestatLoaderInitialized = true;
              appWindow.__labestatLoaderRoute = route;
              if (!firstRender && !routeChanged) return;

              document.documentElement.removeAttribute("data-labestat-ready");
              appWindow.__labestatLoaderStarted = appWindow.performance.now();
            }})();
            </script>
            """,
            height=0,
            width=0,
        )


def finalizar_carregamento():
    """Remove o carregamento depois que os componentes visuais foram montados."""
    with st.container(key="page_loader_finish"):
        components.html(
            """
            <script>
            (() => {
              const appWindow = window.parent;
              const document = appWindow.document;
              const expectedCharts = __EXPECTED_CHARTS__;
              let attempts = 0;

              const finish = () => {
                const loader = document.getElementById("labestat-page-loader");
                if (!loader) return;
                const elapsed = appWindow.performance.now()
                  - (appWindow.__labestatLoaderStarted || 0);
                const remaining = Math.max(0, 520 - elapsed);
                appWindow.setTimeout(() => {
                  document.documentElement.setAttribute("data-labestat-ready", "true");
                }, remaining);
              };

              const waitForCharts = () => {
                const charts = [...document.querySelectorAll('[data-testid="stPlotlyChart"]')];
                const pending = charts.length < expectedCharts || charts.some(
                  (chart) => !chart.querySelector(".js-plotly-plot .main-svg"));
                if (pending && attempts++ < 125) {
                  appWindow.setTimeout(waitForCharts, 40);
                  return;
                }
                appWindow.requestAnimationFrame(() =>
                  appWindow.requestAnimationFrame(finish));
              };

              waitForCharts();
            })();
            </script>
            """.replace("__EXPECTED_CHARTS__", str(st.session_state.get('_graficos_esperados', 0))),
            height=0,
            width=0,
        )
