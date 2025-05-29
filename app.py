import streamlit as st
import pandas as pd
import os

# CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Annotation biais", layout="wide")

# CHEMINS VERS LES FICHIERS
titre_path = "titres_manipulatifs10.csv"
biais_path = "biais_modifie_interface.csv"
save_path = "annotations_global.csv"

# CHARGEMENT DES FICHIERS
if not os.path.exists(titre_path) or not os.path.exists(biais_path):
    st.error("Fichiers manquants.")
    st.stop()

df_titres = pd.read_csv(titre_path, sep=";")
df_biais = pd.read_csv(biais_path)

# ÉTAT DE SESSION : INDEX DU BIAIS
if "biais_index" not in st.session_state:
    st.session_state.biais_index = 0

biais_index = st.session_state.biais_index
current_biais = df_biais.iloc[biais_index]
nom_biais = current_biais["nom"]

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR : QUESTION + DÉFINITION
with st.sidebar:
    st.markdown("## ❓ Question")
    st.markdown(f"**{current_biais['question_annotation']}**")
    with st.expander("ℹ️ Définition du biais"):
        st.markdown(current_biais["definition_operationnelle"])

# ─────────────────────────────────────────────────────────────────────────────
# AFFICHAGE : COMPTEUR ET TITRES
st.markdown(f"### Biais {biais_index + 1} / {len(df_biais)}")

annotations = []
for i, row in df_titres.head(10).iterrows():
    titre = row["Titre"]
    key = f"{nom_biais}_{i}"
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
        "biais": nom_biais,
        "annotation": choix
    })

# ─────────────────────────────────────────────────────────────────────────────
# VALIDATION
def tous_titres_annotes():
    return all(a["annotation"] in ["Oui", "Doute", "Non"] for a in annotations)

# ─────────────────────────────────────────────────────────────────────────────
# NAVIGATION
st.divider()
col1, col2 = st.columns([1, 4])

with col1:
    st.markdown("### Navigation")

with col2:
    if st.button("➡️ Biais suivant"):
        if tous_titres_annotes():
            df_save = pd.DataFrame(annotations)

            if os.path.exists(save_path):
                df_existing = pd.read_csv(save_path)
                df_concat = pd.concat([df_existing, df_save], ignore_index=True)
            else:
                df_concat = df_save

            df_concat.to_csv(save_path, index=False)

            # Nettoyer les radios de ce biais
            for i in range(10):
                key = f"{nom_biais}_{i}"
                if key in st.session_state:
                    del st.session_state[key]

            # Avancer si ce n’est pas le dernier biais
            if biais_index < len(df_biais) - 1:
                st.session_state.biais_index += 1
                st.experimental_rerun()
            else:
                st.success("🎉 Tous les biais ont été annotés.")
        else:
            st.warning("⚠️ Merci d’annoter tous les titres avant de passer au suivant.")
