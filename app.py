from pathlib import Path
import pandas as pd
import streamlit as st
import os

# Redémarrage contrôlé
if "trigger_rerun" not in st.session_state:
    st.session_state.trigger_rerun = False
elif st.session_state.trigger_rerun:
    st.session_state.trigger_rerun = False
    st.rerun()

# CONFIG
st.set_page_config(page_title="Annotation biais", layout="wide")

# PATHS
titre_path = "titres_manipulatifs10.csv"
biais_path = "biais_complet_avec_questions.csv"
save_path = "annotations_global.csv"

def main():
    # CHARGEMENT
    if not os.path.exists(titre_path) or not os.path.exists(biais_path):
        st.error("Fichiers manquants.")
        st.stop()

    df_titres_complet = pd.read_csv(titre_path, sep=";")
    df_biais = pd.read_csv(biais_path)

    # BOUTON DE RÉINITIALISATION
    if st.sidebar.button("🧹 Réinitialiser tout"):
        if os.path.exists(save_path):
            os.remove(save_path)
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.experimental_rerun()

    # INITIALISATION SESSION
    if "biais_index" not in st.session_state:
        st.session_state.biais_index = 0
    if "titres_random" not in st.session_state or st.session_state.get("reset_titres", False):
        nb_titres = min(10, len(df_titres_complet))
        st.session_state.titres_random = df_titres_complet.sample(n=nb_titres).reset_index(drop=True)
        st.session_state.reset_titres = False

    # IDENTIFICATION ANNOTATEUR
    if "initiales" not in st.session_state or not st.session_state.initiales:
        initiales = st.sidebar.text_input("🖊️ Vos initiales :")
        if initiales:
            st.session_state.initiales = initiales
            st.session_state.trigger_rerun = True
            st.rerun()
        else:
            st.title("🧠 Annotation des biais cognitifs")
            st.warning("Merci de saisir vos initiales dans la colonne de gauche pour commencer.")
            st.stop()
    else:
        st.sidebar.markdown(f"👤 Annotateur : **{st.session_state.initiales}**")

    # COURANT
    biais_index = st.session_state.biais_index
    current_biais = df_biais.iloc[biais_index]
    nom_biais = current_biais["nom"]

 ​:contentReference[oaicite:0]{index=0}​
