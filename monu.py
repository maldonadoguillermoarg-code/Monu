import streamlit as st
import base64
import os

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
    
    .bg-watermark {{
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        {watermark_css} z-index: -1;
    }}

    /* HEADER FIJO */
    .header {{
        position: fixed; top: 0; left: 0; width: 100%; height: 140px;
        background: rgba(255,255,255,0.99); border-bottom: 1px solid #000;
        display: flex; justify-content: space-between; align-items: center;
        padding: 0 50px; z-index: 1000;
    }}

    .logo-img-header {{ 
        max-height: 125px; 
        width: auto;
    }}
    
    .nav-links {{ display: flex; gap: 40px; }}
    .nav-item {{ text-decoration: none; font-size: 1.1rem; cursor: pointer; border-bottom: 2px solid transparent; transition: 0.3s; font-weight: 700; }}

    /* BANNER CENTRADO QUIRÚRGICAMENTE */
    .hero-container-full {{
        margin-top: 140px;
        width: 100%;
        background: white;
        border-top: 1px solid #000;
        border-bottom: 1px solid #000;
        display: flex;
        justify-content: center; /* CENTRADO HORIZONTAL */
        align-items: center;     /* CENTRADO VERTICAL */
        overflow: hidden;
        padding: 20px 0;
    }}
    
    .img-banner-envio {{
        width: auto;
        max-width: 90%; /* Para que no toque los bordes y respire */
        max-height: 350px; 
        display: block;
    }}

    .aesthetic-subtitle {{
        text-align: center;
        margin-top: 15px;
        font-size: 0.9rem;
        letter-spacing: 8px;
        font-style: italic;
        opacity: 0.8;
        text-transform: uppercase;
    }}

    .main-content {{ padding: 40px; }}
    .card {{ background: white; border: 1px solid #E0E0E0; padding: 20px; transition: 0.3s; }}
    .stButton>button {{ width: 100%; background-color: #A66355 !important; color: #000 !important; border: none; padding: 15px; font-weight: 600; }}

    header, footer {{ visibility: hidden; }}
    </style>
    <div class="bg-watermark"></div>
    """, unsafe_allow_html=True)

# --- HEADER ---
logo_header_html = f'<img src="data:image/png;base64,{LOGO_HEADER}" class="logo-img-header">' if LOGO_HEADER else '<h1>MONÚ</h1>'

st.markdown(f"""
    <div class="header">
        <div>{logo_header_html}</div>
        <div class="nav-links">
            <a href="#productos" class="nav-item cinzel">CATÁLOGO</a>
            <a href="#contacto" class="nav-item cinzel">CONTACTO</a>
            <a href="/carrito" target="_blank" class="nav-item cinzel" style="color:#A66355 !important;">CARRITO ({len(st.session_state.get('cart', []))})</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- BANNER CENTRAL ---
banner_envio_html = f'<img src="data:image/png;base64,{IMG_BANNER_ENVIO}" class="img-banner-envio">' if IMG_BANNER_ENVIO else '<h1 class="cinzel">COMO COMPRAR</h1>'

st.markdown(f"""
    <div class="hero-container-full">
        {banner_envio_html}
    </div>
    <p class="aesthetic-subtitle">Tienda Online</p>
    """, unsafe_allow_html=True)

# --- PRODUCTOS ---
st.markdown('<div class="main-content" id="productos">', unsafe_allow_html=True)
# ... (resto de la lógica de productos igual que antes)
