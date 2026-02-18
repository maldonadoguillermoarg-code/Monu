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

def inject_custom_css():
    st.markdown("""
    <style>
        /* 1. FORZAR FONDO GRIS CLARO EN TODA LA APP */
        html, body, [data-testid="stAppViewContainer"], .main {
            background-color: #F0F2F6 !important;
        }

        /* 2. FORZAR TEXTO NEGRO ABSOLUTO */
        * {
            color: #000000 !important;
            font-family: 'Helvetica', sans-serif;
        }

        /* 3. CONTENEDOR DE PRODUCTOS (Blanco para que resalte sobre el gris) */
        [data-testid="stVerticalBlock"] > div > div > .stVerticalBlock {
            background-color: #FFFFFF !important;
            border: 1px solid #000000;
            padding: 10px;
            border-radius: 4px;
        }

        /* 4. SIDEBAR (Gris un poco más oscuro para contraste) */
        [data-testid="stSidebar"] {
            background-color: #E0E2E6 !important;
            border-right: 2px solid #000000;
        }

        /* 5. BOTONES (Estilo Minimalista B&W) */
        div.stButton > button {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            border-radius: 2px !important;
            border: none !important;
            font-weight: bold;
        }
        
        div.stButton > button:hover {
            background-color: #444444 !important;
            color: #FFFFFF !important;
        }

        /* 6. INPUTS Y SELECTBOX (Fondo blanco para ver qué escribes) */
        .stSelectbox div[data-baseweb="select"] {
            background-color: #FFFFFF !important;
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
        st.session_state['cart'][prod_id]['qty'] += 1
    else:
        st.session_state['cart'][prod_id] = {'name': prod_name, 'price': prod_price, 'qty': 1}
    st.toast(f"Añadido: {prod_name}")