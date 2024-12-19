import streamlit as st

def afficher_accueil():
    # Lien brut vers l'image sur GitHub
    image_url = "https://raw.githubusercontent.com/Awoutokoffisamson/Application_Web/main/co2_prediction_app/logo6.jpg"

    # Appliquer le CSS avec l'image en fond et des styles modernes
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            color:#00007F; /* Couleur du texte par défaut */
        }}
        .main-title {{
            font-size: 3.9rem;
            font-weight: bold;
            text-align: center;
            color: #00007F; 
            background-color: #FFD700; /* Surlignage jaune */
            padding: 10px;
            border-radius: 10px;
        }}
        .intro-text {{
            font-size: 1.7rem;
            text-align: center;
            font-weight: bold;
            color: #FF0000;
            background-color: #FFFAE6; /* Surlignage clair */
            padding: 8px;
            border-radius: 10px;
            margin-bottom: 50px;
        }}
        .section-header {{
            font-size: 2.6rem;
            font-weight: bold;
            text-align: left;
            color: #00007F;
            text-shadow: 1px 1px 3px #00007F;
            background-color: #C0C0C0; /* Surlignage gris */
            padding: 10px;
            border-radius: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Contenu de la page d'accueil
    st.markdown('<h1 class="main-title">Bienvenue dans l\'application de prédiction de l\'émission du CO2</h1>', unsafe_allow_html=True)
    st.markdown('<p class="intro-text">Une application intuitive pour explorer et prédire l\'émission de CO2.</p>', unsafe_allow_html=True)

    st.markdown('<h2 class="section-header">🎯 Commencez dès maintenant !</h2>', unsafe_allow_html=True)
