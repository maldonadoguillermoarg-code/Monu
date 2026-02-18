import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import base64
import os

# --- CONFIGURACIÓN DE PÁGINA PROFESIONAL ---
st.set_page_config(page_title="Monú | Boutique", layout="wide", initial_sidebar_state="collapsed")

# Inicialización del carrito si no existe
if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- ESTILOS CSS (Respetando tipografía negra y logo grande) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;600&display=swap');
    
    * { color: #000000 !important; font-family: 'Inter', sans-serif; }
    .cinzel { font-family: 'Cinzel', serif !important; }
    
    .stApp { background-color: #FFFFFF; }
    
    /* Logo más grande y centrado */
    .logo-container { display: flex; justify-content: center; padding: 30px 0; }
    .main-logo { width: 350px; }

    /* Estilo de Tarjetas definido */
    .card {
        background: white;
        padding: 15px;
        border: 1px solid #000;
        text-align: center;
        margin-bottom: 10px;
    }
    
    /* Botones de Streamlit personalizados para que no rompan la estética */
    div.stButton > button {
        background-color: #000 !important;
        color: #fff !important;
        width: 100%;
        border-radius: 0px;
        border: none;
        font-weight: 700;
        letter-spacing: 1px;
    }
    
    header, footer, [data-testid="stHeader"] { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER CON LOGO ---
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
# Si tienes el logo localmente se carga aquí, sino puedes usar la URL del sheet
st.image("MonumarcaLogoNegro.png", width=350) 
st.markdown('</div>', unsafe_allow_html=True)

# --- CONEXIÓN A GOOGLE SHEETS (Brain de la tienda) ---
url = "https://docs.google.com/spreadsheets/d/13WPtfzC4qY-Z3nu4kJv6vnVEneI_ikyDtUBuNzl83Fc/edit?usp=sharing"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Leemos el sheet que contiene el catálogo de Dropi
    df = conn.read(spreadsheet=url)
    # Convertimos a la lista de diccionarios que procesa el loop
    PRODUCTOS = df.to_dict('records')
except Exception as e:
    st.error("Error conectando con el catálogo. Verifique el Sheet.")
    PRODUCTOS = []

# --- RENDERIZADO DE GÓNDOLA (Tu código integrado) ---
st.markdown('<div style="padding: 0 10px;">', unsafe_allow_html=True)

# Grid inteligente: Streamlit automáticamente maneja las columnas, pero el CSS las refuerza
cols = st.columns([1, 1] if st.get_option("theme.base") == "dark" else 2) 

for i, p in enumerate(PRODUCTOS):
    with cols[i % 2]:
        # Estructura de tarjeta respetada al 100%
        st.markdown(f"""
            <div class="card">
                <img src="{p['img']}" style="width:100%; height:auto; aspect-ratio:1/1; object-fit:cover;">
                <h3 style="margin: 10px 0; font-size: 1.1rem;">{p['nombre']}</h3>
                <h2 style="margin-bottom:15px; font-size: 1.4rem;">${int(p['precio']):,}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Botón con lógica de sesión
        if st.button(f"AGREGAR", key=f"add_{p['id']}"):
            st.session_state.cart.append(p)
            st.toast(f"Agregado: {p['nombre']}") # Feedback senior al usuario
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER (Tu código original respetado) ---
st.markdown(f"""
    <div style="background: white; padding: 40px 20px; text-align: center; border-top: 1px solid #000; margin-top: 50px;">
        <h2 class="cinzel" style="font-size: 1.2rem; font-weight: 700;">MONÚ</h2>
        <div style="display: flex; justify-content: center; gap: 20px; margin-top: 20px;">
            <a href="#" style="text-decoration: none; font-size: 0.8rem; font-weight: 700; color: #000;">IG</a>
            <a href="#" style="text-decoration: none; font-size: 0.8rem; font-weight: 700; color: #000;">WA</a>
        </div>
    </div>
    """, unsafe_allow_html=True)