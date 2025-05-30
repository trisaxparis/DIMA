import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Annotation biais", layout="wide")

titre_path = "Table4.csv"
biais_path = "biais_complet_avec_questions.csv"
save_path = "annotations_global.csv"

# ▶️ Rerun initial
if "trigger_rerun" not in st.session_state:
    st.session_state.trigger_rerun = False
elif st.session_state.trigger_rerun:
    st.session_state.trigger_rerun = False
    st.rerun()

def main():
    # ⛔ Vérifier fichiers
    if not os.path.exists(titre_path) or not os.path.exists(biais_path):
        st.error("Fichier manquant.")
        st.stop()

    df_titres = pd.read_csv(titre_path, sep=";")
    df_biais = pd.read_csv(biais_path)

    # ✅ Vérification de la source réelle et des colonnes
    st.sidebar.info(f"Fichier source : `{titre_path}`")
    st.sidebar.write("Extrait du fichier :")
    st.sidebar.dataframe(df_titres.head(3))

    if "Bloc" not in df_titres.columns or "Titre" not in df_titres.columns or "Index" not in df_titres.columns:
        st.error("❌ Le fichier de titres doit contenir les colonnes : Bloc, Titre, Index")
        st.stop()

    blocs = sorted(df_titres["Bloc"].dropna().unique())

    if st.sidebar.button("🧹 Réinitialiser tout"):
        if os.path.exists(save_path):
            os.remove(save_path)
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.sidebar.success("Réinitialisation effectuée.")
        st.rerun()

    # Initiales
    if "initiales" not in st.session_state or not st.session_state.initiales:
        initials = st.text_input("🖊️ Vos initiales :", key="initiales_input")
        if initials:
            st.session_state.initiales = initials
            st.rerun()
        else:
            st.title("🧠 Annotation des biais cognitifs")
            st.warning("Merci de saisir vos initiales pour commencer.")
            st.stop()
    else:
        st.sidebar.markdown(f"👤 Annotateur : **{st.session_state.initiales}**")

    # Bloc courant
    if "bloc_index" not in st.session_state:
        st.session_state.bloc_index = 0
    current_bloc = blocs[st.session_state.bloc_index]

    df_bloc = df_titres[df_titres["Bloc"] == current_bloc].sample(n=10, random_state=42).reset_index(drop=True)

    # Biais courant
    if "biais_index" not in st.session_state:
        st.session_state.biais_index = 0
    biais_index = st.session_state.biais_index
    current_biais = df_biais.iloc[biais_index]
    nom_biais = current_biais["nom"]

    st.markdown(f"### Bloc {current_bloc} — Biais {biais_index+1} / {len(df_biais)} : *{nom_biais}*")

    with st.sidebar:
        st.markdown("## ❓ Question")
        st.markdown(f"**{current_biais['question_annotation']}**")
        with st.expander("ℹ️ Définition du biais"):
            st.markdown(current_biais["definition_operationnelle"])

    annotations = []
    for i, row in df_bloc.iterrows():
        titre = row["Titre"]
        index_titre = row["Index"]
        key = f"{nom_biais}_{current_bloc}_{i}"

        st.markdown(f"**{i+1}. {titre}**")
        choix = st.radio(
            label="",
            options=["", "1", "2", "3", "4"],
            format_func=lambda x: {
                "1": "1 – Pas du tout",
                "2": "2 – Faiblement",
                "3": "3 – Moyennement",
                "4": "4 – Très présent"
            }.get(x, "Sélectionner"),
            key=key,
            horizontal=True
        )

        annotations.append({
            "index": index_titre,
            "bloc": current_bloc,
            "titre": titre,
            "biais": nom_biais,
            "annotation": choix,
            "annotateur": st.session_state.initiales
        })

    def tous_annotes():
        return all(a["annotation"] in ["1", "2", "3", "4"] for a in annotations)

    st.divider()
    if st.button("➡️ Biais suivant"):
        if tous_annotes():
            df_save = pd.DataFrame(annotations)
            if os.path.exists(save_path):
                df_old = pd.read_csv(save_path)
                df_concat = pd.concat([df_old, df_save], ignore_index=True)
            else:
                df_concat = df_save
            df_concat.to_csv(save_path, index=False)

            for i in range(10):
                key = f"{nom_biais}_{current_bloc}_{i}"
                if key in st.session_state:
                    del st.session_state[key]

            if biais_index < len(df_biais) - 1:
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
            st.warning("⚠️ Veuillez annoter tous les titres.")

    if os.path.exists(save_path):
        with open(save_path, "rb") as f:
            st.sidebar.download_button("📥 Télécharger les annotations", f, file_name="annotations.csv")

main()
