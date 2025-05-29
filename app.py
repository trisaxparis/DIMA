import streamlit as st
import pandas as pd
import os

# Redémarrage automatique après changement d’état
if "trigger_rerun" in st.session_state and st.session_state.trigger_rerun:
    st.session_state.trigger_rerun = False
    st.rerun()

# CONFIG
st.set_page_config(page_title="Annotation biais", layout="wide")

# PATHS
titre_path = "titres_manipulatifs10.csv"
biais_path = "biais_modifie_interface.csv"
save_path = "annotations_global.csv"

def main():
    # CHARGEMENT
    if not os.path.exists(titre_path) or not os.path.exists(biais_path):
        st.error("Fichiers manquants.")
        st.stop()

    df_titres_complet = pd.read_csv(titre_path, sep=";")
    df_biais = pd.read_csv(biais_path)

    # SESSION
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
            st.experimental_rerun()
        else:
            st.stop()
    else:
        st.sidebar.markdown(f"👤 Annotateur : **{st.session_state.initiales}**")

    # COURANT
    biais_index = st.session_state.biais_index
    current_biais = df_biais.iloc[biais_index]
    nom_biais = current_biais["nom"]

    # PROGRESSION
    if os.path.exists(save_path):
        df_saved = pd.read_csv(save_path)
        biais_annotes = df_saved["biais"].nunique()
    else:
        biais_annotes = 0

    total_biais = len(df_biais)
    progression = biais_annotes / total_biais

    st.markdown(f"### 🔢 Avancement : {biais_annotes} / {total_biais} biais annotés")
    st.progress(progression)
    st.markdown(f"### Biais {biais_index + 1} / {total_biais}")

    # QUESTION & DÉFINITION
    with st.sidebar:
        st.markdown("## ❓ Question")
        st.markdown(f"**{current_biais['question_annotation']}**")
        with st.expander("ℹ️ Définition du biais"):
            st.markdown(f"**{nom_biais}** — {current_biais['definition_operationnelle']}")

    # TITRES À ANNOTER
    annotations = []
    for i, row in st.session_state.titres_random.iterrows():
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
            "annotation": choix,
            "annotateur": st.session_state.initiales
        })

    # VALIDATION
    def tous_titres_annotes():
        return all(a["annotation"] in ["Oui", "Doute", "Non"] for a in annotations)

    # NAVIGATION
    st.divider()
    col1, col2, col3 = st.columns([1, 4, 1])

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

                # Nettoyage
                for i in range(len(st.session_state.titres_random)):
                    key = f"{nom_biais}_{i}"
                    if key in st.session_state:
                        del st.session_state[key]

                # Passage au biais suivant
                if biais_index < len(df_biais) - 1:
                    st.session_state.biais_index += 1
                    st.session_state.reset_titres = True
                    st.session_state.trigger_rerun = True
                else:
                    st.success("🎉 Tous les biais ont été annotés.")
            else:
                st.warning("⚠️ Merci d’annoter tous les titres avant de continuer.")

    # TÉLÉCHARGEMENT
    if os.path.exists(save_path):
        st.sidebar.markdown("---")
        with open(save_path, "rb") as f:
            st.sidebar.download_button("📥 Télécharger annotations", f, file_name="annotations.csv")

# LANCEMENT
main()
