import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud

# Verificar que los archivos existen
try:
    data = pd.read_csv('streamlit_app/posts_atravelerteacher.csv')
    df_emotions = pd.read_csv("streamlit_app/df_emotions_caption_atravelerteacher.csv", usecols=["id", "timestamp", "Sentiment_Score"])
except FileNotFoundError:
    st.error("No se encontraron los archivos CSV. Asegúrate de que las rutas sean correctas.")
    st.stop()

# Comprobar si los archivos fueron cargados correctamente
if data.empty or df_emotions.empty:
    st.error("Los archivos CSV están vacíos o no se cargaron correctamente.")
    st.stop()

# Combinar los datos
data = data.merge(df_emotions[["id", "Sentiment_Score"]], on="id", how="left")

# Preprocesamiento
data["total_seguidores"] = 35500
data["total_interac"] = (data["likesCount"] + data["commentsCount"])
data["tasa_interac"] = (data["total_interac"] / data["total_seguidores"]) * 100
avg_engagement_rate = data["tasa_interac"].mean()
data["seguidoresCount_estimado"] = (data["likesCount"] + data["commentsCount"]) / avg_engagement_rate

scaler = StandardScaler()
data["Sentiment_Score"] = scaler.fit_transform(data[["Sentiment_Score"]])

def analisis_atraveler_teacher():
    st.title("Análisis de Rendimiento de la Cuenta Atraveler Teacher")
    
    # Mostrar una vista general de los datos
    st.subheader("Vista General de los Datos:")
    st.dataframe(data.head())
    
    # Mostrar estadísticas descriptivas
    st.subheader("Estadísticas Descriptivas")
    st.write(data.describe())

    # Gráfico interactivo de la tasa de interacción con Plotly
    st.subheader("Distribución de la Tasa de Interacción")
    fig_histogram = px.histogram(data, x="tasa_interac", nbins=30, title="Distribución de la Tasa de Interacción", 
                                labels={"tasa_interac": "Tasa de Interacción"}, color_discrete_sequence=["#0091b2"])
    st.plotly_chart(fig_histogram, key="histogram_tasa_interac")

    # Gráfico de dispersión interactivo: Tasa de interacción vs Sentiment Score
    st.subheader("Relación entre la Tasa de Interacción y el Sentiment Score")
    fig_scatter = px.scatter(data, x="tasa_interac", y="Sentiment_Score", color="Sentiment_Score", 
                            title="Relación entre Tasa de Interacción y Sentiment Score", 
                            labels={"tasa_interac": "Tasa de Interacción", "Sentiment_Score": "Sentiment Score"}, color_continuous_scale="Blues")
    st.plotly_chart(fig_scatter, key="scatter_tasa_sentiment")

    # Boxplot de Sentiment Score con Plotly
    st.subheader("Distribución de Sentiment Score")
    fig_boxplot = px.box(data, y="Sentiment_Score", title="Distribución de Sentiment Score", color_discrete_sequence=["#00667d"])
    st.plotly_chart(fig_boxplot, key="boxplot_sentiment_score")

    # Gráfico de barras de interacciones totales por tipo de publicación
    st.subheader("Interacciones Totales por Tipo de Publicación")
    fig_bar = px.bar(data, x="type", y="total_interac", color="type", title="Interacciones Totales por Tipo de Publicación", 
                    labels={"type": "Tipo de Publicación", "total_interac": "Total de Interacciones"},color_discrete_sequence=["#bff3ff", "#80e8ff", "#80e8ff"] )
    st.plotly_chart(fig_bar, key="bar_interacciones_tipo")

    # Heatmap de correlación
    st.subheader("Matriz de Correlación entre Variables")
    correlation_matrix = data[["likesCount", "commentsCount", "videoPlayCount", "videoViewCount", "Sentiment_Score", "tasa_interac"]].corr()
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale="Blues",
        colorbar=dict(title="Correlación")
    ))
    fig_heatmap.update_layout(title="Matriz de Correlación", xaxis_title="Variables", yaxis_title="Variables")
    st.plotly_chart(fig_heatmap, key="heatmap_correlacion")

    # Sentiment Distribution
    sentiment_counts = df_emotions["Sentiment_Score"].value_counts()
    fig_sentiment = px.bar(sentiment_counts, x=sentiment_counts.index, y=sentiment_counts.values, title="Distribución de Sentimientos", color_discrete_sequence=["#0091b2"])
    st.plotly_chart(fig_sentiment, key="bar_sentiment_distribution")

    # Scatter Plot de Likes vs Tasa de Interacción
    fig_scatter_likes = px.scatter(data, x="likesCount", y="tasa_interac", title="Likes vs Tasa de Interacción", color_discrete_sequence=["#007BFF"])
    st.plotly_chart(fig_scatter_likes, key="scatter_likes_tasa_interac")

    # Nube de palabras
    st.subheader("Nube de Palabras de Títulos y Primer Comentario de las Publicaciones")
    text = " ".join(data["caption"].dropna()) + " " + " ".join(data["firstComment"].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="Blues").generate(text)

    # Mostrar la nube de palabras
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)

