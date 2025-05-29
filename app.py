import streamlit as st
import pandas as pd
import os

# 1. CONFIG
st.set_page_config(page_title="Annotation biais", layout="wide")

# 2. MAIN FUNCTION
def main():
    # ─── CHARGEMENT DES FICHIERS ──────────────────────────────────────
    titre_path = "titres_manipulatifs10.csv"
    biais_path = "biais_complet_avec_questions.csv"

    if not os.path.exists(titre_path) or not os.path.exists(biais_path):
        st.error("Fichiers manquants.")
        return

    df_titres = pd.read_csv(titre_path, sep=";")
    df_biais = pd.read_csv(biais_path)

    # ─── SESSION ─────────────────────────────────────────────────────
    if "biais_index" not in st.session_state:
        st.session_state.biais_index = 0

    current_biais = df_biais.iloc[st.session_state.biais_index]
    nom_biais = current_biais["nom"]

    # ─── SIDEBAR FIXE ────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("## ❓ Question d’annotation")
        st.markdown(f"{current_biais['question_annotation']}")
        with st.expander(f"ℹ️ Définition du biais : {nom_biais}"):
            st.markdown(current_biais["definition_operationnelle"])

    # ─── ZONE CENTRALE ───────────────────────────────────────────────
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

    def tous_titres_annotés():
        return all(a["annotation"] in ["Oui", "Doute", "Non"] for a in annotations)

    # ─── NAVIGATION & SAUVEGARDE ──────────────────────────────────────
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 2])

    go_next = False
    go_prev = False

    with col1:
        if st.button("⬅️ Biais précédent", disabled=st.session_state.biais_index == 0):
            if tous_titres_annotés():
                pd.DataFrame(annotations).to_csv(
                    f"annotations_{nom_biais.replace(' ', '_')}.csv", index=False
                )
                go_prev = True
            else:
                st.warning("⚠️ Merci d’annoter chaque titre avant de continuer.")

    with col2:
        if st.button("➡️ Biais suivant", disabled=st.session_state.biais_index == len(df_biais) - 1):
            if tous_titres_annotés():
                pd.DataFrame(annotations).to_csv(
                    f"annotations_{nom_biais.replace(' ', '_')}.csv", index=False
                )
                go_next = True
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

    # ─── CHANGEMENT DE BIAIS (en dehors du flux principal) ────────────
    if go_prev:
        for i in range(10):
            key = f"{nom_biais}_{i}"
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.biais_index -= 1
        st.experimental_rerun()
        return

    if go_next:
        for i in range(10):
            key = f"{nom_biais}_{i}"
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.biais_index += 1
        st.experimental_rerun()
        return

# ─── EXÉCUTION ───────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
