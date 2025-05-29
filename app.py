import streamlit as st
import pandas as pd
import os

# Configuration de la page
st.set_page_config(page_title="Annotation biais", layout="centered")

# Chargement des fichiers nécessaires
titre_path = "titres_manipulatifs10.csv"
biais_path = "biais_complet_final_questions.csv"

if not os.path.exists(titre_path) or not os.path.exists(biais_path):
    st.error("Fichiers manquants. Vérifie la présence de 'titres_manipulatifs10.csv' et 'biais_complet_final_questions.csv'.")
    st.stop()

df_titres = pd.read_csv(titre_path, sep=";")
df_biais = pd.read_csv(biais_path)

# Initialiser la session
if "biais_index" not in st.session_state:
    st.session_state.biais_index = 0
if "annotations" not in st.session_state:
    st.session_state.annotations = {}

# Récupérer le biais courant
current_biais = df_biais.iloc[st.session_state.biais_index]
nom_biais = current_biais["nom"]

# Affichage simplifié : uniquement la question et la définition sur demande
st.markdown("### ❓ Question d’annotation")
st.success(current_biais["question_annotation"])

with st.expander("ℹ️ Voir la définition du biais si nécessaire"):
    st.markdown(current_biais["definition_operationnelle"])

st.divider()

# Annotation des titres (10 premiers)
annotations = []

for i, row in df_titres.head(10).iterrows():
    titre = row["Titre"]
    unique_key = f"{nom_biais}_{i}"
    st.markdown(f"**{i+1}.** {titre}")
    annotation = st.radio(
        "Sélectionner une option :",
        ["", "Oui", "Doute", "Non"],
        index=0,
        key=unique_key,
        horizontal=True
    )
    annotations.append({
        "titre": titre,
        "biais": nom_biais,
        "annotation": annotation
    })

st.divider()

# Navigation entre biais et sauvegarde
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
    if st.button("💾 Sauvegarder les annotations"):
        df_save = pd.DataFrame(annotations)
        save_path = f"annotations_{nom_biais.replace(' ', '_')}.csv"
        df_save.to_csv(save_path, index=False)
        st.success(f"Annotations sauvegardées dans `{save_path}`")
