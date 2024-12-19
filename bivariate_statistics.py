import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

def afficher_statistiques_bivariees(data):
    # Style amélioré pour les titres, sous-titres et résultats
    st.markdown(
        """
        <style>
            h3.subtitle {
                color: black;
                background-color: #FFEFD5;
                padding: 6px;
                border-radius: 5px;
                font-family: Arial, sans-serif;
                font-size: 14px;
                margin-top: 8px;
                margin-bottom: 5px;
            }
            .highlight-result {
                background-color: #FDEBD0;
                padding: 4px 8px;
                border-radius: 5px;
                display: inline-block;
                font-weight: bold;
                font-size: 14px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Sélection des variables
    quantitative_columns = data.select_dtypes(include=['float64', 'int']).columns.tolist()
    qualitative_columns = data.select_dtypes(include=['object']).columns.tolist()

    # Sélection de la première variable
    st.markdown("<h3 class='subtitle'>Choisissez la première variable</h3>", unsafe_allow_html=True)
    var1 = st.selectbox('', quantitative_columns + qualitative_columns, key='selectbox1')

    # Sélection de la deuxième variable
    st.markdown("<h3 class='subtitle'>Choisissez la deuxième variable</h3>", unsafe_allow_html=True)
    var2 = st.selectbox('', quantitative_columns + qualitative_columns, key='selectbox2')

    # Vérification des types de variables
    if var1 in quantitative_columns and var2 in quantitative_columns:
        # Nuage de points
        st.markdown(f"<h3 class='subtitle'>Nuage de points entre {var1} et {var2}</h3>", unsafe_allow_html=True)
        fig, ax = plt.subplots()
        ax.scatter(data[var1], data[var2], color='#5DADE2', edgecolors='black')
        ax.set_xlabel(var1)
        ax.set_ylabel(var2)
        st.pyplot(fig)

        # Calcul et affichage de la corrélation avec surlignage
        correlation = data[[var1, var2]].corr().iloc[0, 1]
        st.markdown(
            f"<span class='highlight-result'>Coefficient de corrélation : {correlation:.2f}</span>",
            unsafe_allow_html=True
        )

    elif (var1 in qualitative_columns and var2 in quantitative_columns) or (var1 in quantitative_columns and var2 in qualitative_columns):
        # Diagramme en barres empilées
        st.markdown(f"<h3 class='subtitle'>Diagramme en barres entre {var1} et {var2}</h3>", unsafe_allow_html=True)
        fig, ax = plt.subplots()
        if var1 in qualitative_columns:
            sns.countplot(data=data, x=var1, hue=var2, palette="muted")
        else:
            sns.countplot(data=data, x=var2, hue=var1, palette="muted")
        st.pyplot(fig)

        # Tableau croisé
        st.markdown("<h3 class='subtitle'>Tableau croisé</h3>", unsafe_allow_html=True)
        cross_tab = pd.crosstab(data[var1], data[var2])
        st.table(cross_tab)

    elif var1 in qualitative_columns and var2 in qualitative_columns:
        # Tableau croisé et test du chi-deux
        st.markdown(f"<h3 class='subtitle'>Tableau croisé entre {var1} et {var2}</h3>", unsafe_allow_html=True)
        cross_tab = pd.crosstab(data[var1], data[var2])
        st.table(cross_tab)

        chi2, p, dof, expected = chi2_contingency(cross_tab)
        st.markdown(
            f"<span class='highlight-result'>Valeur du test de Chi-deux : {chi2:.2f}, p-value : {p:.4f}</span>",
            unsafe_allow_html=True
        )
