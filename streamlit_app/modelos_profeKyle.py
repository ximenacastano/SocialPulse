import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor

# Cargar los datasets
def load_data():
    data = pd.read_csv('streamlit_app/data.csv')

    # Codificación para el campo categórico 'type'
    encoder = OneHotEncoder()
    tipo_cod = encoder.fit_transform(data[["type"]].fillna("Desconocido")).toarray()
    tipo_nombres = encoder.get_feature_names_out(["type"])
    tipo_cod_df = pd.DataFrame(tipo_cod, columns=tipo_nombres)
    data = pd.concat([data.reset_index(drop=True), tipo_cod_df.reset_index(drop=True)], axis=1)

    # Normalizar la columna 'Sentiment_Score'
    scaler = StandardScaler()
    data["Sentiment_Score"] = scaler.fit_transform(data[["Sentiment_Score"]])

    return data

data = load_data()

# Procesamiento de datos

variablesX = ["likesCount", "commentsCount", "videoPlayCount", "videoViewCount", "interaction_per_hashtag", "Interaccion_por_videoduracion", "Sentiment_Score"]
X = data[variablesX].fillna(0)
y = data["seguidoresCount_estimado"]

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenamiento y evaluación de modelos
def train_models(X_train, y_train, X_test, y_test, model_type, params):
    if model_type == "Árbol de Decisiones":
        model = DecisionTreeRegressor(max_depth=params['max_depth'], min_samples_leaf=params['min_samples_leaf'], 
                                      min_samples_split=params['min_samples_split'], random_state=42)
    elif model_type == "Random Forest":
        model = RandomForestRegressor(n_estimators=params['n_estimators'], max_depth=params['max_depth'], 
                                      min_samples_leaf=params['min_samples_leaf'], min_samples_split=params['min_samples_split'], random_state=42)
    elif model_type == "XGBoost":
        model = XGBRegressor(n_estimators=params['n_estimators'], max_depth=params['max_depth'], 
                             learning_rate=params['learning_rate'], random_state=42, eval_metric="mae")
    
    model.fit(X_train, y_train)
    predicciones = model.predict(X_test)
    
    return model, predicciones

# Función para evaluar modelos
def evaluate_models(y_test, predicciones):
    mae = mean_absolute_error(y_test, predicciones)
    r2 = r2_score(y_test, predicciones)
    return mae, r2


# Interacción con Streamlit
st.title("Predicción del Número Estimado de Seguidores")

# Parámetros para ajustar
model_params = {
    "Árbol de Decisiones": {"max_depth": 8, "min_samples_leaf": 5, "min_samples_split": 10},
    "Random Forest": {"n_estimators": 100, "max_depth": 10, "min_samples_leaf": 2, "min_samples_split": 2},
    "XGBoost": {"n_estimators": 100, "max_depth": 8, "learning_rate": 0.05},
}

# Entrenamiento de todos los modelos
models = {}
predicciones = {}

for model_type in ["Árbol de Decisiones", "Random Forest", "XGBoost"]:
    model, pred = train_models(X_train, y_train, X_test, y_test, model_type, model_params[model_type])
    models[model_type] = model
    predicciones[model_type] = pred

# Botón para hacer predicciones con los tres modelos
st.write("""
    Utiliza esta herramienta para estimar la cantidad de seguidores que podrías alcanzar, basándote en diferentes características de tus publicaciones. Compara los resultados obtenidos con tres modelos: Árbol de Decisiones, Random Forest y XGBoost.
""")

# Entrada de datos del usuario
def load_modelos():
    likesCount = st.number_input("Likes Totales", min_value=0, value=1000)
    commentsCount = st.number_input("Comentarios Totales", min_value=0, value=100)
    videoPlayCount = st.number_input("Reproducciones del Video", min_value=0, value=10000)
    videoViewCount = st.number_input("Vistas del video", min_value=0, value=20000)
    interaction_per_hashtag = st.number_input("Interacción por Hashtag", min_value=0.0, value=0.2)
    Interaccion_por_videoduracion = st.number_input("Interacción por Duración del Video", min_value=0.0, value=0.3)
    Sentiment_Score = st.number_input("Puntaje de Sentimiento", min_value=-1.0, max_value=1.0, value=0.0)

    input_data = np.array([likesCount, commentsCount, videoPlayCount, videoViewCount, interaction_per_hashtag, Interaccion_por_videoduracion, Sentiment_Score]).reshape(1, -1)

    if st.button("Calcular las predicciones."):
        st.write("### Resultados de Predicción de Seguidores")
        st.write("""
        Basándonos en los datos ingresados, estos son los números estimados de seguidores para cada modelo
    """)
        
        for model_type in ["Árbol de Decisiones", "Random Forest", "XGBoost"]:
            pred = models[model_type].predict(input_data)
            st.write(f"{model_type}: {pred[0]:,.0f} seguidores")
        
    #     st.write("### Gráfico de Comparación de Predicciones")
    #     fig, ax = plt.subplots()
    #     ax.bar(["Árbol de Decisiones", "Random Forest", "XGBoost"], 
    #            [models["Árbol de Decisiones"].predict(input_data)[0],
    #             models["Random Forest"].predict(input_data)[0],
    #             models["XGBoost"].predict(input_data)[0]], 
    #            color=['red', 'blue', 'green'])
    #     ax.set_ylabel('Predicción de Seguidores')
    #     st.pyplot(fig)

    # Evaluación de los modelos
    # st.write("### Evaluación de los Modelos (Error Promedio y R²)")

    # for model_type in ["Árbol de Decisiones", "Random Forest", "XGBoost"]:
    #     mae, r2 = evaluate_models(y_test, predicciones[model_type])
    #     st.write(f"{model_type} - MAE: {mae:.4f}, R²: {r2:.4f}")
