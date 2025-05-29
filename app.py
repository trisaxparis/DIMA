import streamlit as st
import pandas as pd

# Chargement des données
df_titres = pd.read_csv("table_de_titres manipulatifs10.csv", sep=";")
df_biais = pd.read_csv("biais_complet.csv")  # Ce fichier doit contenir les colonnes mentionnées

# Initialisation
if "biais_index" not in st.session_state:
    st.session_state.biais_index = 0

if "annotations" not in st.session_state:
    st.session_state.annotations = {}

# Navigation entre biais
biais_list = df_biais["nom"].tolist()
current_biais = df_biais.iloc[st.session_state.biais_index]

# Affichage du biais
st.title("Annotation de biais cognitifs dans les titres")
st.subheader(f"Biais : {current_biais['nom']}")
st.markdown(f"**Définition :** {current_biais['definition_operationnelle']}")
st.markdown(f"**Structure cognitive :** {current_biais['structure_cognitive_typique']}")

# Annotation des titres
st.markdown("---")
st.subheader("Titres à annoter")

for i, row in df_titres.head(10).iterrows():
    titre = row["Titre"]
    unique_id = f"{current_biais['nom']}_{i}"
    st.markdown(f"**{i+1}.** {titre}")
    st.radio(
        f"Annotation pour ce titre [{i+1}]",
        ["Non", "Doute", "Oui"],
        key=unique_id,
        horizontal=True
    )

# Boutons de navigation
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("⬅️ Biais précédent", disabled=st.session_state.biais_index == 0):
        st.session_state.biais_index -= 1

with col2:
    if st.button("➡️ Biais suivant", disabled=st.session_state.biais_index == len(biais_list) - 1):
        st.session_state.biais_index += 1

with col3:
    if st.button("💾 Sauvegarder les annotations"):
        annotations = []
        for i in df_titres.head(10).index:
            unique_id = f"{current_biais['nom']}_{i}"
            annotations.append({
                "biais": current_biais['nom'],
                "titre": df_titres.loc[i, "Titre"],
                "annotation": st.session_state.get(unique_id, "Non")
            })
        df_out = pd.DataFrame(annotations)
        df_out.to_csv("annotations_temp.csv", index=False)
        st.success("Annotations sauvegardées dans annotations_temp.csv")
