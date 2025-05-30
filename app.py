from pathlib import Path
import pandas as pd
import streamlit as st
import os

st.set_page_config(page_title="Annotation biais", layout="wide")

titre_path = "Table4.csv"  # Nouveau fichier avec colonnes Bloc, Index, Titre, Type
biais_path = "biais_complet_avec_questions.csv"
save_path = "annotations_global.csv"

# Rerun trigger
if "trigger_rerun" not in st.session_state:
    st.session_state.trigger_rerun = False
elif st.session_state.trigger_rerun:
    st.session_state.trigger_rerun = False
    st.rerun()

def main():
    if not os.path.exists(titre_path) or not os.path.exists(biais_path):
        st.error("Fichiers manquants.")
        st.stop()

    df_titres = pd.read_csv(titre_path, sep=";")
    df_biais = pd.read_csv(biais_path)

    blocs = sorted(df_titres["Bloc"].dropna().unique())

    # Réinitialisation
    if st.sidebar.button("🧹 Réinitialiser tout"):
        if os.path.exists(save_path):
            os.remove(save_path)
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.sidebar.success("Réinitialisation effectuée. Rechargement…")
        st.rerun()

    # Bloc courant
    if "bloc_index" not in st.session_state:
        st.session_state.bloc_index = 0
    current_bloc = blocs[st.session_state.bloc_index]

    # Initiales
    if "initiales" not in st.session_state or not st.session_state.initiales:
        initiales = st.text_input("🖊️ Vos initiales :", key="initiales_input")
        if initiales:
            st.session_state.initiales = initiales
            st.session_state.trigger_rerun = True
            st.rerun()
        else:
            st.title("🧠 Annotation des biais cognitifs")
            st.warning("Merci de saisir vos initiales pour commencer.")
            st.stop()
    else:
        st.sidebar.markdown(f"👤 Annotateur : **{st.session_state.initiales}**")

    # Choix du biais
    if "biais_index" not in st.session_state:
        st.session_state.biais_index = 0
    biais_index = st.session_state.biais_index
    current_biais = df_biais.iloc[biais_index]
    nom_biais = current_biais["nom"]

    # Progrès
    if os.path.exists(save_path):
        df_saved = pd.read_csv(save_path)
        biais_annotes = df_saved[df_saved["bloc"] == current_bloc]["biais"].nunique()
    else:
        biais_annotes = 0

    total_biais = len(df_biais)
    st.markdown(f"### Bloc {current_bloc} – 🔢 Avancement : {biais_annotes} / {total_biais} biais annotés")
    st.progress(biais_annotes / total_biais)
    st.markdown(f"### Biais {biais_index + 1} / {total_biais} – *{nom_biais}*")

    # Sidebar : contexte du biais
    with st.sidebar:
        st.markdown("## ❓ Question")
        st.markdown(f"**{current_biais['question_annotation']}**")
        with st.expander("ℹ️ Définition du biais"):
            st.markdown(f"**{nom_biais}** — {current_biais['definition_operationnelle']}")

    # Échantillon du bloc courant
    df_bloc = df_titres[df_titres["Bloc"] == current_bloc].sample(n=10, random_state=biais_index).reset_index(drop=True)

    annotations = []
    for i, row in df_bloc.iterrows():
        titre = row["Titre"]
        index_titre = row["Index"]
        key = f"{nom_biais}_{current_bloc}_{i}"

        st.markdown(
            f"""<div style='margin-bottom: 0.2rem; margin-top: 1.2rem; font-weight: 600;'>
            {i+1}. {titre}
            </div>""",
            unsafe_allow_html=True
        )

        likert_labels = {
            "1": "1 – Pas du tout",
            "2": "2 – Faiblement",
            "3": "3 – Moyennement",
            "4": "4 – Très présent"
        }

        choix = st.radio(
            label="",
            options=[""] + list(likert_labels.keys()),
            format_func=lambda x: likert_labels.get(x, "Sélectionner"),
            key=key,
            horizontal=True
        )

        st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)

        annotations.append({
            "index": index_titre,
            "bloc": current_bloc,
            "titre": titre,
            "biais": nom_biais,
            "annotation": choix,
            "annotateur": st.session_state.initiales
        })

    def tous_titres_annotes():
        return all(a["annotation"] in ["1", "2", "3", "4"] for a in annotations)

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

                for i in range(10):
                    key = f"{nom_biais}_{current_bloc}_{i}"
                    if key in st.session_state:
                        del st.session_state[key]

                if biais_index < total_biais - 1:
                    st.session_state.biais_index += 1
                    st.rerun()
                else:
                    if st.session_state.bloc_index < len(blocs) - 1:
                        st.session_state.biais_index = 0
                        st.session_state.bloc_index += 1
                        st.success("✅ Bloc terminé. Passage au bloc suivant.")
                        st.rerun()
                    else:
                        st.success("🎉 Tous les blocs et biais ont été annotés.")
            else:
                st.warning("⚠️ Merci d’annoter tous les titres avant de continuer.")

    # Téléchargement
    if os.path.exists(save_path):
        st.sidebar.markdown("---")
        with open(save_path, "rb") as f:
            st.sidebar.download_button("📥 Télécharger annotations", f, file_name="annotations.csv")

main()
