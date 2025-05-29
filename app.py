import streamlit as st
import pandas as pd
import os

# CONFIG
st.set_page_config(page_title="Annotation biais", layout="wide")

# Chargement des fichiers
titre_path = "titres_manipulatifs10.csv"
biais_path = "biais_modifie_interface.csv"

if not os.path.exists(titre_path) or not os.path.exists(biais_path):
    st.error("Fichiers manquants. Assure-toi que les deux fichiers sont présents.")
    st.stop()

df_titres = pd.read_csv(titre_path, sep=";")
df_biais = pd.read_csv(biais_path)

# Sélection du biais
liste_biais = df_biais["nom"].tolist()
biais_selectionne = st.selectbox("Choisissez un biais à annoter :", liste_biais)
current_biais = df_biais[df_biais["nom"] == biais_selectionne].iloc[0]

# Sidebar : question + définition
with st.sidebar:
    st.markdown("## ❓ Question")
    st.markdown(f"**{current_biais['question_annotation']}**")
    with st.expander("ℹ️ Définition du biais"):
        st.markdown(current_biais["definition_operationnelle"])

# Affichage des titres
st.markdown("## Titres à annoter")

annotations = []
for i, row in df_titres.head(10).iterrows():
    titre = row["Titre"]
    key = f"{biais_selectionne}_{i}"
    st.markdown(f"**{i+1}.** {titre}")
    choix = st.radio(
        "Réponse :",
        ["", "Oui", "Doute", "Non"],
        index=0,
        key=key,
        horizontal=True
    )
    annotations.append({
        "titre": titre,
        "biais": biais_selectionne,
        "annotation": choix
    })

# Vérification
def tous_titres_annotes():
    return all(a["annotation"] in ["Oui", "Doute", "Non"] for a in annotations)

# Sauvegarde
if st.button("💾 Sauvegarder les annotations"):
    if tous_titres_annotes():
        df_save = pd.DataFrame(annotations)
        save_path = "annotations_global.csv"

        if os.path.exists(save_path):
            df_existing = pd.read_csv(save_path)
            df_concat = pd.concat([df_existing, df_save], ignore_index=True)
        else:
            df_concat = df_save

        df_concat.to_csv(save_path, index=False)
        st.success("✅ Annotations sauvegardées dans `annotations_global.csv`")
    else:
        st.warning("⚠️ Merci d’annoter tous les titres avant de sauvegarder.")
