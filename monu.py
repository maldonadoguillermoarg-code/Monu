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

# --- UI FRAMEWORK: CSS CUSTOM OPTIMIZADO PARA MÓVILES ---
watermark_css = f"""
    background-image: url("data:image/png;base64,{LOGO_WATERMARK}");
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center;
    background-size: 80%; /* Más grande en móvil para que se note */
    opacity: 0.05;
""" if LOGO_WATERMARK else ""

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;400;600&display=swap');

    /* Reseteo de seguridad para móviles */
    html, body, [data-testid="stAppViewContainer"] {{
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }}

    * {{ color: #000000 !important; font-family: 'Inter', sans-serif; }}
    h1, h2, h3, .cinzel {{ font-family: 'Cinzel', serif !important; font-weight: 700; letter-spacing: 1px; }}

    .stApp {{ background-color: #F5F5F5; }}
    
    .bg-watermark {{
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        {watermark_css} z-index: -1;
    }}

    /* HEADER ADAPTATIVO */
    .header {{
        position: fixed; top: 0; left: 0; width: 100%; height: 100px;
        background: rgba(255,255,255,0.98); border-bottom: 1px solid #000;
        display: flex; justify-content: space-between; align-items: center;
        padding: 0 20px; z-index: 1000;
    }}

    .logo-img-header {{ 
        max-height: 70px; /* Reducido para móviles */
        width: auto;
    }}
    
    .nav-links {{ display: flex; gap: 15px; }}
    .nav-item {{ text-decoration: none; font-size: 0.8rem; font-weight: 700; }}

    /* BANNER MOBILE FIRST */
    .hero-container-full {{
        margin-top: 100px;
        width: 100%;
        background: white;
        border-bottom: 1px solid #000;
        display: flex;
        justify-content: center;
        padding: 15px 10px;
    }}
    
    .img-banner-envio {{
        width: 100%;
        max-width: 600px; 
        height: auto;
        border-radius: 8px;
    }}

    /* GÓNDOLA DE PRODUCTOS OPTIMIZADA */
    .main-content {{ padding: 20px 10px; }}
    
    .card {{ 
        background: white; 
        border: 1px solid #EEE; 
        padding: 15px; 
        margin-bottom: 20px;
        border-radius: 8px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
    }}
    
    .card img {{
        border-radius: 4px;
        margin-bottom: 15px;
    }}

    /* BOTÓN TOUCH-FRIENDLY (44px de altura mínimo) */
    .stButton>button {{ 
        width: 100%; 
        height: 50px;
        background-color: #A66355 !important; 
        color: #000 !important; 
        border-radius: 4px;
        font-weight: 700;
        text-transform: uppercase;
    }}

    /* Media Query para pantallas grandes (PC) */
    @media (min-width: 768px) {{
        .header {{ height: 140px; padding: 0 50px; }}
        .logo-img-header {{ max-height: 110px; }}
        .nav-item {{ font-size: 1.1rem; gap: 40px; }}
        .hero-container-full {{ margin-top: 140px; padding: 30px 0; }}
        .img-banner-envio {{ max-width: 1100px; }}
    }}

    header, footer, [data-testid="stHeader"] {{ visibility: hidden; }}
    </style>
    <div class="bg-watermark"></div>
    """, unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- HEADER ---
logo_header_html = f'<img src="data:image/png;base64,{LOGO_HEADER}" class="logo-img-header">' if LOGO_HEADER else '<h2 class="cinzel">MONÚ</h2>'

st.markdown(f"""
    <div class="header">
        <div>{logo_header_html}</div>
        <div class="nav-links">
            <a href="#productos" class="nav-item cinzel">PRODUCTOS</a>
            <a href="/carrito" target="_blank" class="nav-item cinzel" style="color:#A66355 !important;">🛒 ({len(st.session_state.cart)})</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- BANNER CENTRAL ---
banner_envio_html = f'<img src="data:image/png;base64,{IMG_BANNER_ENVIO}" class="img-banner-envio">' if IMG_BANNER_ENVIO else '<p>Pasos de compra</p>'

st.markdown(f"""
    <div class="hero-container-full">
        {banner_envio_html}
    </div>
    """, unsafe_allow_html=True)

# --- PRODUCTOS (GRID RESPONSIVE) ---
st.markdown('<div class="main-content" id="productos">', unsafe_allow_html=True)

PRODUCTOS = [
    {"id": "M001", "nombre": "Bala Labial 10 Vel.", "precio": 19999, "img": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=800"},
    {"id": "M002", "nombre": "Conjunto Puntilla Soft", "precio": 14000, "img": "https://images.unsplash.com/photo-1541310588484-ad456b40e94f?w=800"},
    {"id": "M003", "nombre": "Lubricante Anal LUBE", "precio": 11000, "img": "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800"},
    {"id": "M004", "nombre": "Body Splash SEXITIVE", "precio": 11000, "img": "https://images.unsplash.com/photo-1594035910387-fea47794261f?w=800"}
]

# Grid inteligente: Streamlit automáticamente maneja las columnas, pero el CSS las refuerza
cols = st.columns([1, 1] if st.get_option("theme.base") == "dark" else 2) 

for i, p in enumerate(PRODUCTOS):
    with cols[i % 2]:
        st.markdown(f"""
            <div class="card">
                <img src="{p['img']}" style="width:100%; height:auto; aspect-ratio:1/1; object-fit:cover;">
                <h3 style="margin: 10px 0; font-size: 1.1rem;">{p['nombre']}</h3>
                <h2 style="margin-bottom:15px; font-size: 1.4rem;">${p['precio']:,}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"AGREGAR", key=f"add_{p['id']}"):
            st.session_state.cart.append(p)
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown(f"""
    <div style="background: white; padding: 40px 20px; text-align: center; border-top: 1px solid #000;">
        <h2 class="cinzel" style="font-size: 1.2rem;">MONÚ</h2>
        <div style="display: flex; justify-content: center; gap: 20px; margin-top: 20px;">
            <a href="#" style="text-decoration: none; font-size: 0.8rem; font-weight: 700;">IG</a>
            <a href="#" style="text-decoration: none; font-size: 0.8rem; font-weight: 700;">WA</a>
        </div>
    </div>
    """, unsafe_allow_html=True)