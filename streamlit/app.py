
import requests
import streamlit as st
import os

from dotenv import load_dotenv
from pathlib import Path
from datetime import date
from html.parser import HTMLParser


# ==========================================
# 1. CONFIGURACOES
# ==========================================

caminho_env = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=caminho_env)

link_API = os.getenv("NASA_API_URL")

st.set_page_config(
    page_title="NASA Explorer",
    page_icon="🚀",
    layout="wide"
)


# ==========================================
# 2. LIMPAR CODIGOS HTML DAS DESCRICOES
# ==========================================

class LimparHTML(HTMLParser):

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.texto = []
        self.ignorar_conteudo = False

    def handle_starttag(self, tag, atributos):

        if tag in ["script", "style"]:
            self.ignorar_conteudo = True

        elif not self.ignorar_conteudo and tag in [
            "br", "p", "div", "li", "h1", "h2", "h3"
        ]:
            self.texto.append("\n")

    def handle_endtag(self, tag):

        if tag in ["script", "style"]:
            self.ignorar_conteudo = False

        elif not self.ignorar_conteudo and tag in [
            "p", "div", "li", "h1", "h2", "h3"
        ]:
            self.texto.append("\n")

    def handle_data(self, dado):

        if not self.ignorar_conteudo:
            self.texto.append(dado)


def limpar_html(texto):

    if not texto:
        return "Descrição não disponível."

    conversor = LimparHTML()
    conversor.feed(str(texto))

    descricao = "".join(conversor.texto)

    return descricao.strip()


# ==========================================
# 3. ESTILO VISUAL
# ==========================================

st.markdown("""
<style>

    .stApp {
        background-color: #172438;
        color: #FFFFFF;
    }

    h1 {
        color: #9BD5FF !important;
        text-align: center;
    }

    h2, h3 {
        color: #B8DEFF !important;
    }

    .stMarkdown p,
    .stMarkdown li {
        color: #FFFFFF !important;
        line-height: 1.7;
    }

    [data-testid="stSidebar"] {
        background-color: #203249;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #263A52;
        border-radius: 14px;
        border: 1px solid #496783;
        padding: 14px;
    }

    [data-testid="stCaptionContainer"] p {
        color: #D5E3F0 !important;
    }

    [data-testid="stMetricValue"] {
        color: #9BD5FF !important;
    }

    [data-testid="stMetricLabel"] {
        color: #FFFFFF !important;
    }

    [data-testid="stExpander"] {
        background-color: #30465F !important;
        border: 1px solid #75B9E8 !important;
        border-radius: 10px;
    }

    [data-testid="stExpander"] p {
        color: #FFFFFF !important;
        font-size: 16px;
        line-height: 1.8;
    }

    .stButton button,
    .stLinkButton a {
        background-color: #315B7D;
        color: #FFFFFF !important;
        border-radius: 8px;
        border: 1px solid #75B9E8;
    }

</style>
""", unsafe_allow_html=True)


# ==========================================
# 4. FUNCAO PARA EXIBIR PUBLICACOES
# ==========================================

def mostrar_publicacao(publicacao):

    titulo = publicacao.get("title", "Sem título")
    data = publicacao.get("date", "Data não disponível")

    explicacao = publicacao.get(
        "explanation",
        "Descrição não disponível."
    )

    tipo_midia = publicacao.get("media_type")
    imagem = publicacao.get("hdurl") or publicacao.get("url")
    video = publicacao.get("url")
    link = publicacao.get("permalink")

    st.subheader(titulo)

    st.caption("📅 Data: " + str(data))

    # EXIBINDO IMAGENS
    if tipo_midia == "image":

        if imagem:
            st.image(imagem, width="stretch")
        else:
            st.warning("Imagem não disponível.")

    # EXIBINDO VIDEOS
    elif tipo_midia == "video":

        if video and (
            "youtube.com" in video or
            "youtu.be" in video or
            "vimeo.com" in video
        ):
            st.video(video)
        else:
            st.info("Vídeo disponível na página original.")

    # EXIBINDO DESCRICAO SEM CODIGOS HTML
    with st.expander("🔎 Saiba mais sobre esta publicação"):

        descricao_limpa = limpar_html(explicacao)

        st.write(descricao_limpa)

    # CREDITOS
    credito = publicacao.get("copyright")

    if credito:
        st.caption("Créditos: " + str(credito))

    # LINK ORIGINAL
    if link:

        st.link_button(
            "Ver publicação na NASA ↗",
            link
        )


