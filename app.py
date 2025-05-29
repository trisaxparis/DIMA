import streamlit as st
import pandas as pd
import os

# ─── 1. CONFIGURATION STREAMLIT ──────────────────────────────────────
st.set_page_config(page_title="Annotation biais", layout="wide")

# ─── 2. CHARGEMENT DES FICHIERS ──────────────────────────────────────
titre_path = "titres_manipulatifs10.csv"
biais_path = "biais_complet_avec_questions.csv"  # <- NOM FIXE ICI

if not os.path.exists(titre_path) or not os.path.exists(biais_path):
    st.error("Fichiers manquants. Vérifie la présence des CSV dans le dossier.")
    st.stop()

df_titres = pd.read_csv(titre_path, sep=";")
df_biais = pd.read_csv(biais_path)

# ─── 3. SESSION STATE ────────────────────────────────────────────────
if "biais_index" not in st.session_state:
    st.session_state.biais_index = 0

# ─── 4. RÉCUPÉRATION DU BIAIS ACTUEL ─────────────────────────────────
current_biais = df_biais.iloc[st.session_state.biais_index]
nom_biais = current_biais["nom"]

# ─── 5. SIDEBAR : QUESTION D’ANNOTATION FIXE ─────────────────────────
with st.sidebar:
    st.markdown("## ❓ Question d’annotation")
    st.markdown(f"{current_biais['question_annotation']}")
    st.markdown("---")
    with st.expander("ℹ️ Voir la définition du biais si nécessaire"):
        st.markdown(current_biais["definition_operationnelle"])

# ─── 6. COLONNE PRINCIPALE : ANNOTATION DES TITRES ───────────────────
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

# ─── 7. NAVIGATION & SAUVEGARDE ──────────────────────────────────────
st.divider()
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("⬅️ Biais précédent", disabled=st.session_state.biais_index == 0):
        if any(a["annotation"] for a in annotations if a["annotation"]):
            pd.DataFrame(annotations).to_csv(
                f"annotations_{nom_biais.replace(' ', '_')}.csv",
                index=False
            )
        st.session_state.biais_index -= 1
        st.experimental_rerun()

with col2:
    if st.button("➡️ Biais suivant", disabled=st.session_state.biais_index == len(df_biais) - 1):
        if any(a["annotation"] for a in annotations if a["annotation"]):
            pd.DataFrame(annotations).to_csv(
                f"annotations_{nom_biais.replace(' ', '_')}.csv",
                index=False
            )
        st.session_state.biais_index += 1
        st.experimental_rerun()

with col3:
    if st.button("💾 Sauvegarder"):
        valid_annotations = [a for a in annotations if a["annotation"]]
        if valid_annotations:
            pd.DataFrame(valid_annotations).to_csv(
                f"annotations_{nom_biais.replace(' ', '_')}.csv",
                index=False
            )
            st.success("🔖 Annotations sauvegardées !")
        else:
            st.warning("Aucune annotation à sauvegarder.")
