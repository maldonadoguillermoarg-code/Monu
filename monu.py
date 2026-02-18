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

# --- FUNCIÓN SENIOR PARA ASSETS ---
def get_base64(bin_file):
    file_path = os.path.join(os.getcwd(), bin_file)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# Cargamos los logos
logo_bg_base64 = get_base64('MonumarcaLogoNegro.png')
logo_header_base64 = get_base64('LogoHorizontal2.png')

# --- ESTILO QUIRÚRGICO AESTHETIC ---
fondo_style = ""
if logo_bg_base64:
    fondo_style = f"""
    background-image: url("data:image/png;base64,{logo_bg_base64}");
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center;
    background-size: 35%;
    """

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;400;600&display=swap');

    /* Fondo con blur */
    .stApp {{
        background-color: #FFFFFF;
        {fondo_style}
    }}
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        z-index: -1;
    }}

    /* HEADER FIJO BLANCO (AESTHETIC) */
    .fixed-header {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 70px;
        background-color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        border-bottom: 1px solid #F2E8DF;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        z-index: 999999;
    }}
    
    .header-logo-img {{
        max-height: 45px;
        width: auto;
    }}

    /* Ajuste de margen para que el contenido no quede atrás del header */
    .main-content {{
        margin-top: 80px;
    }}

    /* Cards de Producto Minimalistas */
    .product-card {{
        background: white;
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #F8F1EB;
        text-align: center;
        margin-bottom: 20px;
        transition: 0.3s ease-in-out;
    }}
    .product-card:hover {{
        border: 1px solid #D4A373;
        box-shadow: 0 10px 20px rgba(212, 163, 115, 0.1);
    }}

    /* Botón Boutique */
    .stButton>button {{
        width: 100%;
        border-radius: 8px;
        background-color: #A66355;
        color: white;
        border: none;
        padding: 10px;
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 0.9rem;
        letter-spacing: 1px;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background-color: #5D3A32;
        color: #D4A373;
    }}

    /* Quitar padding innecesario de Streamlit */
    .block-container {{
        padding-top: 0rem;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- RENDER DEL HEADER FIJO ---
if logo_header_base64:
    st.markdown(f"""
        <div class="fixed-header">
            <img src="data:image/png;base64,{logo_header_base64}" class="header-logo-img">
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("<div class='fixed-header'><h2 style='font-family:Cinzel; margin:0;'>MONÚ</h2></div>", unsafe_allow_html=True)

# Contenedor para el contenido principal
st.markdown('<div class="main-content"></div>', unsafe_allow_html=True)

# --- SECCIÓN DE PRODUCTOS ---
st.markdown("<p style='text-align: center; color: #D4A373; font-family: Cinzel; letter-spacing: 4px; margin-bottom:30px;'>CURADURÍA ASTRAL</p>", unsafe_allow_html=True)

productos = [
    {"id": 1, "nombre": "Bala Labial 10 Vel.", "precio": 19999, "img": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=500"},
    {"id": 2, "nombre": "Conjunto Puntilla Soft", "precio": 14000, "img": "https://images.unsplash.com/photo-1541310588484-ad456b40e94f?w=500"},
    {"id": 3, "nombre": "Lubricante Anal LUBE", "precio": 11000, "img": "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=500"},
    {"id": 4, "nombre": "Body Splash SEXITIVE", "precio": 11000, "img": "https://images.unsplash.com/photo-1594035910387-fea47794261f?w=500"}
]

if 'carrito' not in st.session_state:
    st.session_state.carrito = []

cols = st.columns(2)
for i, prod in enumerate(productos):
    with cols[i % 2]:
        st.markdown(f"""
            <div class="product-card">
                <img src="{prod['img']}" style="width:100%; border-radius:10px; height:180px; object-fit:cover; margin-bottom:10px;">
                <h4 style="font-family: 'Cinzel'; color: #5D3A32; font-size: 1rem; margin-bottom:5px;">{prod['nombre']}</h4>
                <p style="font-size: 1.1rem; color: #A66355; font-weight: 600;">${prod['precio']:,}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"LO QUIERO", key=f"prod_{prod['id']}"):
            st.session_state.carrito.append(prod)
            st.toast(f"Añadido ✨")

# --- SIDEBAR (PEDIDO) ---
with st.sidebar:
    st.markdown("<h2 style='font-family: Cinzel; color: #5D3A32;'>Tu Pedido</h2>", unsafe_allow_html=True)
    if not st.session_state.carrito:
        st.write("Seleccioná tus favoritos.")
    else:
        total = sum(item['precio'] for item in st.session_state.carrito)
        resumen = ""
        for item in st.session_state.carrito:
            st.write(f"✨ {item['nombre']} - ${item['precio']:,}")
            resumen += f"- {item['nombre']} (${item['precio']:,})%0A"
        
        st.divider()
        st.markdown(f"### Total: ${total:,}")
        
        ws_msg = f"Hola Monú! ✨%0A{resumen}%0ATotal: ${total:,}"
        ws_url = f"https://wa.me/5491112345678?text={ws_msg}" 
        
        st.markdown(f"""
            <a href="{ws_url}" target="_blank" style="text-decoration: none;">
                <button style="width: 100%; border-radius: 8px; background-color: #25d366; color: white; border: none; padding: 12px; font-weight: bold; cursor: pointer;">
                    Finalizar por WhatsApp 💬
                </button>
            </a>
        """, unsafe_allow_html=True)
        
        if st.button("Limpiar"):
            st.session_state.carrito = []
            st.rerun()