# ==========================================
# 5. MENU LATERAL
# ==========================================

st.sidebar.title("🚀 NASA Explorer")

st.sidebar.write(
    "Explore imagens e descobertas do universo."
)

pagina = st.sidebar.radio(
    "Navegação",
    [
        "Explorar publicações",
        "Viagem no tempo",
        "Sobre o projeto"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "Projeto de consumo de API com Python e Streamlit."
)


# ==========================================
# 6. CABECALHO
# ==========================================

st.title("🚀 NASA EXPLORER")

st.markdown(
    '<p style="text-align:center; color:#D5E3F0; font-size:18px;">'
    'Explore o universo através das imagens e descobertas da NASA.'
    '</p>',
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# 7. VERIFICANDO A API
# ==========================================

if not link_API:

    st.error("URL da API não encontrada. Verifique o arquivo .env.")

else:

    # ==========================================
    # 8. EXPLORAR PUBLICACOES
    # ==========================================

    if pagina == "Explorar publicações":

        try:

            resposta = requests.get(link_API, timeout=15)

            if resposta.status_code == 200:

                dados = resposta.json()

                st.subheader("🌌 Explore as publicações")

                total_imagens = sum(
                    1 for item in dados
                    if item.get("media_type") == "image"
                )

                total_videos = sum(
                    1 for item in dados
                    if item.get("media_type") == "video"
                )

                coluna1, coluna2, coluna3 = st.columns(3)

                coluna1.metric("Publicações", len(dados))
                coluna2.metric("Imagens", total_imagens)
                coluna3.metric("Vídeos", total_videos)

                st.divider()

                coluna_filtro, coluna_pesquisa = st.columns([1, 2])

                with coluna_filtro:

                    tipo = st.selectbox(
                        "Tipo de conteúdo:",
                        ["Todas", "Imagens", "Vídeos"]
                    )

                with coluna_pesquisa:

                    pesquisa = st.text_input(
                        "Pesquisar publicação:",
                        placeholder="Digite o título..."
                    )

                st.divider()

                publicacoes_filtradas = []

                for publicacao in dados:

                    tipo_midia = publicacao.get("media_type")
                    titulo = publicacao.get("title", "")

                    if tipo == "Imagens" and tipo_midia != "image":
                        continue

                    if tipo == "Vídeos" and tipo_midia != "video":
                        continue

                    if pesquisa.lower() not in titulo.lower():
                        continue

                    publicacoes_filtradas.append(publicacao)

                st.write(
                    "Resultados encontrados:",
                    len(publicacoes_filtradas)
                )

                contador = 0

                for publicacao in publicacoes_filtradas:

                    if contador % 3 == 0:
                        colunas = st.columns(3)

                    with colunas[contador % 3]:

                        with st.container(border=True):

                            mostrar_publicacao(publicacao)

                    contador += 1

                if contador == 0:

                    st.warning("Nenhuma publicação encontrada.")

            else:

                st.error("Não foi possível acessar a API da NASA.")
                st.write("Código HTTP:", resposta.status_code)

        except requests.exceptions.RequestException as erro:

            st.error("Erro ao conectar com a API.")
            st.write(erro)


    # ==========================================
    # 9. VIAGEM NO TEMPO
    # ==========================================

    elif pagina == "Viagem no tempo":

        st.subheader("🪐 Viagem no tempo")

        st.write(
            "Escolha uma data ou descubra uma publicação "
            "astronômica aleatória."
        )

        st.divider()

        st.markdown("### 📅 Escolha uma data")

        data_escolhida = st.date_input(
            "Selecione o dia:",
            value=date.today(),
            min_value=date(1995, 6, 16),
            max_value=date.today(),
            format="DD/MM/YYYY"
        )

        if st.button(
            "🔎 Buscar publicação desta data",
            use_container_width=True
        ):

            try:

                resposta = requests.get(
                    link_API,
                    params={"date": data_escolhida.isoformat()},
                    timeout=15
                )

                if resposta.status_code == 200:

                    dados = resposta.json()

                    if isinstance(dados, list):
                        publicacao = dados[0] if dados else None
                    else:
                        publicacao = dados

                    if publicacao and publicacao.get("title"):

                        st.success("Publicação encontrada!")

                        st.divider()

                        mostrar_publicacao(publicacao)

                    else:

                        st.warning("Nenhuma publicação encontrada.")

                else:

                    st.error("Não foi possível consultar essa data.")
                    st.write("Código HTTP:", resposta.status_code)

            except requests.exceptions.RequestException as erro:

                st.error("Erro ao conectar com a NASA.")
                st.write(erro)

        st.divider()

        st.markdown("### 🎲 Descubra algo aleatório")

        st.write(
            "Deixe a NASA escolher uma publicação para você."
        )

        if st.button(
            "✨ Descobrir publicação aleatória",
            use_container_width=True
        ):

            try:

                resposta = requests.get(
                    link_API,
                    params={"count": 1},
                    timeout=15
                )

                if resposta.status_code == 200:

                    dados = resposta.json()

                    if isinstance(dados, list):
                        publicacao = dados[0] if dados else None
                    else:
                        publicacao = dados

                    if publicacao and publicacao.get("title"):

                        st.success("Sua descoberta foi encontrada!")

                        st.divider()

                        mostrar_publicacao(publicacao)

                    else:

                        st.warning("Nenhuma publicação encontrada.")

                else:

                    st.error("Não foi possível buscar uma publicação.")
                    st.write("Código HTTP:", resposta.status_code)

            except requests.exceptions.RequestException as erro:

                st.error("Erro ao conectar com a NASA.")
                st.write(erro)


    # ==========================================
    # 10. SOBRE O PROJETO
    # ==========================================

    elif pagina == "Sobre o projeto":

        st.subheader("🪐 Sobre o NASA Explorer")

        st.write("""
        O NASA Explorer é uma aplicação desenvolvida em Python
        que consome uma API da NASA para apresentar publicações
        relacionadas à astronomia e ao universo.
        """)

        st.divider()

        st.markdown("### 🎯 Objetivo")

        st.write("""
        Facilitar o acesso a imagens, vídeos e informações
        disponibilizadas pela NASA.
        """)

        st.markdown("### ⚙️ Como funciona?")

        st.write("""
        1. Python realiza uma requisição para a API.
        2. A API retorna os dados em formato JSON.
        3. O programa interpreta as informações.
        4. O Streamlit apresenta os resultados.
        """)

        st.markdown("### 🌌 Funcionalidades")

        st.write("""
        - Explorar publicações astronômicas.
        - Filtrar imagens e vídeos.
        - Pesquisar pelo título.
        - Consultar publicações por data.
        - Descobrir publicações aleatórias.
        - Visualizar descrições sem as marcações HTML.
        """)

        st.markdown("### 🛠️ Tecnologias utilizadas")

        st.write("""
        - Python
        - Requests
        - Streamlit
        - python-dotenv
        - HTMLParser
        - API da NASA
        """)

        st.divider()

        st.markdown("### 🌐 API utilizada")

        st.code(link_API)

        st.link_button("Acessar API ↗", link_API)

        st.info(
            "As publicações e informações são fornecidas pela NASA. "
            "O NASA Explorer organiza e apresenta esses conteúdos "
            "em uma interface interativa."
        )
