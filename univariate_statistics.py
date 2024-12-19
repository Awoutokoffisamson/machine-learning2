import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def afficher_statistiques_univariees(data):
    # Titre principal avec design amélioré
    st.markdown(
        """
        <style>
            h1.title {
                color: #1E1E1E;
                background-color: #F7DC6F;
                padding: 12px;
                text-align: center;
                border-radius: 8px;
                font-family: Arial, sans-serif;
                font-weight: bold;
                margin-bottom: 20px;
                font-size: 20px;
            }
            h3.subtitle {
                color: #1E1E1E;
                background-color: #FDEBD0;
                padding: 8px;
                border-radius: 5px;
                font-family: Arial, sans-serif;
                margin-top: 10px;
                margin-bottom: 5px;
                font-size: 16px;
            }
            .stTable {
                background-color: white !important;
                border-radius: 8px;
                padding: 8px;
                box-shadow: 0px 0px 8px rgba(0, 0, 0, 0.3);
            }
        </style>
        <h1 class="title">Statistiques Univariées</h1>
        """,
        unsafe_allow_html=True
    )

    # Sélection de la variable à visualiser
    quantitative_columns = data.select_dtypes(include=['float64', 'int']).columns.tolist()
    
    # Titre de la sélection de variable avec style amélioré
    st.markdown("<h3 class='subtitle'>Choisissez une variable quantitative à visualiser</h3>", unsafe_allow_html=True)
    variable = st.selectbox('', quantitative_columns)

    # Créer les statistiques descriptives
    stats = data[variable].describe()

    # Renommer les paramètres statistiques
    stats_renamed = stats.rename(index={
        'count': 'Effectif',
        'mean': 'Moyenne',
        'std': 'Écart-type',
        'min': 'Minimum',
        '25%': '1er Quartile',
        '50%': 'Médiane',
        '75%': '3ème Quartile',
        'max': 'Maximum'
    })
    stats_renamed['Effectif'] = stats_renamed['Effectif'].astype(int)

    # Affichage avec alignement propre
    col1, col2 = st.columns([1, 1])  # Assure la même largeur
    with col1:
        st.markdown(f"<h3 class='subtitle'>Histogramme de la variable {variable}</h3>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(5, 5))
        data[variable].hist(bins=20, ax=ax, color='#5DADE2', edgecolor='black')
        ax.set_title(f"Distribution de {variable}", fontsize=10, color='#1E1E1E')
        ax.set_xlabel(variable, fontsize=8)
        ax.set_ylabel('Fréquence', fontsize=8)
        st.pyplot(fig)

    with col2:
        st.markdown(f"<h3 class='subtitle'>Statistiques descriptives</h3>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class='stTable'>
                {stats_renamed.to_frame().to_html(classes='dataframe', border=0)}
            </div>
            """,
            unsafe_allow_html=True
        )
