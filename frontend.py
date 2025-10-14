# app.py
import streamlit as st
import requests
from PIL import Image
import io

st.title("🧠 SRGAN — Super Resolution GAN")
st.write("Améliorez la résolution de vos images grâce à SRGAN (backend séparé).")

API_URL = "http://localhost:8000/superres"  # <-- adapte selon ton déploiement

uploaded_file = st.file_uploader("Téléchargez une image basse résolution", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Image basse résolution", use_container_width=True)

    with st.spinner("Amélioration de la résolution en cours..."):
        response = requests.post(API_URL, files={"file": uploaded_file.getvalue()})
        if response.status_code == 200:
            result_image = Image.open(io.BytesIO(response.content))
            st.image(result_image, caption="Résultat SRGAN", use_container_width=True)
        else:
            st.error("Erreur : impossible d'obtenir une réponse du serveur SRGAN.")
