import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from carte import afficher_carte
from univariate_statistics import afficher_statistiques_univariees
from bivariate_statistics import afficher_statistiques_bivariees
import base64

def set_background(image_url):
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("{image_url}");
        background-size: cover;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

def afficher_visualisation(data):
    # Utilisation de l'image depuis GitHub comme fond
    set_background("https://raw.githubusercontent.com/Awoutokoffisamson/Application_Web/main/co2_prediction_app/logo4.jpg")

    # Titres principaux et sous-titres avec surlignage doux
    st.markdown('<h1 style="color: black; background-color: #FFD700; padding: 10px;">Visualisation des données</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="color: black; background-color: #FFEFD5; padding: 5px;">DataFrame de Final_base</h3>', unsafe_allow_html=True)

    st.dataframe(data)

    # Gestion des boutons pour afficher différentes sections
    if 'show_univariate' not in st.session_state:
        st.session_state.show_univariate = False
    if 'show_bivariate' not in st.session_state:
        st.session_state.show_bivariate = False
    if 'show_map' not in st.session_state:
        st.session_state.show_map = False

    # Création des boutons en ligne
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Afficher les statistiques univariées"):
            st.session_state.show_univariate = not st.session_state.show_univariate
            st.session_state.show_bivariate = False
            st.session_state.show_map = False
    with col2:
        if st.button("Afficher les statistiques bivariées"):
            st.session_state.show_bivariate = not st.session_state.show_bivariate
            st.session_state.show_univariate = False
            st.session_state.show_map = False
    with col3:
        if st.button("Afficher la carte"):
            st.session_state.show_map = not st.session_state.show_map
            st.session_state.show_univariate = False
            st.session_state.show_bivariate = False

    # Affichage des sections correspondantes
    if st.session_state.show_univariate:
        st.markdown('<h3 style="color: black; background-color: #FFEFD5; padding: 5px;">Statistiques univariées</h3>', unsafe_allow_html=True)
        afficher_statistiques_univariees(data)

    if st.session_state.show_bivariate:
        st.markdown('<h3 style="color: black; background-color: #FFEFD5; padding: 5px;">Statistiques bivariées</h3>', unsafe_allow_html=True)
        afficher_statistiques_bivariees(data)

    if st.session_state.show_map:
        st.markdown('<h3 style="color: black; background-color: #FFEFD5; padding: 5px;">Carte des données</h3>', unsafe_allow_html=True)
        afficher_carte("Final_data2.xlsx")

# Charger les données depuis GitHub
data = pd.read_csv('https://raw.githubusercontent.com/Awoutokoffisamson/Application_Web/main/co2_prediction_app/Final_data.csv')

if __name__ == "__main__":
    afficher_visualisation(data)
