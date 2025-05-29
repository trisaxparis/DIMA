import streamlit as st
import pandas as pd
import os

# Configuration de la page
st.set_page_config(page_title="Annotation de biais cognitifs", layout="centered")

# Chargement des données avec vérification
titre_path = "titres_manipulatifs10.csv"
biais_path = "biais_complet.csv"

if not os.path.exists(titre_path) or not os.path.exists(biais_path):
    st.error("Fichiers manquants. Vérifie que 'titres_manipulatifs10.csv' et 'biais_complet.csv' sont bien présents.")
    st.stop()

df_titres = pd.read_csv(titre_path, sep=";")
df_biais = pd.read_csv(biais_path)

# Initialisation de la session
if "biais_index" not in st.session_state:
    st.session_state.biais_index = 0
if "annotations" not in st.session_state:
    st.session_state.annotations = {}

# Variables utiles
biais_list = df_biais["nom"].tolist()
current_biais = df_biais.iloc[st.session_state.biais_index]
nom_biais = current_biais["nom"]

# Affichage du biais sélectionné
st.title("🧠 Annotation de biais cognitifs")
st.markdown(f"### Biais analysé : {nom_biais}")
st.info(f"**Définition :** {current_biais['definition_operationnelle']}")
st.markdown(f"**Structure cognitive :** {current_biais['structure_cognitive_typique']}")

st.divider()

# Annotation de 10 titres
st.markdown("### Titres à annoter (10 affichés)")
annotations = []

for i, row in df_titres.head(10).iterrows():
    titre = row["Titre"]
    unique_key = f"{nom_biais}_{i}"
    st.markdown(f"**{i+1}.** {titre}")
    annotation = st.radio(
    f"Ce biais est-il présent dans ce titre ?",
    ["", "Oui", "Doute", "Non"],
    index=0,
    key=unique_key,
    horizontal=True
)
    annotations.append({
        "titre": titre,
        "biais": nom_biais,
        "annotation": annotation,
    })

st.divider()

# Navigation entre biais
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("⬅️ Biais précédent", disabled=st.session_state.biais_index == 0):
        st.session_state.biais_index -= 1
        st.experimental_rerun()

with col2:
    if st.button("➡️ Biais suivant", disabled=st.session_state.biais_index == len(biais_list) - 1):
        st.session_state.biais_index += 1
        st.experimental_rerun()

with col3:
    if st.button("💾 Sauvegarder les annotations"):
        df_save = pd.DataFrame(annotations)
        save_path = f"annotations_{nom_biais.replace(' ', '_')}.csv"
        df_save.to_csv(save_path, index=False)
        st.success(f"Annotations sauvegardées dans `{save_path}`")

