import streamlit as st
import pandas as pd
import os

# ─── 1) CONFIGURATION DE LA PAGE ─────────────────────────────────────
st.set_page_config(page_title="Annotation biais", layout="wide")

# ─── 2) CHARGEMENT DES FICHIERS CSV ─────────────────────────────────
titre_path = "titres_manipulatifs10.csv"
biais_path = "biais_complet_final_questions.csv"

if not os.path.exists(titre_path) or not os.path.exists(biais_path):
    st.error("Fichiers manquants. Vérifie la présence des fichiers nécessaires.")
    st.stop()

df_titres = pd.read_csv(titre_path, sep=";")
df_biais = pd.read_csv(biais_path)

# ─── 3) INITIALISATION SESSION ──────────────────────────────────────
if "biais_index" not in st.session_state:
    st.session_state.biais_index = 0

# ─── 4) RÉCUPÉRATION DU BIAIS COURANT ───────────────────────────────
current_biais = df_biais.iloc[st.session_state.biais_index]
nom_biais = current_biais["nom"]

# ─── 5) MISE EN PAGE EN DEUX COLONNES ───────────────────────────────
col_question, col_annotation = st.columns([1.2, 2.8], gap="large")

# ────── Colonne de gauche : question + définition
with col_question:
    st.markdown("## ❓ Question d’annotation")
    st.markdown(f"**{current_biais['question_annotation']}**")

    with st.expander("ℹ️ Voir la définition du biais si nécessaire"):
        st.markdown(current_biais["definition_operationnelle"])

# ────── Colonne de droite : annotation des titres
with col_annotation:
    st.markdown("## Titres à annoter")
    annotations = []

    for i, row in df_titres.head(10).iterrows():
        titre = row["Titre"]
        key = f"{nom_biais}_{i}"
        st.markdown(f"**{i+1}.** {titre}")
        choix = st.radio(
            "Sélectionner une option :",
            ["", "Oui", "Doute", "Non"],
            index=0,
            key=key,
            horizontal=True
        )
        annotations.append({
            "titre": titre,
            "biais": nom_biais,
            "annotation": choix
        })

    st.divider()

    # ────── Navigation et sauvegarde
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
