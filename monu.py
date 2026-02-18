import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import requests
from bs4 import BeautifulSoup
import urllib.parse

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Monú | Boutique Astral & Global",
    page_icon="🎬",
    layout="wide"
)

# --- CONFIGURACIÓN DE PÁGINA (Debe ser la primera instrucción) ---
st.set_page_config(
    page_title="B&W Minimalist E-commerce",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INYECCIÓN DE CSS SEGURO (B&W Identity) ---
def inject_custom_css():
    st.markdown("""
    <style>
        /* Reset de Colores a Blanco y Negro */
        .stApp {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        
        /* Forzar texto negro absoluto en toda la app */
        h1, h2, h3, h4, p, span, div, label, .stMarkdown {
            color: #000000 !important;
            font-family: 'Inter', 'Helvetica', sans-serif;
        }

        /* Estilo de las Cards de Producto */
        .product-container {
            border: 2px solid #000000;
            padding: 20px;
            margin-bottom: 25px;
            background-color: #FFFFFF;
            transition: all 0.3s ease;
        }
        
        /* Botones Globales Minimalistas */
        div.stButton > button {
            border-radius: 0px !important;
            border: 2px solid #000000 !important;
            background-color: #FFFFFF !important;
            color: #000000 !important;
            width: 100%;
            font-weight: bold;
            text-transform: uppercase;
        }
        
        div.stButton > button:hover {
            background-color: #000000 !important;
            color: #FFFFFF !important;
        }

        /* Imagen con filtro escala de grises */
        img {
            filter: grayscale(100%);
            transition: 0.3s;
        }
        img:hover {
            filter: grayscale(0%);
        }

        /* Logo Centrado */
        .logo-wrapper {
            display: flex;
            justify-content: center;
            padding: 40px 0;
        }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE DATOS (GOOGLE SHEETS) ---
@st.cache_data(ttl=300) # Cache de 5 minutos para performance
def load_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        # Se asume que la URL está configurada en .streamlit/secrets.toml o en Streamlit Cloud Secrets
        df = conn.read()
        # Limpieza básica de datos
        df = df.dropna(subset=['id', 'nombre', 'precio'])
        return df
    except Exception as e:
        st.error(f"Error cargando base de datos: {e}")
        return pd.DataFrame()

# --- GESTIÓN DE CARRITO (SESSION STATE) ---
if 'cart' not in st.session_state:
    st.session_state['cart'] = {}

def add_to_cart(prod_id, prod_name, prod_price):
    if prod_id in st.session_state['cart']:
        st.session_state['cart'][prod_id]['