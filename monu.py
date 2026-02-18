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

# --- ESTILO QUIRÚRGICO AESTHETIC REFINADO ---
fondo_style = ""
if logo_bg_base64:
    fondo_style = f"""
    background-image: url("data:image/png;base64,{logo_bg_base64}");
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center;
    background-size: 30%;
    """

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;400;600&display=swap');

    /* Fondo y Blur */
    .stApp {{
        background-color: #FFFFFF;
        {fondo_style}
    }}
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(15px);
        z-index: -1;
    }}

    /* HEADER FIJO MEJORADO */
    .fixed-header {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 90px;
        background-color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 5%;
        border-bottom: 1px solid #F2E8DF;
        box-shadow: 0 2px 15px rgba(0,0,0,0.03);
        z-index: 999999;
    }}
    
    .header-logo-img {{
        max-height: 65px; /* Más grande como pediste */
        width: auto;
    }}

    .nav-buttons {{
        display: flex;
        gap: 20px;
    }}

    .nav-link {{
        text-decoration: none;
        color: #5D3A32;
        font-family: 'Cinzel', serif;
        font-size: 0.9rem;
        letter-spacing: 2px;
        font-weight: 700;
        cursor: pointer;
        padding: 10px 15px;
        border-radius: 5px;
        transition: 0.3s;
    }}
    .nav-link:hover {{
        color: #A66355;
        background-color: #FDF8F5;
    }}

    /* Margen para el contenido */
    .main-content {{
        margin-top: 120px;
    }}

    /* Cards de Producto */
    .product-card {{
        background: white;
        padding: 20px;
        border-radius: 0px; /* Estética más minimalista/editorial */
        border: 1px solid #F8F1EB;
        text-align: center;
        margin-bottom: 25px;
        transition: 0.4s;
    }}
    .product-card:hover {{
        border: 1px solid #A66355;
    }}

    /* Botón Boutique */
    .stButton>button {{
        width: 100%;
        border-radius: 0px;
        background-color: #5D3A32;
        color: white;
        border: none;
        padding: 12px;
        font-family: 'Inter', sans-serif;
        font-weight: 300;
        letter-spacing: 2px;
        font-size: 0.8rem;
    }}
    .stButton>button:hover {{
        background-color: #A66355;
        color: white;
    }}

    /* Ocultar elementos de Streamlit */
    #MainMenu {{visibility: hidden;}}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .block-container {{padding-top: 0rem;}}
    </style>
    """, unsafe_allow_html=True)

# --- RENDER DEL HEADER FIJO ---
logo_html = f'<img src="data:image/png;base64,{logo_header_base64}" class="header-logo-img">' if logo_header_base64 else '<h2 style="font-family:Cinzel; margin:0;">MONÚ</h2>'

st.markdown(f"""
    <div class="fixed-header">
        <div>
            {logo_html}
        </div>
        <div class="nav-buttons">
            <a class="nav-link" href="#catálogo">CATÁLOGO</a>
            <span class="nav-link" onclick="window.parent.document.querySelector('.st-emotion-cache-1gh6602').click()">CARRITO</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Espaciador para el contenido principal
st.markdown('<div class="main-content" id="catálogo"></div>', unsafe_allow_html=True)

# --- CUERPO DE LA TIENDA ---
st.markdown("<h2 style='text-align: center; font-family: Cinzel; letter-spacing: 6px; color: #5D3A32;'>NUESTRA COLECCIÓN</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #D4A373; font-style: italic; margin-bottom: 50px;'>Curaduría Astral & Estilo de Vida</p>", unsafe_allow_html=True)

# Inventario
productos = [
    {"id": 1, "nombre": "Bala Labial 10 Vel.", "precio": 19999, "img": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=500"},
    {"id": 2, "nombre": "Conjunto Puntilla Soft", "precio": 14000, "img": "https://images.unsplash.com/photo-1541310588484-ad456b40e94f?w=500"},
    {"id": 3, "nombre": "Lubricante Anal LUBE", "precio": 11000, "img": "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=500"},
    {"id": 4, "nombre": "Body Splash SEXITIVE", "precio": 11000, "img": "https://images.unsplash.com/photo-1594035910387-fea47794261f?w=500"}
]

if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# Grid
cols = st.columns(2)
for i, prod in enumerate(productos):
    with cols[i % 2]:
        st.markdown(f"""
            <div class="product-card">
                <img src="{prod['img']}" style="width:100%; height:250px; object-fit:cover; margin-bottom:15px;">
                <h4 style="font-family: 'Cinzel'; color: #5D3A32; letter-spacing: 1px;">{prod['nombre']}</h4>
                <p style="color: #A66355; font-weight: 400; font-size: 1.2rem;">${prod['precio']:,}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"AGREGAR AL PEDIDO", key=f"prod_{prod['id']}"):
            st.session_state.carrito.append(prod)
            st.toast(f"Añadido ✨")

# --- SIDEBAR (EL CARRITO) ---
with st.sidebar:
    st.markdown("<h2 style='font-family: Cinzel; color: #5D3A32;'>Tu Selección</h2>", unsafe_allow_html=True)
    if not st.session_state.carrito:
        st.write("Tu pedido está vacío.")
    else:
        total = sum(item['precio'] for item in st.session_state.carrito)
        resumen = ""
        for item in st.session_state.carrito:
            st.write(f"🏷️ **{item['nombre']}** - ${item['precio']:,}")
            resumen += f"- {item['nombre']} (${item['precio']:,})%0A"
        
        st.divider()
        st.markdown(f"### Total: ${total:,}")
        
        ws_msg = f"Hola Monú! ✨%0A{resumen}%0ATotal: ${total:,}"
        ws_url = f"https://wa.me/5491112345678?text={ws_msg}" 
        
        st.markdown(f"""
            <a href="{ws_url}" target="_blank" style="text-decoration: none;">
                <button style="width: 100%; border-radius: 0px; background-color: #25d366; color: white; border: none; padding: 15px; font-weight: bold; cursor: pointer; letter-spacing: 1px;">
                    CONSULTAR POR WHATSAPP 💬
                </button>
            </a>
        """, unsafe_allow_html=True)
        
        if st.button("VACIAR"):
            st.session_state.carrito = []
            st.rerun()