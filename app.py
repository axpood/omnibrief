# ==============================================================
# OMNIBRIEF — BLOC 4 : LA VITRINE WEB
# app.py — Page principale du site Streamlit
# ==============================================================

import html
import streamlit as st
import pandas as pd

st.set_page_config(page_title="OmniBrief", page_icon="🗞️", layout="centered")

# Couleur d'accent propre à chaque catégorie, dans une palette encre/papier
# plutôt que les couleurs vives génériques d'une interface web classique.
COULEURS_CATEGORIE = {
    "Économie": "#1F4E5F",
    "Géopolitique": "#5C3A5C",
    "Sport": "#2F5233",
}

# CSS personnalisé : on quitte entièrement le thème Streamlit par défaut
# pour une identité visuelle propre à OmniBrief.
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,400;0,600;1,400&family=Inter:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #FCFCFB;
        color: #2B2A26;
    }
    #MainMenu, footer, header {visibility: hidden;}

    .logo {
        font-family: 'Newsreader', serif;
        font-weight: 600;
        font-size: 2.4rem;
        letter-spacing: -0.5px;
        border-bottom: 2px solid #2B2A26;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    .categorie-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        font-weight: 500;
    }
    .titre-vedette {
        font-family: 'Newsreader', serif;
        font-weight: 600;
        font-size: 2rem;
        line-height: 1.25;
        margin: 0.4rem 0 0.6rem 0;
    }
    .titre-secondaire {
        font-family: 'Newsreader', serif;
        font-weight: 600;
        font-size: 1.3rem;
        margin: 0.3rem 0 0.4rem 0;
    }
    .source { font-size: 0.85rem; color: #6B6A64; margin: 0 0 0.6rem 0; }
    .resume { font-size: 1rem; line-height: 1.6; }
    .vedette, .article-secondaire {
        padding-bottom: 1.4rem;
        border-bottom: 1px solid #DAD8D2;
        margin-bottom: 1.4rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def charger_articles() -> pd.DataFrame:
    """Charge les articles depuis le CSV et ne garde que ceux jugés pertinents."""
    df = pd.read_csv("dernier_export.csv")
    return df[df["pertinent"] == True].reset_index(drop=True)


def rendre_article(article: pd.Series, style_classe: str, titre_classe: str) -> None:
    """Affiche un article en HTML, en échappant le texte pour éviter tout souci
    si un titre RSS contient des caractères spéciaux (<, >, &...)."""
    couleur = COULEURS_CATEGORIE.get(article["categorie"], "#2B2A26")
    st.markdown(f"""
    <div class="{style_classe}">
        <span class="categorie-label" style="color:{couleur};">{html.escape(article['categorie'])}</span>
        <h1 class="{titre_classe}">{html.escape(article['titre'])}</h1>
        <p class="source">{html.escape(article['source'])}</p>
        <p class="resume">{html.escape(article['resume_ia'])}</p>
    </div>
    """, unsafe_allow_html=True)


# --- Construction de la page ---
st.markdown("<div class='logo'>OmniBrief</div>", unsafe_allow_html=True)

df = charger_articles()

categories = ["Toutes"] + sorted(df["categorie"].unique().tolist())
choix = st.selectbox("Filtrer par catégorie", categories)
if choix != "Toutes":
    df = df[df["categorie"] == choix]

if df.empty:
    st.write("Aucun article disponible pour cette catégorie.")
else:
    rendre_article(df.iloc[0], "vedette", "titre-vedette")
    for _, article in df.iloc[1:].iterrows():
        rendre_article(article, "article-secondaire", "titre-secondaire")
