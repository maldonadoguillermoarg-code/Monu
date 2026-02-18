import streamlit as st
import base64
import os

# --- CONFIGURACIÓN PRO ---
st.set_page_config(
    page_title="Monú | Boutique Astral",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- FUNCIÓN ASSETS ---
def get_base64(bin_file):
    file_path = os.path.join(os.getcwd(), bin_file)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# Carga de recursos
logo_bg_base64 = get_base64('MonumarcaLogoNegro.png')
logo_header_base64 = get_base64('LogoHorizontal2.png')

# --- ESTILO QUIRÚRGICO SUPER PRO ---
# Bajamos la opacidad del fondo al 0.05 para que sea ultra sutil
fondo_style = ""
if logo_bg_base64:
    fondo_style = f"""
    background-image: url("data:image/png;base64,{logo_bg_base64}");
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center;
    background-size: 35%;
    opacity: 0.05; 
    """

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;400;600&display=swap');

    /* Reset y Tipografía Negra Total */
    html, body, [class*="st-"] {{
        color: #000000 !important;
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background-color: #FFFFFF;
    }}

    /* Marca de agua de fondo con transparencia controlada */
    .bg-watermark {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        {fondo_style}
        z-index: -1;
    }}

    /* HEADER FIJO PROFESIONAL */
    .fixed-header {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100px;
        background-color: rgba(255, 255, 255, 0.98);
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 40px;
        border-bottom: 1px solid #000000;
        z-index: 9999;
    }}
    
    .header-logo-img {{
        max-height: 80px; /* Logo más grande */
        width: auto;
    }}

    .nav-container {{
        display: flex;
        gap: 30px;
        align-items: center;
    }}

    .nav-btn {{
        background: none;
        border: none;
        color: #000000 !important;
        font-family: 'Cinzel', serif;
        font-weight: 700;
        letter-spacing: 2px;
        text-decoration: none;
        font-size: 0.9rem;
        cursor: pointer;
        text-transform: uppercase;
    }}

    /* Contenido principal */
    .main-container {{
        margin-top: 140px;
        padding: 0 5%;
    }}

    /* Cards Minimalistas */
    .product-card {{
        border: 1px solid #EEEEEE;
        padding: 20px;
        transition: 0.3s;
        background: white;
    }}
    .product-card:hover {{
        border: 1px solid #000000;
    }}

    /* Botones de Acción */
    .stButton>button {{
        width: 100%;
        border-radius: 0px;
        background-color: #000000;
        color: #FFFFFF !important;
        border: 1px solid #000000;
        padding: 12px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        letter-spacing: 2px;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background-color: #FFFFFF;
        color: #000000 !important;
    }}

    /* Ocultar elementos nativos */
    header, footer {{visibility: hidden;}}
    </style>
    <div class="bg-watermark"></div>
    """, unsafe_allow_html=True)

# --- LOGICA DE CARRITO ---
if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# --- HEADER RENDER ---
logo_content = f'<img src="data:image/png;base64,{logo_header_base64}" class="header-logo-img">' if logo_header_base64 else '<h1>MONÚ</h1>'

st.markdown(f"""
    <div class="fixed-header">
        <div style="cursor: pointer;">{logo_content}</div>
        <div class="nav-container">
            <a href="#catalogo" class="nav-btn">CATÁLOGO</a>
            <div class="nav-btn">CARRITO ({len(st.session_state.carrito)})</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- SECCIÓN CATÁLOGO ---
st.markdown('<div class="main-container" id="catalogo"></div>', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; font-family: Cinzel; letter-spacing: 10px; color: black;'>MONÚ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: black; letter-spacing: 3px; margin-bottom: 60px;'>CURADURÍA GLOBAL • SELECCIÓN ASTRAL</p>", unsafe_allow_html=True)

# Inventario vinculado a Emidica
productos = [
    {"id": 1, "nombre": "Bala Labial 10 Vel.", "precio": 19999, "img": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=500", "sku": "EMI-001"},
    {"id": 2, "nombre": "Conjunto Puntilla Soft", "precio": 14000, "img": "https://images.unsplash.com/photo-1541310588484-ad456b40e94f?w=500", "sku": "EMI-002"},
    {"id": 3, "nombre": "Lubricante Anal LUBE", "precio": 11000, "img": "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=500", "sku": "EMI-003"},
    {"id": 4, "nombre": "Body Splash SEXITIVE", "precio": 11000, "img": "https://images.unsplash.com/photo-1594035910387-fea47794261f?w=500", "sku": "EMI-004"}
]

cols = st.columns(2)
for i, prod in enumerate(productos):
    with cols[i % 2]:
        st.markdown(f"""
            <div class="product-card">
                <img src="{prod['img']}" style="width:100%; height:350px; object-fit:cover; margin-bottom:20px;">
                <h3 style="font-family: 'Cinzel'; color: black; font-size: 1.2rem; margin-bottom:10px;">{prod['nombre']}</h3>
                <p style="color: black; font-weight: 700; font-size: 1.3rem; margin-bottom:20px;">${prod['precio']:,}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"AGREGAR AL PEDIDO", key=f"btn_{prod['id']}"):
            st.session_state.carrito.append(prod)
            st.rerun()

# --- SIDEBAR (CARRITO PROFESIONAL) ---
with st.sidebar:
    st.markdown("<h2 style='font-family: Cinzel; color: black;'>TU PEDIDO</h2>", unsafe_allow_html=True)
    if not st.session_state.carrito:
        st.write("Tu selección está vacía.")
    else:
        total = sum(item['precio'] for item in st.session_state.carrito)
        resumen_ws = ""
        for item in st.session_state.carrito:
            st.markdown(f"**{item['nombre']}** \n${item['precio']:,} (Ref: {item['sku']})")
            resumen_ws += f"- {item['nombre']} ({item['sku']}): ${item['precio']:,}%0A"
        
        st.divider()
        st.markdown(f"### TOTAL: ${total:,}")
        
        # Link de WhatsApp con SKU para que sepas qué cargar en Emidica
        ws_url = f"https://wa.me/5491112345678?text=Hola Monú! ✨ Quiero concretar este pedido:%0A{resumen_ws}%0ATotal: ${total:,}"
        
        st.markdown(f"""
            <a href="{ws_url}" target="_blank" style="text-decoration: none;">
                <button style="width: 100%; background-color: #25d366; color: white; border: none; padding: 15px; font-weight: bold; cursor: pointer; letter-spacing: 1px;">
                    FINALIZAR PEDIDO 💬
                </button>
            </a>
        """, unsafe_allow_html=True)
        
        if st.button("LIMPIAR CARRITO"):
            st.session_state.carrito = []
            st.rerun()