import streamlit as st
import base64
import os
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import requests

# Manejo preventivo de BeautifulSoup
try:
    from bs4 import BeautifulSoup
except ImportError:
    st.error("Por favor, añade 'beautifulsoup4' a tu requirements.txt")

# --- CONFIGURACIÓN DE ALTO NIVEL ---
st.set_page_config(
    page_title="Monú | Boutique Astral & Global",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CORE ENGINE: ASSETS ---
@st.cache_data
def get_base64_image(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return None

LOGO_HEADER = get_base64_image('MonumarcaLogoNegro.png')
IMG_BANNER_ENVIO = get_base64_image('envio.jpeg')

# --- SCRAPER ENGINE ---
@st.cache_data(ttl=3600)
def fetch_dropi_details(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Descripción
        desc_div = soup.find('div', {'class': 'woocommerce-product-details__short-description'}) or soup.find('div', {'id': 'tab-description'})
        description = desc_div.get_text(separator="\n").strip() if desc_div else "Inspiración Monú: Detalles en catálogo."
        
        # Imágenes
        images = []
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src')
            if src and ('uploads' in src or 'products' in src) and src.endswith(('.jpg', '.png')):
                if src not in images: images.append(src)
        return description, images[:3]
    except:
        return "Cargando detalles del showroom...", []

# --- CSS ESTABLE (Sin interferir con el DOM de Streamlit) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;600&display=swap');
    
    * {{ color: #000000 !important; font-family: 'Inter', sans-serif; }}
    .stApp {{ background-color: #F5F5F5; }}
    
    /* Header Fijo con corrección de z-index */
    .custom-header {{
        position: fixed; top: 0; left: 0; width: 100%; height: 140px;
        background: white; border-bottom: 1px solid #000;
        display: flex; justify-content: space-between; align-items: center;
        padding: 0 50px; z-index: 99;
    }}
    
    .logo-header {{ max-height: 100px; width: auto; }}
    
    /* Contenedor principal para evitar solapamiento */
    .main-wrapper {{ margin-top: 150px; }}
    
    .card {{ 
        background: white; border: 1px solid #E0E0E0; padding: 20px; 
        text-align: center; margin-bottom: 20px;
    }}
    
    .stButton>button {{ 
        width: 100%; background-color: #000 !important; color: #FFF !important; 
        border-radius: 0; border: none; font-weight: 600; 
    }}
    
    .secondary-button>div>button {{
        background-color: #FFF !important; color: #000 !important; 
        border: 1px solid #000 !important; margin-top: 5px;
    }}

    /* Ocultar elementos nativos que causan conflicto */
    header, footer {{ visibility: hidden; height: 0; }}
    </style>
""", unsafe_allow_html=True)

# --- UI RENDER: HEADER ---
logo_html = f'<img src="data:image/png;base64,{LOGO_HEADER}" class="logo-header">' if LOGO_HEADER else '<h1 class="cinzel">MONÚ</h1>'
st.markdown(f"""
    <div class="custom-header">
        <div>{logo_html}</div>
        <div style="font-family:'Cinzel'; font-weight:700; letter-spacing:2px;">
            CARRITO ({len(st.session_state.get('cart', []))})
        </div>
    </div>
""", unsafe_allow_html=True)

# --- CONTENIDO PRINCIPAL ---
st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

# Banner
if IMG_BANNER_ENVIO:
    st.image(f"data:image/png;base64,{IMG_BANNER_ENVIO}", use_container_width=True)

# Lógica de Productos
sheet_url = "https://docs.google.com/spreadsheets/d/13WPtfzC4qY-Z3nu4kJv6vnVEneI_ikyDtUBuNzl83Fc/edit?usp=sharing"
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=sheet_url)
    productos = df.to_dict('records')
except:
    productos = []

# Grid de Productos
cols = st.columns(2)
for i, p in enumerate(productos):
    with cols[i % 2]:
        st.markdown(f"""
            <div class="card">
                <img src="{p['img']}" style="width:100%; height:350px; object-fit:cover;">
                <h3 style="font-family:'Cinzel'; margin:15px 0;">{p['nombre']}</h3>
                <h2 style="margin-bottom:15px;">${int(p['precio']):,}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Botones (Nativos para evitar errores de Node)
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("INFO", key=f"btn_info_{p['id']}"):
                st.session_state.view_product = p
                st.rerun()
        with col_btn2:
            if st.button("AÑADIR", key=f"btn_add_{p['id']}"):
                if 'cart' not in st.session_state: st.session_state.cart = []
                st.session_state.cart.append(p)
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True) # Cierre de main-wrapper

# --- SIDEBAR DE DETALLES ---
if st.session_state.get('view_product'):
    p = st.session_state.view_product
    desc, fotos = fetch_dropi_details(p['img'])
    
    with st.sidebar:
        st.markdown(f"<h2 style='font-family:Cinzel;'>{p['nombre']}</h2>", unsafe_allow_html=True)
        st.image(p['img'], use_container_width=True)
        st.write(desc)
        for f in fotos:
            st.image(f, use_container_width=True)
        if st.button("VOLVER AL CATÁLOGO"):
            st.session_state.view_product = None
            st.rerun()