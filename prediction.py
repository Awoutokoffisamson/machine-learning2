import gdown
import joblib
import pandas as pd
import numpy as np
import streamlit as st

# Liens des fichiers sur Google Drive
model_columns_url = "https://drive.google.com/uc?id=1hA2nmYYDhswZ9Xt-Keazp9kVOpGBdTmI"
trained_model_url = "https://drive.google.com/uc?id=1HobHUNSjvfiOZ9QrqnCO8v4cNqqOo1rU"

# Télécharger et charger model_columns.pkl
print("Téléchargement de model_columns.pkl...")
gdown.download(model_columns_url, "model_columns.pkl", quiet=False)
model_columns = joblib.load("model_columns.pkl")
print("model_columns.pkl chargé avec succès.")

# Télécharger et charger trained_model.pkl
print("Téléchargement de trained_model.pkl...")
gdown.download(trained_model_url, "trained_model.pkl", quiet=False)
model = joblib.load("trained_model.pkl")
print("trained_model.pkl chargé avec succès.")

# Charger les données pour les sélecteurs
final_data_url = "https://raw.githubusercontent.com/Awoutokoffisamson/Application_Web/main/co2_prediction_app/Final_data.csv"
data = pd.read_csv(final_data_url)

# Fonction pour appliquer les styles CSS
def apply_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f4f4f4;
            font-family: Arial, sans-serif;
        }
        .main-title {
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            color: #FFD700;
            background-color: #000000;
            padding: 10px;
            border-radius: 10px;
        }
        .section-title {
            font-size: 1.5rem;
            font-weight: bold;
            color: #FFD700;
            text-align: center;
            margin-bottom: 20px;
        }
        label {
            font-weight: bold;
            color: #000000;
        }
        input, select {
            color: #FFD700 !important;
            background-color: #333333 !important;
            border: 1px solid #FFD700 !important;
            border-radius: 5px !important;
        }
        .prediction-result {
            background-color: #FFD700;
            color: #000000;
            font-size: 1.2rem;
            text-align: center;
            padding: 10px;
            border-radius: 10px;
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Fonction principale
def afficher_prediction():
    apply_styles()

    # Titre principal
    st.markdown('<h1 class="main-title">🔮 Prédiction de la consommation de CO2</h1>', unsafe_allow_html=True)

    # Onglets
    tab1, tab2 = st.tabs(["🏢 Prédiction unique", "📂 Prédictions multiples"])

    # Prédiction unique
    with tab1:
        st.markdown('<h2 class="section-title">🏢 Informations pour une prédiction unique</h2>', unsafe_allow_html=True)

        with st.form("prediction_unique"):
            # Champs d'entrée
            number_of_floors = st.number_input("Nombre d'étages", min_value=1, max_value=100, value=10)
            number_of_buildings = st.number_input("Nombre de bâtiments", min_value=1, max_value=100, value=5)
            property_gfa_building = st.number_input("Surface totale du bâtiment (GFA)", min_value=1, max_value=100000, value=5000)
            property_gfa_parking = st.number_input("Surface du parking (GFA)", min_value=1, max_value=100000, value=1000)
            energystar_score = st.number_input("Score ENERGY STAR", min_value=0, max_value=100, value=50)
            site_eui = st.number_input("Site EUI (kBtu/sf)", min_value=0, max_value=1000, value=200)
            electricity_kbtu = st.number_input("Consommation d'électricité (kBtu)", min_value=0, max_value=1000000, value=100000)
            natural_gas_kbtu = st.number_input("Consommation de gaz naturel (kBtu)", min_value=0, max_value=1000000, value=50000)
            largest_property_use_type_gfa = st.number_input("Plus grande utilisation du bâtiment (GFA)", min_value=1, max_value=100000, value=10000)
            building_age = st.number_input("Âge du bâtiment", min_value=0, max_value=100, value=30)
            ghg_emissions_intensity = st.number_input("Intensité des émissions GES", min_value=0.0, max_value=1000.0, value=200.0)
            building_type = st.selectbox("Type de bâtiment", data['BuildingType'].unique())
            neighborhood = st.selectbox("Quartier", data['Neighborhood'].unique())

            submitted = st.form_submit_button("Prédire")

        if submitted:
            # Préparation des données
            input_data = {
                'NumberofFloors': number_of_floors,
                'NumberofBuildings': number_of_buildings,
                'PropertyGFABuilding(s)': property_gfa_building,
                'PropertyGFAParking': property_gfa_parking,
                'ENERGYSTARScore': energystar_score,
                'SiteEUIWN(kBtu/sf)': site_eui,
                'Electricity(kBtu)': electricity_kbtu,
                'NaturalGas(kBtu)': natural_gas_kbtu,
                'LargestPropertyUseTypeGFA': largest_property_use_type_gfa,
                'BuildingAge': building_age,
                'GHGEmissionsIntensity': ghg_emissions_intensity,
                'Neighborhood': neighborhood,
                'BuildingType': building_type,
            }
            input_df = pd.DataFrame(input_data, index=[0])
            input_df = pd.get_dummies(input_df, drop_first=True)

            # Ajout des colonnes manquantes
            missing_cols = set(model_columns) - set(input_df.columns)
            for col in missing_cols:
                input_df[col] = 0
            input_df = input_df[model_columns]

            # Prédiction
            predicted_log_y = model.predict(input_df)
            predicted_co2 = np.exp(predicted_log_y)

            # Résultat
            st.markdown(
                f'<div class="prediction-result">🌍 Émission de CO2 prédite : <strong>{predicted_co2[0]:.2f} kg CO2</strong></div>',
                unsafe_allow_html=True,
            )

    # Prédictions multiples
    with tab2:
        st.markdown('<h2 class="section-title">📂 Prédictions multiples pour plusieurs bâtiments</h2>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Téléchargez un fichier Excel", type=["xlsx", "xls"])
        if uploaded_file:
            data_excel = pd.read_excel(uploaded_file, engine='openpyxl')
            st.write("📋 **Aperçu des données :**", data_excel.head())
            if st.button("Lancer les prédictions multiples"):
                data_cleaned = pd.get_dummies(data_excel, drop_first=True)
                missing_cols = set(model_columns) - set(data_cleaned.columns)
                for col in missing_cols:
                    data_cleaned[col] = 0
                data_cleaned = data_cleaned[model_columns]
                predictions = model.predict(data_cleaned)
                data_excel['Predicted_CO2'] = np.exp(predictions)
                st.write("📊 **Résultats avec prédictions :**", data_excel)

if __name__ == "__main__":
    afficher_prediction()
