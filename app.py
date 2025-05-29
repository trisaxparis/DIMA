import streamlit as st
import pandas as pd
import os

# 1. CONFIG
st.set_page_config(page_title="Annotation biais", layout="wide")

# 2. REDIRECTION SÛRE PAR FLAG
if "redirect" in st.session_state:
    del st.session_state["redirect"]
    st.experimental_rerun()

# 3. CHARGEMENT DES FICHIERS
titre_path = "titres_manipulatifs10.csv"
biais_path = "biais_complet_avec_questions.csv"

if not os.path.exists(titre_path) or not os.path.exists(biais_path):
    st.error("Fichiers manquants.")
    st.stop()

df_titres = pd.read_csv(titre_path, sep=";")
df_biais = pd.read_csv(biais_path)

# 4. SESSION STATE INIT
if "biais_index" not in st.session_state:
    st.session_state.biais_index = 0

biais_index = st.session_state.biais_index
current_biais = df_biais.iloc[biais_index]
nom_biais = current_biais["nom"]

# 5. SIDEBAR : question + définition
with st.sidebar:
    st.markdown("## ❓ Question d’annotation")
    st.markdown(f"{current_biais['question_annotation']}")
    with st.expander(f"ℹ️ Définition du biais : {nom_biais}"):
        st.markdown(current_biais["definition_operationnelle"])

# 6. AFFICHAGE DES TITRES
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

# 7. VALIDATION
def tous_titres_annotés():
    return all(a["annotation"] in ["Oui", "Doute", "Non"] for a in annotations)

# 8. BOUTONS ACTIONS
st.divider()
col1, col2, col3 = st.columns([1, 1, 2])

def clear_radios():
    for i in range(10):
        key = f"{nom_biais}_{i}"
        if key in st.session_state:
            del st.session_state[key]

with col1:
    if st.button("⬅️ Biais précédent", disabled=biais_index == 0):
        if tous_titres_annotés():
            pd.DataFrame(annotations).to_csv(
                f"annotations_{nom_biais.replace(' ', '_')}.csv", index=False
            )
            clear_radios()
            st.session_state.biais_index -= 1
            st.session_state["redirect"] = True
        else:
            st.warning("⚠️ Merci d’annoter chaque titre avant de continuer.")

with col2:
    if st.button("➡️ Biais suivant", disabled=biais_index == len(df_biais) - 1):
        if tous_titres_annotés():
            pd.DataFrame(annotations).to_csv(
                f"annotations_{nom_biais.replace(' ', '_')}.csv", index=False
            )
            clear_radios()
            st.session_state.biais_index += 1
            st.session_state["redirect"] = True
        else:
            st.warning("⚠️ Merci d’annoter chaque titre avant de continuer.")

with col3:
    if st.button("💾 Sauvegarder"):
        if tous_titres_annotés():
            pd.DataFrame(annotations).to_csv(
                f"annotations_{nom_biais.replace(' ', '_')}.csv", index=False
            )
            st.success("🔖 Annotations sauvegardées !")
        else:
            st.warning("⚠️ Merci d’annoter tous les titres avant de sauvegarder.")
