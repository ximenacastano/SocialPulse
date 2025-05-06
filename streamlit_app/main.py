import streamlit as st

# Importa las funciones de cada página
def load_home():
    from Home import home
    home()

def load_analisis():
    from analisis_profeKyle import analisis
    analisis()

def load_analisis_atraveler():
    from analisis_atraveler import analisis_atraveler_teacher
    analisis_atraveler_teacher()

def load_modelos():
    from modelos_profeKyle import load_modelos
    load_modelos()

def load_modelos_atraveler():
    from modelos_atraveler import load_modelos_atraveler
    load_modelos_atraveler()

# Barra lateral para la navegación
st.sidebar.title("Navegación")
page = st.sidebar.selectbox("Selecciona una página", ("Inicio", "Análisis Profe Kyle", "Analisis Atraveler Teacher", "Modelos Profe Kyle", "Modelos Atraveler Teacher"))

# Cargar la página correspondiente según la selección
if page == "Inicio":
    load_home()
elif page == "Análisis Profe Kyle":
    load_analisis()
elif page == "Analisis Atraveler Teacher":
    load_analisis_atraveler()
elif page == "Modelos Profe Kyle":
    load_modelos()
elif page == "Modelos Atraveler Teacher":
    load_modelos_atraveler()