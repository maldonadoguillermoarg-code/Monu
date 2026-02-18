import streamlit as st
import base64
import os
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import requests
from bs4 import BeautifulSoup

# --- CONFIGURACIÓN DE ALTO NIVEL ---
st.set_page_config(
    page_title="Monú | Boutique Astral & Global",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CORE ENGINE: MANEJO DE ASSETS ---
@st.cache_data
def get_base64_image(file_path):
    abs_path = os.path.join(os.getcwd(), file_path)
    if os.path.exists(abs_path):
        with open(abs_path, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# --- SCRAPER ENGINE (OPCIÓN 1 - REAL) ---
@st.cache_data(ttl=3600)
def fetch_product_details(url):
    """
    Extrae la descripción y fotos de la landing page que pongas en el Sheet.
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Buscamos la descripción técnica
        desc_div = soup.find('div', {'class': 'woocommerce-product-details__short-description'})
        if not desc_div:
            desc_div = soup.find('div', {'id': 'tab-description'})
        
        description = desc_div.get_text(separator="\n").strip() if desc_div else "Detalles exclusivos disponibles en nuestro showroom."
        
        # 2. Buscamos la imagen principal y galería
        # Si el link es una página, buscamos la imagen dentro; si es imagen directa, la devolvemos.
        images = []
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src')
            if src and ('uploads' in src or 'products' in src) and src.endswith(('.jpg', '.jpeg', '.png')):
                if src not in images: images.append(src)
        
        # La primera imagen suele ser la principal
        main_img = images[0] if images else url 
        return description, images[:4], main_img
    except:
        return "Cargando descripción astral...", [], url

# Assets
LOGO_HEADER = get_base64_image('MonumarcaLogoNegro.png')
IMG_BANNER_ENVIO = get_base64_image('envio.jpeg') 
LOGO_WATERMARK = get_base64_image('MonuMarcaDeAgua1.png')

# --- UI FRAMEWORK: CSS CUSTOM ---
watermark_css = f"""
    background-image: url("data:image/png;base64,{LOGO_WATERMARK}");
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center;
    background-size: 45%;
    opacity: 0.12;
""" if LOGO_WATERMARK else ""

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;400;600&display=swap');

    /* Tipografía Negra y Estética Global */
    * {{ color: #000000 !important; font-family: 'Inter', sans-serif; }}
    h1, h2, h3, .cinzel {{ font-family: 'Cinzel', serif !important; font-weight: 700; letter-spacing: 2px; }}

    .stApp {{ background-color: #F5F5F5; }}
    .bg-watermark {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; {watermark_css} z-index: -1; }}

    /* HEADER FIJO */
    .header {{
        position: fixed; top: 0; left: 0; width: 100%; height: 140px;
        background: rgba(255,255,255,0.99); border-bottom: 1px solid #000;
        display: flex; justify-content: space-between; align-items: center;
        padding: 0 50px; z-index: 1000;
    }}
    .logo-img-header {{ max-height: 140px; width: auto; padding: 5px 0; }}
    .nav-links {{ display: flex; gap: 40px; }}
    .nav-item {{ text-decoration: none; font-size: 1.1rem; cursor: pointer; font-weight: 700; }}

    /* BANNER */
    .hero-container-full {{ margin-top: 140px; width: 100vw; margin-left: -5rem; background: white; border-top: 1px solid #000; border-bottom: 1px solid #000; display: flex; justify-content: center; overflow: hidden; }}
    .img-banner-envio {{ width: 100%; max-width: 1200px; height: auto; }}
    .aesthetic-subtitle {{ text-align: center; margin-top: 15px; font-size: 0.9rem; letter-spacing: 8px; font-style: italic; opacity: 0.8; text-transform: uppercase; }}

    /* CARDS - Estructura estanca para evitar removeChild error */
    .card-info-box {{
        background: white; border: 1px solid #E0E0E0; padding: 20px; text-align: center;
    }}
    
    .stButton>button {{ width: 100%; background-color: #000 !important; color: #FFF !important; border: none; padding: 12px; font-weight: 600; border-radius: 0; }}
    .info-btn-style>div>button {{ background-color: #FFF !important; color: #000 !important; border: 1px solid #000 !important; margin-bottom: 10px; }}

    header, footer {{ visibility: hidden; }}
    </style>
    <div class="bg-watermark"></div>
    """, unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'cart' not in st.session_state: st.session_state.cart = []
if 'view_product' not in st.session_state: st.session_state.view_product = None

# --- HEADER RENDER ---
logo_header_html = f'<img src="data:image/png;base64,{LOGO_HEADER}" class="logo-img-header">' if LOGO_HEADER else '<h1>MONÚ</h1>'
st.markdown(f"""
    <div class="header">
        <div>{logo_header_html}</div>
        <div class="nav-links">
            <a href="#productos" class="nav-item cinzel">CATÁLOGO</a>
            <a class="nav-item cinzel" style="color:#A66355 !important;">CARRITO ({len(st.session_state.cart)})</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- BANNER ---
st.markdown(f'<div class="hero-container-full"><img src="data:image/png;base64,{IMG_BANNER_ENVIO}" class="img-banner-envio"></div><p class="aesthetic-subtitle">Tienda Online</p>', unsafe_allow_html=True)

# --- PRODUCTOS (GRID - INTEGRACIÓN GOOGLE SHEETS) ---
st.markdown('<div id="productos" style="padding: 40px;">', unsafe_allow_html=True)

sheet_url = "https://docs.google.com/spreadsheets/d/13WPtfzC4qY-Z3nu4kJv6vnVEneI_ikyDtUBuNzl83Fc/edit?usp=sharing"
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=sheet_url)
    PRODUCTOS_SHEET = df.to_dict('records')
except:
    PRODUCTOS_SHEET = []

cols = st.columns(2)
for i, p in enumerate(PRODUCTOS_SHEET):
    # Aquí es donde ocurre la magia del scraper usando el link de la columna "img"
    desc_temp, fotos_temp, img_preview = fetch_product_details(p['img'])
    
    with cols[i % 2]:
        # Contenedor estético (HTML)
        st.markdown(f"""
            <div class="card-info-box">
                <img src="{img_preview}" style="width:100%; height:400px; object-fit:cover;">
                <h3 class="cinzel" style="margin: 15px 0;">{p['nombre']}</h3>
                <h2 style="margin-bottom:20px;">${int(p['precio']):,}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Botones Nativos (Fuera del markdown para evitar el error removeChild)
        with st.container():
            st.markdown('<div class="info-btn-style">', unsafe_allow_html=True)
            if st.button(f"VER INFORMACIÓN", key=f"info_{p['id']}"):
                st.session_state.view_product = {"data": p, "desc": desc_temp, "fotos": fotos_temp}
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

            if st.button(f"AÑADIR AL PEDIDO", key=f"add_{p['id']}"):
                st.session_state.cart.append(p)
                st.rerun()
        st.write("") # Espaciador

st.markdown('</div>', unsafe_allow_html=True)

# --- SIDEBAR DE DETALLES (FICHA TÉCNICA) ---
if st.session_state.view_product:
    vp = st.session_state.view_product
    with st.sidebar:
        st.markdown(f"<h2 class='cinzel'>{vp['data']['nombre']}</h2>", unsafe_allow_html=True)
        st.image(vp['data']['img'], use_container_width=True)
        st.markdown(f"### ${int(vp['data']['precio']):,}")
        st.divider()
        st.markdown("#### Descripción Técnica")
        st.write(vp['desc'])
        
        if vp['fotos']:
            st.markdown("#### Galería de Fotos")
            for f in vp['fotos']:
                st.image(f, use_container_width=True)
        
        if st.button("CERRAR FICHA"):
            st.session_state.view_product = None
            st.rerun()

# --- FOOTER ---
st.markdown(f"""
    <div style="background: white; padding: 50px; text-align: center; border-top: 1px solid #000;" id="contacto">
        <h2 class="cinzel">CONECTÁ CON MONÚ</h2>
    </div>
    """, unsafe_allow_html=True)