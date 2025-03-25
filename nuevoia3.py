import streamlit as st
import pandas as pd
import google.generativeai as genai
import time

# Initialize the Gemini API
genai.configure(api_key=st.secrets["API_KEY_GENAI"])
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

# Function to get analysis and initial recommendations
def obtener_analisis_y_recomendaciones(data_description):
    prompt = f"Analiza el siguiente conjunto de datos:\n{data_description}\nRealiza Preguntas basicas a responder y plantea hipotesis a trabajar sobre el mismo, análisis EDA, analiza mejoras y proporciona recomendaciones, realiza tambien un analisis multivariado y por último muestra un desarrollo en Python para el mismo utilizando las librerías de ciencia de datos estándar que mas se ajusen al modelo."
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Ocurrió un error al obtener el análisis: {e}"

# Título de la aplicación
st.title('📊 Generador EDA con IA')

# Introducción
st.markdown("""
    ✅Esta aplicación permite subir archivos (CSV, JSON, XLSX) para realizar un análisis descriptivo.
    Obtendrás los primeros registros del dataset, podrás elegir la hoja a trabajar (si aplica)
    y recibir recomendaciones a partir de un análisis exploratorio de datos (EDA). Comienza subiendo tu archivo en el selector
""", unsafe_allow_html=True)

# Componentes clave de EDA
st.markdown("""
    
    <p>
    <strong style="color: blue;">ESTADÍSTICAS DESCRIPTIVAS:</strong> Incluyen medidas como la media, mediana, moda, desviación estándar y percentiles.<br>
    
    <strong style="color: blue;">VISUALIZACIÓN DE DATOS:</strong> Uso de gráficos como histogramas, diagramas de caja (boxplots), gráficos de dispersión (scatter plots) y diagramas de barras.<br>
    
    <strong style="color: blue;">IDENTIFICACIÓN DE VALORES FALTANTES:</strong> Evaluar la cantidad y los patrones de datos faltantes.<br>
    
    <strong style="color: blue;">RELACIONES ENTRE VARIABLES:</strong> Explorar cómo las variables se relacionan entre sí, usando gráficos y correlaciones.<br>
    
    <strong style="color: blue;">DISTRIBUCIONES:</strong> Examinar la distribución de variables para entender su comportamiento y forma.<br>
    
    <strong style="color: blue;">IMPORTANCIA DE EDA:</strong> Es crucial para entender el contexto y las dinámicas de los datos.
    </p>
""", unsafe_allow_html=True)

# Título en el sidebar con color usando markdown
st.sidebar.markdown('<h2 style="color: blue;"> 📁 Selector de Archivos</h2>', unsafe_allow_html=True)

# Agregar una imagen decorativa relacionada con ciencia de datos desde Internet
st.sidebar.image('https://www.gaceta.unam.mx/wp-content/uploads/2020/08/200820-aca1-des-f1-Ciencia-de-Datos.jpg', caption='Ciencia de Datos', use_container_width=True)

# Verificar el tamaño del archivo con una clave única
uploaded_file = st.sidebar.file_uploader("⏫Sube tu archivo (CSV, JSON, XLSX)", type=["csv", "json", "xlsx"], key="file_uploader_1")

# Acerca de...
st.sidebar.header('Creditos ✅')
st.sidebar.markdown("""
    Esta aplicación está diseñada para facilitar el análisis exploratorio de datos utilizando inteligencia artificial.<br>
    Se recomienda subir archivos bien estructurados y del tamaño adecuado.
    
    <span style="color: red;">**Programador:** Juan Manuel Olguin</span><br>
    **//Licenciado en Informática**<br>
    **Full-Stack Developer y Data Scientist//**<br>
""", unsafe_allow_html=True)

# Agregar iconos de LinkedIn y GitHub justificados a la derecha
st.sidebar.markdown("""
                    <h5 style="text-align: left;">Contacto:</h5>
    <div style="text-align: center;">
        <a href="https://www.linkedin.com/in/juano34519842/" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/e/e9/Linkedin_icon.svg" alt="LinkedIn" style="width: 30px; height: 30px; margin-right: 10px;">
        </a>
        <a href="https://github.com/Juanolguin21/" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub" style="width: 30px; height: 30px;">
        </a>
    </div>
""", unsafe_allow_html=True)

# Verificar el tamaño del archivo

if uploaded_file is not None:
    if uploaded_file.size > 200 * 1024 * 1024:  # 200 MB en bytes
        st.sidebar.error("El archivo es demasiado grande. No se permite el ingreso de archivos mayores a 200 MB.")
    else:
        with st.spinner('Cargando y analizando el archivo...'):
            time.sleep(1)  # Simula un pequeño retraso para visualizar el spinner.

            # Cargar los datos según el tipo de archivo
            try:
                if uploaded_file.type == "text/csv":
                    data = pd.read_csv(uploaded_file, dtype={'columna1': str, 'columna2': float})
                elif uploaded_file.type == "application/json":
                    data = pd.read_json(uploaded_file)
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                    xls = pd.ExcelFile(uploaded_file)
                    sheet_names = xls.sheet_names

                    # Si hay más de una hoja, mostrar el dropdown en la sección principal
                    if len(sheet_names) > 1:
                        selected_sheet = st.selectbox(
                            f"Selecciona la hoja a trabajar (por defecto se elige: {sheet_names[0]}):", 
                            sheet_names
                        )
                        data = pd.read_excel(xls, sheet_name=selected_sheet)
                    else:
                        data = pd.read_excel(xls, sheet_name=sheet_names[0])

                # Mostrar los primeros registros del archivo
                st.subheader("Primeros registros del archivo:")
                st.dataframe(data.head())

                # Crear un resumen del DataFrame
                data_summary = {
                    "Métrica": [
                        "Número de filas",
                        "Número de columnas",
                        "Columnas",
                        "Tipos de datos",
                        "Valores faltantes"
                    ],
                    "Descripción": [
                        len(data),
                        len(data.columns),
                        ', '.join(data.columns),
                        data.dtypes.to_string(),
                        data.isnull().sum().to_string()
                    ]
                }

                summary_df = pd.DataFrame(data_summary)

                # Mostrar descripción del conjunto de datos
                st.subheader("Descripción del conjunto de datos:")
                st.dataframe(summary_df)

                # Obtener análisis y recomendaciones relevantes
                recomendaciones = obtener_analisis_y_recomendaciones(summary_df.to_string())
                
                st.subheader("Recomendaciones obtenidas de la IA:")
                st.write(recomendaciones)

            except Exception as e:
                st.error(f"Ocurrió un error al cargar el archivo: {e}")