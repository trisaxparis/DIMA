import streamlit as st
import pandas as pd
import os

# Configuration de la page
st.set_page_config(page_title="Annotation biais", layout="centered")

# Chargement des fichiers nécessaires
titre_path = "titres_manipulatifs10.csv"
biais_path = "biais_complet_avec_questions.csv"

if not os.path.exists(titre_path) or not os.path.exists(biais_path):
    st.error("Fichiers manquants. Vérifie la présence de 'titres_manipulatifs10.csv' et 'biais_complet_final_questions.csv'.")
    st.stop()

df_titres = pd.read_csv(titre_path, sep=";")
df_biais = pd.read_csv(biais_path)

# Initialisation des variables de session
if "biais_index" not in st.session_state:
    st.session_state.biais_index = 0
if "annotations" not in st.session_state:
    st.session_state.annotations = {}

# Récupération du biais courant
current_biais = df_biais.iloc[st.session_state.biais_index]
nom_biais = current_biais["nom"]

# Bloc HTML sticky réaliste en Streamlit (simulateur sticky en haut de page)
st.markdown("""
    <style>
        .sticky-header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            padding: 1rem;
            background-color: #f9f9fa;
            border-bottom: 1px solid #ccc;
            z-index: 9999;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .content-offset {
            margin-top: 120px;
        }
    </style>
    <div class="sticky-header">
        <strong>❓ Question d’annotation :</strong><br>
        <span style="font-size: 1.1rem;">""" + current_biais["question_annotation"] + """</span>
    </div>
    <div class="content-offset"></div>
""", unsafe_allow_html=True)


# Définition du biais dans un expander
with st.expander("ℹ️ Voir la définition du biais si nécessaire"):
    st.markdown(current_biais["definition_operationnelle"])

st.divider()

# Annotation des 10 premiers titres
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
