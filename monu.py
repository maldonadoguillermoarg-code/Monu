import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import base64

# --- CONFIGURACIÓN DE NIVEL SUPER SENIOR ---
st.set_page_config(page_title="Monú | Boutique", layout="wide")

# --- ESTILOS: TYPOGRAPHY BLACK & LOGO BIG ---
def local_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&display=swap');
        
        /* Typography Always Black */
        * { color: #000000 !important; }
        
        /* Logo más grande y centrado */
        .logo-container {
            display: flex;
            justify-content: center;
            padding: 20px 0;
        }
        .main-logo {
            width: 300px; /* Logo más grande como pediste */
            filter: drop-shadow(0px 4px 4px rgba(0,0,0,0.1));
        }

        /* Background con transparencia reducida */
        .stApp {
            background-color: rgba(255, 255, 255, 0.95); /* Menos transparencia */
        }

        .product-card {
            border: 1px solid #000;
            padding: 20px;
            border-radius: 0px; /* Estilo minimalista boutique */
            text-align: center;
            margin-bottom: 20px;
            background: #fff;
        }

        .buy-button {
            background-color: #000 !important;
            color: #fff !important;
            padding: 10px 20px;
            text-decoration: none;
            font-weight: bold;
            display: inline-block;
            margin-top: 10px;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

local_css()

# --- CONEXIÓN QUIRÚRGICA CON TU SHEET ---
# Tu link: https://docs.google.com/spreadsheets/d/13WPtfzC4qY-Z3nu4kJv6vnVEneI_ikyDtUBuNzl83Fc/edit?usp=sharing
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/13WPtfzC4qY-Z3nu4kJv6vnVEneI_ikyDtUBuNzl83Fc/edit?usp=sharing")
    
    # --- HEADER CON LOGO ---
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    # Aquí asumo que tienes el logo en la carpeta raíz. Si no, usa un link directo.
    st.image("MonumarcaLogoNegro.png", width=300) 
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; font-family: Cinzel;'>CATÁLOGO EXCLUSIVO</h1>", unsafe_allow_html=True)
    st.divider()

    # --- GRID DE PRODUCTOS ---
    if not df.empty:
        cols = st.columns(2) # Ideal para celulares en Argentina
        for index, row in df.iterrows():
            with cols[index % 2]:
                st.markdown(f"""
                    <div class="product-card">
                        <img src="{row['img']}" style="width:100%; aspect-ratio:1/1; object-fit:cover;">
                        <h2 style="font-size: 1.2rem; margin-top:10px;">{row['nombre']}</h2>
                        <p style="font-size: 1.5rem; font-weight: bold;">${row['precio']}</p>
                        <a href="https://wa.me/549XXXXXXXXXX?text=Hola!%20Quiero%20la%20{row['nombre']}" class="buy-button">COMPRAR AHORA</a>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.write("Cargando productos de la boutique...")

except Exception as e:
    st.error("Conectando con la base de datos de Monú...")