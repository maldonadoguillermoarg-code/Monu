import streamlit as st
import base64

# Configuración de la página
st.set_page_config(
    page_title="Monú | Esencia Astral",
    page_icon="✨",
    layout="wide"
)

# --- LÓGICA DE SUPER SENIOR PARA CARGAR IMÁGENES LOCALES ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Intentamos cargar el logo de fondo para el CSS
try:
    bin_str = get_base64_of_bin_file('MonumarcaLogoNegro.png')
    fondo_css = f"background-image: url('data:image/png;base64,{bin_str}');"
except:
    fondo_css = "" # Fallback si el archivo no está

# --- ESTILO QUIRÚRGICO: IDENTIDAD VISUAL MONÚ ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;400;600&display=swap');

    /* Fondo con MonumarcaLogoNegro.png borroso */
    .main {{
        background-color: #FFFDFB;
        {fondo_css}
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        background-size: 50%;
    }}
    
    .main::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(255, 253, 251, 0.85); /* Capa de claridad */
        backdrop-filter: blur(12px); /* Efecto borroso pedido */
        z-index: -1;
    }}

    /* Banner Superior con LogoHorizontal.png */
    .banner-container {{
        background: linear-gradient(135deg, #4A2C2A 0%, #5D3A32 100%);
        padding: 30px;
        border-radius: 0 0 40px 40px;
        text-align: center;
        margin: -60px -50px 40px -50px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }}
    .logo-horizontal {{
        max-width: 300px;
        height: auto;
    }}

    /* Cards de Producto con Glassmorphism */
    .product-card {{
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(5px);
        padding: 25px;
        border-radius: 25px;
        border: 1px solid rgba(242, 232, 223, 0.8);
        text-align: center;
        margin-bottom: 25px;
        transition: all 0.3s ease;
    }}
    .product-card:hover {{
        transform: translateY(-8px);
        border: 1px solid #A66355;
        box-shadow: 0 20px 40px rgba(166, 99, 85, 0.1);
    }}

    /* Botones Monú */
    .stButton>button {{
        width: 100%;
        border-radius: 50px;
        background: #A66355;
        color: white;
        border: none;
        padding: 12px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        letter-spacing: 1px;
    }}
    .stButton>button:hover {{
        background: #5D3A32;
        color: #D4A373;
    }}

    [data-testid="stSidebar"] {{
        background-color: #FDF8F5;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- RENDER DEL BANNER CON LOGOHORIZONTAL.PNG ---
st.markdown(f"""
    <div class="banner-container">
        <img src="app/static/LogoHorizontal.png" class="logo-horizontal" onerror="this.src='https://via.placeholder.com/300x100?text=Logo+Horizontal'">
    </div>
    """, unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #A66355; font-style: italic; letter-spacing: 3px; margin-top: 10px;'>CURADURÍA ASTRAL & GLOBAL</p>", unsafe_allow_html=True)
st.divider()

# --- BASE DE DATOS DE PRODUCTOS ---
productos = [
    {"id": 1, "nombre": "Reloj Inteligente V2", "precio": 35000, "tag": "Dropi", "img": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500"},
    {"id": 2, "nombre": "Remera Monu Oversize", "precio": 15000, "tag": "Propio", "img": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500"},
    {"id": 3, "nombre": "Auriculares Noise Cancelling", "precio": 55000, "tag": "Dropi", "img": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500"},
    {"id": 4, "nombre": "Gorra Trucker Monu", "precio": 8000, "tag": "Propio", "img": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=500"}
]

if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# --- GRID DE PRODUCTOS ---
cols = st.columns(2)

for i, prod in enumerate(productos):
    with cols[i % 2]:
        st.markdown(f"""
            <div class="product-card">
                <img src="{prod['img']}" style="width:100%; border-radius:15px; height: 200px; object-fit: cover;">
                <p style="font-size: 0.7rem; color: #A66355; font-weight: bold; margin-top:15px; letter-spacing: 1.5px;">{prod['tag'].upper()}</p>
                <h3 style="margin: 5px 0; font-size: 1.3rem; font-family: 'Cinzel', serif;">{prod['nombre']}</h3>
                <p style="font-size: 1.2rem; font-weight: bold; color: #4A2C2A;">${prod['precio']:,}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"Lo quiero", key=f"btn_{prod['id']}"):
            st.session_state.carrito.append(prod)
            st.toast(f"¡{prod['nombre']} agregado!")

# --- SIDEBAR / CHECKOUT ---
with st.sidebar:
    st.markdown("<h2 style='text-align: left; font-family: Cinzel, serif;'>Tu Selección ✨</h2>", unsafe_allow_html=True)
    if not st.session_state.carrito:
        st.write("Tu carrito está esperando.")
    else:
        total = 0
        resumen = ""
        for item in st.session_state.carrito:
            st.write(f"• **{item['nombre']}** - ${item['precio']:,}")
            total += item['precio']
            resumen += f"- {item['nombre']} (%24{item['precio']:,})%0A"
        
        st.divider()
        st.write(f"### Total: ${total:,}")
        
        numero_tel = "5491112345678" # TU WHATSAPP
        msg = f"Hola Monú! ✨ Quiero este pedido:%0A{resumen}%0ATotal: ${total:,}"
        ws_link = f"https://wa.me/{numero_tel}?text={msg}"
        
        st.markdown(f"""
            <a href="{ws_link}" target="_blank" style="text-decoration: none;">
                <button style="width: 100%; border-radius: 50px; background-color: #25d366; color: white; border: none; padding: 15px; font-weight: bold; cursor: pointer;">
                    Finalizar por WhatsApp 💬
                </button>
            </a>
        """, unsafe_allow_html=True)
        
        if st.button("Vaciar carrito"):
            st.session_state.carrito = []
            st.rerun()