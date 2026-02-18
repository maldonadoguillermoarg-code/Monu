import streamlit as st
import base64
import os

# --- CONFIGURACIÓN DE NIVEL MUNDIAL ---
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
# CAMBIO QUIRÚRGICO: Nueva imagen de fondo solicitada
LOGO_WATERMARK = get_base64_image('MonuMarcaDeAgua1.png')

# --- DEFINICIÓN DE PRODUCTOS (EMIDICA READY) ---
PRODUCTOS = [
    {
        "id": "M001",
        "nombre": "Bala Labial 10 Vel.",
        "precio": 19999,
        "img": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=800",
        "categoria": "Bienestar",
        "descripcion": "Elegancia y placer en un solo diseño místico."
    },
    {
        "id": "M002",
        "nombre": "Conjunto Puntilla Soft",
        "precio": 14000,
        "img": "https://images.unsplash.com/photo-1541310588484-ad456b40e94f?w=800",
        "categoria": "Lencería",
        "descripcion": "Suavidad astral para tus momentos más íntimos."
    },
    {
        "id": "M003",
        "nombre": "Lubricante Anal LUBE",
        "precio": 11000,
        "img": "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800",
        "categoria": "Cuidado",
        "descripcion": "Calidad premium para una experiencia sin límites."
    },
    {
        "id": "M004",
        "nombre": "Body Splash SEXITIVE",
        "precio": 11000,
        "img": "https://images.unsplash.com/photo-1594035910387-fea47794261f?w=800",
        "categoria": "Fragancias",
        "descripcion": "Aromas que conectan con tu energía interior."
    }
]

# --- UI FRAMEWORK: CSS CUSTOM ---
watermark_css = f"""
    background-image: url("data:image/png;base64,{LOGO_WATERMARK}");
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center;
    background-size: 30%;
    opacity: 0.05;
""" if LOGO_WATERMARK else ""

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;400;600&display=swap');

    /* Estética Global: Tipografía Negra */
    * {{ color: #000000 !important; font-family: 'Inter', sans-serif; }}
    h1, h2, h3, .cinzel {{ font-family: 'Cinzel', serif !important; font-weight: 700; letter-spacing: 2px; }}

    .stApp {{ background-color: #FFFFFF; }}
    
    .bg-watermark {{
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        {watermark_css} z-index: -1;
    }}

    /* Header Estilo Boutique */
    .header {{
        position: fixed; top: 0; left: 0; width: 100%; height: 115px;
        background: rgba(255,255,255,0.98); border-bottom: 1px solid #000;
        display: flex; justify-content: space-between; align-items: center;
        padding: 0 50px; z-index: 1000;
    }}
    /* CAMBIO QUIRÚRGICO: Logo 15% más grande (de 80px a 92px) */
    .logo-img {{ max-height: 92px; }}
    
    .nav-links {{ display: flex; gap: 40px; }}
    .nav-item {{ text-decoration: none; font-size: 1rem; cursor: pointer; border-bottom: 2px solid transparent; transition: 0.3s; }}
    .nav-item:hover {{ border-bottom: 2px solid #A66355; }}

    /* Layout de Productos */
    .main-content {{ margin-top: 150px; padding: 40px; }}
    
    .card {{
        background: white; border: 1px solid #F0F0F0; padding: 20px;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    .card:hover {{ border: 1px solid #A66355; transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0,0,0,0.05); }}
    
    /* Botonera Premium */
    .stButton>button {{
        width: 100%; border-radius: 0; background-color: #A66355 !important;
        color: #000 !important; border: none; padding: 15px; font-weight: 600;
        letter-spacing: 2px; transition: 0.3s;
    }}
    .stButton>button:hover {{ background-color: #000 !important; color: #FFF !important; }}

    /* Footer Profesional */
    .footer {{
        background: #F9F9F9; padding: 50px; margin-top: 50px;
        border-top: 1px solid #EEE; text-align: center;
    }}
    .social-icons {{ display: flex; justify-content: center; gap: 30px; margin: 20px 0; }}
    .social-icons a {{ text-decoration: none; font-weight: 700; }}

    /* Sidebar Fix */
    [data-testid="stSidebar"] {{ background-color: #FFF; border-left: 1px solid #EEE; }}
    header, footer {{ visibility: hidden; }}
    </style>
    <div class="bg-watermark"></div>
    """, unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- HEADER RENDER ---
logo_html = f'<img src="data:image/png;base64,{LOGO_HEADER}" class="logo-img">' if LOGO_HEADER else '<h1>MONÚ</h1>'

# CAMBIO QUIRÚRGICO: El link del carrito ahora apunta a una página nueva (mockup)
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

# --- MAIN CONTENT ---
st.markdown('<div class="main-content" id="productos">', unsafe_allow_html=True)

# Hero Section
st.markdown("<h1 style='text-align:center; font-size: 3rem;'>MONÚ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; letter-spacing: 5px; margin-bottom: 50px;'>ESTÉTICA • PODER • CONEXIÓN</p>", unsafe_allow_html=True)

# Grid de Productos
cols = st.columns(2)
for i, p in enumerate(PRODUCTOS):
    with cols[i % 2]:
        st.markdown(f"""
            <div class="card">
                <img src="{p['img']}" style="width:100%; height:400px; object-fit:cover;">
                <p style="margin-top:15px; font-size: 0.8rem; color: #A66355 !important;">{p['categoria'].upper()}</p>
                <h3 style="margin: 10px 0;">{p['nombre']}</h3>
                <p style="font-size: 0.9rem; margin-bottom:15px;">{p['descripcion']}</p>
                <h2 style="margin-bottom:20px;">${p['precio']:,}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"AÑADIR AL CARRITO", key=f"add_{p['id']}"):
            st.session_state.cart.append(p)
            st.toast(f"✨ {p['nombre']} agregado.")
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER & CONTACTO ---
st.markdown(f"""
    <div class="footer" id="contacto">
        <h2 class="cinzel">CONECTÁ CON MONÚ</h2>
        <p>Estamos para asesorarte en tu búsqueda astral.</p>
        <div class="social-icons">
            <a href="https://instagram.com/tu_cuenta" target="_blank">INSTAGRAM</a>
            <a href="mailto:contacto@monu.com">EMAIL</a>
            <a href="https://wa.me/5491112345678">WHATSAPP</a>
        </div>
        <p style="font-size: 0.7rem; margin-top: 30px; opacity: 0.6;">© 2026 MONÚ BOUTIQUE. TODOS LOS DERECHOS RESERVADOS.</p>
    </div>
    """, unsafe_allow_html=True)