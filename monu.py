import streamlit as st
import base64
import os
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import requests

# --- CONFIGURACIÓN DE ALTO NIVEL ---
st.set_page_config(
    page_title="Monú | Boutique Astral & Global",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CORE ENGINE: MANEJO DE ASSETS ---
def get_base64_image(file_path):
    abs_path = os.path.join(os.getcwd(), file_path)
    if os.path.exists(abs_path):
        with open(abs_path, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# --- SCRAPER ENGINE (OPCIÓN 1) ---
@st.cache_data(ttl=3600)
def fetch_dropi_details(product_id):
    """
    Simula la extracción de datos de la API/Web de Dropi.
    En una integración real, aquí se usaría requests.get() a la URL de Dropi.
    """
    # Esta es la base de la descripción técnica que traemos por ID
    desc_base = f"Este producto (ID {product_id}) forma parte de la colección exclusiva de Monú. " \
                "Diseñado con estándares de alta calidad, ideal para el público aesthetic que busca distinción. " \
                "Envío garantizado por Dropi Argentina."
    
    # Generamos links de fotos adicionales basados en el patrón de almacenamiento de Dropi
    fotos_extra = [
        f"https://dropi.com.co/storage/products/{product_id}/image_1.jpg",
        f"https://dropi.com.co/storage/products/{product_id}/image_2.jpg"
    ]
    return desc_base, fotos_extra

# Cargamos assets
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
    opacity: 0.08;
""" if LOGO_WATERMARK else ""

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;400;600&display=swap');

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
    .logo-img-header {{ max-height: 125px; width: auto; padding: 5px 0; }}
    .nav-links {{ display: flex; gap: 40px; }}
    .nav-item {{ text-decoration: none; font-size: 1.1rem; cursor: pointer; font-weight: 700; }}

    /* BANNER HERO */
    .hero-container-full {{ margin-top: 140px; width: 100vw; margin-left: -5rem; background: white; border-top: 1px solid #000; border-bottom: 1px solid #000; display: flex; justify-content: center; align-items: center; overflow: hidden; }}
    .img-banner-envio {{ width: 100%; max-width: 1200px; height: auto; display: block; }}
    .aesthetic-subtitle {{ text-align: center; margin-top: 15px; font-size: 0.9rem; letter-spacing: 8px; font-style: italic; opacity: 0.8; text-transform: uppercase; }}

    /* CARDS */
    .main-content {{ padding: 40px; }}
    .card {{ background: white; border: 1px solid #E0E0E0; padding: 20px; transition: 0.3s; text-align: center; }}
    .card:hover {{ border: 1px solid #000; }}
    
    /* Botones Personalizados */
    .stButton>button {{ width: 100%; background-color: #000 !important; color: #FFF !important; border: none; padding: 10px; font-weight: 600; border-radius: 0; margin-top: 5px; }}
    .info-btn>div>button {{ background-color: #FFF !important; color: #000 !important; border: 1px solid #000 !important; }}

    header, footer {{ visibility: hidden; }}
    </style>
    <div class="bg-watermark"></div>
    """, unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'cart' not in st.session_state: st.session_state.cart = []
if 'view_product' not in st.session_state: st.session_state.view_product = None

# --- HEADER ---
logo_header_html = f'<img src="data:image/png;base64,{LOGO_HEADER}" class="logo-img-header">' if LOGO_HEADER else '<h1>MONÚ</h1>'
st.markdown(f'<div class="header"><div>{logo_header_html}</div><div class="nav-links"><a href="#productos" class="nav-item cinzel">CATÁLOGO</a><a href="/carrito" target="_blank" class="nav-item cinzel" style="color:#A66355 !important;">CARRITO ({len(st.session_state.cart)})</a></div></div>', unsafe_allow_html=True)

# --- BANNER ---
st.markdown(f'<div class="hero-container-full">{f"<img src=\'data:image/png;base64,{IMG_BANNER_ENVIO}\' class=\'img-banner-envio\'>" if IMG_BANNER_ENVIO else "<h1 class=\'cinzel\'>COMO COMPRAR</h1>"}</div><p class="aesthetic-subtitle">Tienda Online</p>', unsafe_allow_html=True)

# --- PRODUCTOS ---
st.markdown('<div class="main-content" id="productos">', unsafe_allow_html=True)
sheet_url = "https://docs.google.com/spreadsheets/d/13WPtfzC4qY-Z3nu4kJv6vnVEneI_ikyDtUBuNzl83Fc/edit?usp=sharing"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=sheet_url)
    PRODUCTOS = df.to_dict('records')
except:
    PRODUCTOS = []

cols = st.columns(2)
for i, p in enumerate(PRODUCTOS):
    with cols[i % 2]:
        st.markdown(f"""
            <div class="card">
                <img src="{p['img']}" style="width:100%; height:400px; object-fit:cover;">
                <h3 style="margin: 15px 0; font-family: 'Cinzel', serif;">{p['nombre']}</h3>
                <h2 style="margin-bottom:20px;">${int(p['precio']):,}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Botón de Info (Scraper)
        st.markdown('<div class="info-btn">', unsafe_allow_html=True)
        if st.button(f"DETALLES TÉCNICOS", key=f"info_{p['id']}"):
            st.session_state.view_product = p
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button(f"AÑADIR AL PEDIDO", key=f"add_{p['id']}"):
            st.session_state.cart.append(p)
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- MODAL DE DETALLES (SCRAPER ACTIVO) ---
if st.session_state.view_product:
    p = st.session_state.view_product
    desc, fotos = fetch_dropi_details(p['id'])
    
    with st.sidebar: # Usamos el sidebar como panel de detalles elegante
        st.markdown(f"<h2 class='cinzel'>{p['nombre']}</h2>", unsafe_allow_html=True)
        st.image(p['img'])
        st.markdown(f"**Precio:** ${int(p['precio']):,}")
        st.write(desc)
        
        st.markdown("### Galería Dropi")
        st.image(fotos)
        
        if st.button("VOLVER AL CATÁLOGO"):
            st.session_state.view_product = None
            st.rerun()

# --- FOOTER ---
st.markdown(f"""
    <div style="background: white; padding: 50px; margin-top: 50px; text-align: center; border-top: 1px solid #000;" id="contacto">
        <h2 class="cinzel">CONECTÁ CON MONÚ</h2>
        <div style="display: flex; justify-content: center; gap: 30px; margin: 20px 0;">
            <a href="#" style="font-weight: 700; text-decoration: none; color:#000;">INSTAGRAM</a>
            <a href="https://wa.me/5491112345678" style="font-weight: 700; text-decoration: none; color:#000;">WHATSAPP</a>
        </div>
    </div>
    """, unsafe_allow_html=True)