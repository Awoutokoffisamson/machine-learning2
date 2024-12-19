import streamlit as st
from accueil import afficher_accueil
from visualisation import afficher_visualisation
from prediction import afficher_prediction
import pandas as pd
import joblib
from streamlit_option_menu import option_menu

# Charger le modèle et les données
model = joblib.load('trained_model.pkl')  # Assurez-vous que le modèle est dans le même répertoire
data = pd.read_csv('https://raw.githubusercontent.com/Awoutokoffisamson/Application_Web/refs/heads/main/co2_prediction_app/Final_data.csv') # Assurez-vous que le fichier CSV est dans le même répertoire
model_columns = joblib.load('model_columns.pkl')  # Charger les colonnes du modèle

# Configuration de la barre latérale avec des icônes
with st.sidebar:
    st.image("https://cdn.pixabay.com/animation/2023/08/23/15/46/15-46-31-162_512.gif", use_column_width=True)
    st.title("Navigation")
    page = option_menu(
        menu_title="Menu principal",
        options=["Accueil", "Visualisation", "Prédiction"],
        icons=["house", "bar-chart-line", "robot"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#f8f9fa"},
            "icon": {"color": "blue", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#007BFF", "color": "white"},
        },
    )

# Affichage de la page choisie
if page == "Accueil":
    afficher_accueil()
elif page == "Visualisation":
    afficher_visualisation(data)
elif page == "Prédiction":
    afficher_prediction()

# Ajouter du style CSS pour améliorer l'esthétique globale
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f7fa;
    }
    .block-container {
        padding: 2rem;
        border-radius: 10px;
        background: white;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1, h2, h3, h4, h5, h6 {
        color: #007BFF;
    }
    </style>
""", unsafe_allow_html=True)
