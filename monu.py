import streamlit as st
import base64
import os
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import requests

# Manejo preventivo para que la app no muera si falta bs4
try:
    from bs4 import BeautifulSoup
except ImportError:
    st.error("⚠️ Falta instalar 'beautifulsoup4'. Revisá tu requirements.txt")

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

# --- SCRAPER ENGINE ---
@st.cache_data(ttl=3600)
def fetch_product_details(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        desc_div = soup.find('div', {'class': 'woocommerce-product-details__short-description'}) or soup.find('div', {'id': 'tab-description'})
        description = desc_div.get_text(separator="\n").strip() if desc_div else "Inspiración Monú: Detalles en showroom."
        
        images = []
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src')
            if src and ('uploads' in src or 'products' in src) and src.endswith(('.jpg', '.png')):
                if src not in images: images.append(src)
        
        return description, images[:4]
    except:
        return "Conectando con el showroom...", []

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
    * {{ color: #000000 !important; font-family: 'Inter', sans-serif; }}
    h1, h2, h3, .cinzel {{ font-family: 'Cinzel', serif !important; font-weight: 700; letter-spacing: 2px; }}
    .stApp {{ background-color: #F5F5F5; }}
    .bg-watermark {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; {watermark_css} z-index: -1; }}
    .header {{
        position: fixed; top: 0; left: 0; width: 100%; height: 140px;
        background: white; border-bottom: 1px solid #000;
        display: flex; justify-content: space-between; align-items: center;
        padding: 0 50px; z-index: 1000;
    }}
    .logo-img-header {{ max-height: 140px; width: auto; }}
    .hero-container-full {{ margin-top: 140px; width: 100vw; margin-left: -5rem; background: white; border-top: 1px solid #000; border-bottom: 1px solid #000; display: flex; justify-content: center; overflow: hidden; }}
    .img-banner-envio {{ width: 100%; max-width: 1200px; height: auto; }}
    .card-box {{ background: white; border: 1px solid #E0E0E0; padding: 20px; text-align: center; }}
    .stButton>button {{ width: 100%; background-color: #000 !important; color: #FFF !important; border-radius: 0; padding: 12px; font-weight: 600; border: none; }}
    .info-btn-style>div>button {{ background-color: #FFF !important; color: #000 !important; border: 1px solid #000 !important; margin-bottom: 8px; }}
    header, footer {{ visibility: hidden; }}
    </style>
    <div class="bg-watermark"></div>
    """, unsafe_allow_html=True)

# --- STATE ---
if 'cart' not in st.session_state: st.session_state.cart = []
if 'view_product' not in st.session_state: st.session_state.view_product = None

# --- UI RENDER ---
logo_html = f'<img src="data:image/png;base64,{LOGO_HEADER}" class="logo-img-header">' if LOGO_HEADER else '<h1>MONÚ</h1>'
st.markdown(f'<div class="header"><div>{logo_html}</div><div class="cinzel">CARRITO ({len(st.session_state.cart)})</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="hero-container-full"><img src="data:image/png;base64,{IMG_BANNER_ENVIO}" class="img-banner-envio"></div>', unsafe_allow_html=True)

# --- PRODUCTOS ---
st.markdown('<div style="padding: 40px;">', unsafe_allow_html=True)

sheet_url = "https://docs.google.com/spreadsheets/d/13WPtfzC4qY-Z3nu4kJv6vnVEneI_ikyDtUBuNzl83Fc/edit?usp=sharing"
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=sheet_url)
    PRODUCTOS = df.to_dict('records')
except Exception as e:
    st.error(f"Error vinculando con el showroom: {e}")
    PRODUCTOS = []

cols = st.columns(2)
for i, p in enumerate(PRODUCTOS):
    # Verificación defensiva de columnas para evitar KeyError
    p_id = p.get('id', f'prod_{i}')
    p_nombre = p.get('nombre', 'Producto Monú')
    p_precio = p.get('precio', 0)
    p_img = p.get('img', '')

    with cols[i % 2]:
        st.markdown(f'<div class="card-box"><img src="{p_img}" style="width:100%; height:400px; object-fit:cover;"><h3 class="cinzel" style="margin: 15px 0;">{p_nombre}</h3><h2 style="margin-bottom:20px;">${int(p_precio):,}</h2></div>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="info-btn-style">', unsafe_allow_html=True)
            if st.button(f"INFO TÉCNICA", key=f"info_{p_id}"):
                desc, fotos = fetch_product_details(p_img)
                st.session_state.view_product = {"data": p, "desc": desc, "fotos": fotos}
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            if st.button(f"AÑADIR AL PEDIDO", key=f"add_{p_id}"):
                st.session_state.cart.append(p)
                st.rerun()
        st.write("")
st.markdown('</div>', unsafe_allow_html=True)

# --- SIDEBAR DETALLES ---
if st.session_state.view_product:
    vp = st.session_state.view_product
    with st.sidebar:
        st.markdown(f"<h2 class='cinzel'>{vp['data'].get('nombre', 'Producto')}</h2>", unsafe_allow_html=True)
        st.image(vp['data'].get('img', ''), use_container_width=True)
        st.write(vp['desc'])
        for f in vp['fotos']: st.image(f, use_container_width=True)
        if st.button("VOLVER"):
            st.session_state.view_product = None
            st.rerun()