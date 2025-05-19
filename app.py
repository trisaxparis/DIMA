import streamlit as st
import pandas as pd
import random
import io

# --- Chargement des données ---
biais_df = pd.read_csv("biais.csv", dtype={"index_biais": str})
titres_df = pd.read_csv("titres.csv", sep=";")

# --- Initialisation session state ---
if "annotations" not in st.session_state:
    st.session_state.annotations = []
if "current_biais" not in st.session_state:
    st.session_state.current_biais = None
if "current_titles" not in st.session_state:
    st.session_state.current_titles = []

# --- Titre de l'application ---
st.title("Annotation de biais cognitifs dans les titres de presse")

# --- Entrée du nom de l'annotateur ---
annotateur = st.text_input("Entrez votre nom d'annotateur :")

# --- Bouton pour générer un biais et 5 titres ---
if annotateur:
    if st.button("Générer un biais et 5 titres"):
        st.session_state.current_biais = random.choice(biais_df['index_biais'].tolist())
        st.session_state.current_titles = titres_df.sample(5).Titre.tolist()

    # --- Affichage du biais et des titres côte à côte ---
    if st.session_state.current_biais:
        biais_info = biais_df[biais_df['index_biais'] == st.session_state.current_biais].iloc[0]

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"Biais à évaluer : {biais_info['nom']} ({biais_info['index_biais']})")
            for col in ['mecanisme', 'declencheurs', 'exemple', 'faux_positif', 'validation']:
                st.markdown(f"**{col.capitalize().replace('_', ' ')} :**  \n{biais_info[col]}")
                st.markdown("")  # ligne vide

        with col2:
            selected_titles = []
            st.subheader("Titres à annoter")
            for i, titre in enumerate(st.session_state.current_titles):
                if st.checkbox(titre, key=f"titre_{i}"):
                    selected_titles.append(titre)

            # --- Bouton de validation ---
            if st.button("Enregistrer l'annotation"):
                for titre in selected_titles:
                    st.session_state.annotations.append({
                        "annotateur": annotateur,
                        "biais": st.session_state.current_biais,
                        "nom_biais": biais_info['nom'],
                        "titre": titre
                    })
                st.success("Annotations enregistrées !")

    # --- Export des annotations ---
    if st.session_state.annotations:
        df_export = pd.DataFrame(st.session_state.annotations)
        buffer = io.StringIO()
        df_export.to_csv(buffer, index=False)
        st.download_button("Télécharger les annotations", data=buffer.getvalue(), file_name="annotations.csv", mime="text/csv")
else:
    st.info("Veuillez entrer votre nom pour commencer.")
