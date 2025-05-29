import streamlit as st
import pandas as pd
import os

# ─── 1) CONFIGURATION STREAMLIT ─────────────────────────────────────────────────
st.set_page_config(page_title="Annotation biais", layout="wide")

# ─── 2) INJECTION CSS POUR BANDEAU STICKY ───────────────────────────────────────
st.markdown("""
    <style>
        .main .block-container {
            padding-top: 0 !important;
        }
        .sticky-question {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            padding: 1rem 2rem;
            background-color: white;
            border-bottom: 1px solid #ccc;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            z-index: 9999;
        }
        .spacer {
            height: 100px;
        }
    </style>
""", unsafe_allow_html=True)

# ─── 3) CHARGEMENT DES FICHIERS ─────────────────────────────────────────────────
titre_path = "titres_manipulatifs10.csv"
biais_path = "biais_complet_avec_questions.csv"

if not os.path.exists(titre_path) or not os.path.exists(biais_path):
    st.error("Fichiers manquants. Vérifie que les CSV sont bien présents.")
    st.stop()

df_titres = pd.read_csv(titre_path, sep=";")
df_biais = pd.read_csv(biais_path)

# ─── 4) INITIALISATION DE LA SESSION ─────────────────────────────────────────────
if "biais_index" not in st.session_state:
    st.session_state.biais_index = 0

# ─── 5) RÉCUPÉRATION DU BIAIS ACTIF ──────────────────────────────────────────────
current_biais = df_biais.iloc[st.session_state.biais_index]
nom_biais = current_biais["nom"]

# ─── 6) AFFICHE LE BANDEAU STICKY ───────────────────────────────────────────────
st.markdown(f"""
    <div class="sticky-question">
        <strong>❓ Question d’annotation :</strong><br>
        <span style="font-size:1.1rem;">{current_biais["question_annotation"]}</span>
    </div>
    <div class="spacer"></div>
""", unsafe_allow_html=True)

# ─── 7) DÉFINITION EN EXPANDER ───────────────────────────────────────────────────
with st.expander("ℹ️ Voir la définition du biais si nécessaire"):
    st.markdown(current_biais["definition_operationnelle"])

st.divider()

# ─── 8) AFFICHAGE DES 10 PREMIERS TITRES ────────────────────────────────────────
annotations = []
for i, row in df_titres.head(10).iterrows():
    titre = row["Titre"]
    key = f"{nom_biais}_{i}"
    st.markdown(f"**{i+1}.** {titre}")
    choix = st.radio(
        "", ["", "Oui", "Doute", "Non"],
        index=0, key=key, horizontal=True
    )
    annotations.append({
        "titre": titre,
        "biais": nom_biais,
        "annotation": choix
    })

st.divider()

# ─── 9) NAVIGATION & SAUVEGARDE ─────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("⬅️ Biais précédent", disabled=st.session_state.biais_index == 0):
        st.session_state.biais_index -= 1
        st.experimental_rerun()
with col2:
    if st.button("➡️ Biais suivant", disabled=st.session_state.biais_index == len(df_biais) - 1):
        st.session_state.biais_index += 1
        st.experimental_rerun()
with col3:
    if st.button("💾 Sauvegarder"):
        pd.DataFrame(annotations).to_csv(
            f"annotations_{nom_biais.replace(' ', '_')}.csv",
            index=False
        )
        st.success("🔖 Annotations sauvegardées !")
