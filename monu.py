import streamlit as st
import base64
import os

# --- CONFIGURACIÓN PRO ---
st.set_page_config(
    page_title="Monú | Esencia & Estilo",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- FUNCIÓN SENIOR PARA ASSETS ---
def get_base64(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# Cargamos los logos
logo_bg_base64 = get_base64('MonumarcaLogoNegro.png')
logo_header_base64 = get_base64('LogoHorizontal2.png')

# --- ESTILO QUIRÚRGICO DE ALTO NIVEL ---
fondo_style = ""
if logo_bg_base64:
    fondo_style = f"""
    background-image: url("data:image/png;base64,{logo_bg_base64}");
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center;
    background-size: 40%;
    """

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;400;600&display=swap');

    /* Fondo Maestro con Efecto Borroso */
    .stApp {{
        background-color: #FFFDFB;
        {fondo_style}
    }}
    
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(255, 253, 251, 0.88);
        backdrop-filter: blur(15px); /* El borroso pro que pediste */
        z-index: -1;
    }}

    /* Header Banner */
    .header-banner {{
        background: linear-gradient(135deg, #2D1B19 0%, #4A2C2A 100%);
        padding: 40px;
        border-radius: 0 0 50px 50px;
        text-align: center;
        margin: -80px -50px 40px -50px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }}
    
    .header-logo {{
        max-width: 280px;
        filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.3));
    }}

    /* Cards de Producto Estilo Boutique */
    .product-card {{
        background: rgba(255, 255, 255, 0.7);
        padding: 20px;
        border-radius: 25px;
        border: 1px solid rgba(166, 99, 85, 0.2);
        text-align: center;
        margin-bottom: 20px;
        transition: 0.4s;
    }}
    .product-card:hover {{
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(166, 99, 85, 0.15);
        border: 1px solid #A66355;
    }}

    /* Botón Monú */
    .stButton>button {{
        width: 100%;
        border-radius: 50px;
        background: #A66355;
        color: white;
        border: none;
        padding: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background: #2D1B19;
        color: #D4A373;
        transform: scale(1.02);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- RENDER DEL ENCABEZADO ---
if logo_header_base64:
    st.markdown(f"""
        <div class="header-banner">
            <img src="data:image/png;base64,{logo_header_base64}" class="header-logo">
            <p style="color: #D4A373; letter-spacing: 4px; font-family: 'Cinzel'; margin-top:15px;">ESENCIA ASTRAL & GLOBAL</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.title("MONÚ")

# --- INVENTARIO REAL (Extraído de tu Monú Inventario ) ---
productos = [
    {"id": 1, "nombre": "Bala Labial 10 Vel.", "precio": 19999, "img": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=500"},
    {"id": 2, "nombre": "Conjunto Puntilla Soft", "precio": 14000, "img": "https://images.unsplash.com/photo-1541310588484-ad456b40e94f?w=500"},
    {"id": 3, "nombre": "Lubricante Anal LUBE", "precio": 11000, "img": "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=500"},
    {"id": 4, "nombre": "Body Splash SEXITIVE", "precio": 11000, "img": "https://images.unsplash.com/photo-1594035910387-fea47794261f?w=500"}
]

# --- CARRITO ---
if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# --- GRID DE PRODUCTOS ---
cols = st.columns(2)
for i, prod in enumerate(productos):
    with cols[i % 2]:
        st.markdown(f"""
            <div class="product-card">
                <img src="{prod['img']}" style="width:100%; border-radius:15px; height:180px; object-fit:cover;">
                <h3 style="font-family: 'Cinzel'; color: #2D1B19; margin-top:15px;">{prod['nombre']}</h3>
                <p style="font-size: 1.4rem; font-weight: bold; color: #A66355;">${prod['precio']:,}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"Lo quiero", key=f"prod_{prod['id']}"):
            st.session_state.carrito.append(prod)
            st.toast(f"¡{prod['nombre']} añadido! ✨")

# --- SIDEBAR PROFESIONAL ---
with st.sidebar:
    st.markdown("<h2 style='font-family: Cinzel;'>Mi Pedido</h2>", unsafe_allow_html=True)
    if not st.session_state.carrito:
        st.info("Tu selección aparecerá aquí.")
    else:
        total = sum(item['precio'] for item in st.session_state.carrito)
        resumen = ""
        for item in st.session_state.carrito:
            st.write(f"🏷️ **{item['nombre']}** - ${item['precio']:,}")
            resumen += f"- {item['nombre']} (${item['precio']:,})%0A"
        
        st.divider()
        st.markdown(f"### Total: ${total:,}")
        
        # WhatsApp Botón
        ws_msg = f"Hola Monú! ✨ Quiero estos productos:%0A{resumen}%0ATotal: ${total:,}"
        ws_url = f"https://wa.me/5491112345678?text={ws_msg}" # Cambiá por tu cel real
        
        st.markdown(f"""
            <a href="{ws_url}" target="_blank" style="text-decoration: none;">
                <button style="width: 100%; border-radius: 50px; background-color: #25d366; color: white; border: none; padding: 15px; font-weight: bold; cursor: pointer;">
                    Finalizar por WhatsApp 💬
                </button>
            </a>
        """, unsafe_allow_html=True)
        
        if st.button("Limpiar carrito"):
            st.session_state.carrito = []
            st.rerun()