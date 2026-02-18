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

LOGO_HEADER = get_base64_image('LogoHorizontal2.png')
LOGO_WATERMARK = get_base64_image('MonuMarcaDeAgua1.png')

# --- UI FRAMEWORK: CSS CUSTOM (PASOS 1, 2, 3 y 4) ---
# Paso 2: Fondo Gris Humo para contraste
# Paso 4: Optimización de visibilidad del logo de fondo
watermark_css = f"""
    background-image: url("data:image/png;base64,{LOGO_WATERMARK}");
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center;
    background-size: 45%;
    opacity: 0.08; /* Aumentamos levemente para que se note sobre el gris */
""" if LOGO_WATERMARK else ""

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;400;600&display=swap');

    /* Estética Global: Tipografía Negra */
    * {{ color: #000000 !important; font-family: 'Inter', sans-serif; }}
    h1, h2, h3, .cinzel {{ font-family: 'Cinzel', serif !important; font-weight: 700; letter-spacing: 2px; }}

    /* Paso 2: Fondo Gris Humo Claro */
    .stApp {{ background-color: #F5F5F5; }}
    
    .bg-watermark {{
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        {watermark_css} z-index: -1;
    }}

    /* Header Estilo Boutique */
    .header {{
        position: fixed; top: 0; left: 0; width: 100%; height: 125px;
        background: rgba(255,255,255,0.99); border-bottom: 1px solid #000;
        display: flex; justify-content: space-between; align-items: center;
        padding: 0 50px; z-index: 1000;
    }}

    /* Paso 1: Logo de imagen 15% más grande respecto al anterior */
    .logo-img {{ 
        max-height: 105px; /* Escalado para protagonismo absoluto */
        width: auto;
    }}
    
    .nav-links {{ display: flex; gap: 40px; }}
    .nav-item {{ text-decoration: none; font-size: 1.1rem; cursor: pointer; border-bottom: 2px solid transparent; transition: 0.3s; font-weight: 700; }}
    .nav-item:hover {{ border-bottom: 2px solid #A66355; }}

    /* Paso 3: Rectángulo Monú minimalista y ceñido */
    .hero-container {{
        margin-top: 160px;
        display: flex;
        justify-content: center;
        width: 100%;
    }}
    .hero-box {{
        background: white;
        border: 1px solid #000;
        padding: 5px 30px; /* Ceñido al texto */
        display: inline-block;
        text-align: center;
    }}
    .hero-box h1 {{ margin: 0; font-size: 2.5rem; line-height: 1.2; }}

    /* Layout de Productos */
    .main-content {{ padding: 40px; }}
    
    .card {{
        background: white; border: 1px solid #E0E0E0; padding: 20px;
        transition: 0.4s;
    }}
    .card:hover {{ border: 1px solid #A66355; }}
    
    /* Botonera Premium */
    .stButton>button {{
        width: 100%; border-radius: 0; background-color: #A66355 !important;
        color: #000 !important; border: none; padding: 15px; font-weight: 600;
        letter-spacing: 2px;
    }}

    /* Sidebar Fix */
    [data-testid="stSidebar"] {{ background-color: #FFF; }}
    header, footer {{ visibility: hidden; }}
    </style>
    <div class="bg-watermark"></div>
    """, unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- HEADER RENDER ---
logo_html = f'<img src="data:image/png;base64,{LOGO_HEADER}" class="logo-img">' if LOGO_HEADER else '<h1>MONÚ</h1>'

st.markdown(f"""
    <div class="header">
        <div>{logo_html}</div>
        <div class="nav-links">
            <a href="#productos" class="nav-item cinzel">CATÁLOGO</a>
            <a href="#contacto" class="nav-item cinzel">CONTACTO</a>
            <a href="/carrito" target="_blank" class="nav-item cinzel" style="color:#A66355 !important;">CARRITO ({len(st.session_state.cart)})</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- PASO 3: RECTÁNGULO MONÚ CEÑIDO ---
st.markdown("""
    <div class="hero-container">
        <div class="hero-box">
            <h1 class="cinzel">MONÚ</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<p style='text-align:center; letter-spacing: 5px; margin-top: 20px; margin-bottom: 50px;'>ESTÉTICA • PODER • CONEXIÓN</p>", unsafe_allow_html=True)

# --- PRODUCTOS (GRID) ---
st.markdown('<div id="productos">', unsafe_allow_html=True)
PRODUCTOS = [
    {"id": "M001", "nombre": "Bala Labial 10 Vel.", "precio": 19999, "img": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=800"},
    {"id": "M002", "nombre": "Conjunto Puntilla Soft", "precio": 14000, "img": "https://images.unsplash.com/photo-1541310588484-ad456b40e94f?w=800"},
    {"id": "M003", "nombre": "Lubricante Anal LUBE", "precio": 11000, "img": "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800"},
    {"id": "M004", "nombre": "Body Splash SEXITIVE", "precio": 11000, "img": "https://images.unsplash.com/photo-1594035910387-fea47794261f?w=800"}
]

cols = st.columns(2)
for i, p in enumerate(PRODUCTOS):
    with cols[i % 2]:
        st.markdown(f"""
            <div class="card">
                <img src="{p['img']}" style="width:100%; height:400px; object-fit:cover;">
                <h3 style="margin: 15px 0;">{p['nombre']}</h3>
                <h2 style="margin-bottom:20px;">${p['precio']:,}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"AÑADIR AL PEDIDO", key=f"add_{p['id']}"):
            st.session_state.cart.append(p)
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown(f"""
    <div style="background: white; padding: 50px; margin-top: 50px; text-align: center; border-top: 1px solid #000;" id="contacto">
        <h2 class="cinzel">CONECTÁ CON MONÚ</h2>
        <div style="display: flex; justify-content: center; gap: 30px; margin: 20px 0;">
            <a href="#" style="font-weight: 700; text-decoration: none;">INSTAGRAM</a>
            <a href="mailto:contacto@monu.com" style="font-weight: 700; text-decoration: none;">EMAIL</a>
            <a href="https://wa.me/5491112345678" style="font-weight: 700; text-decoration: none;">WHATSAPP</a>
        </div>
    </div>
    """, unsafe_allow_html=True)