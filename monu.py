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

# --- ESTILO QUIRÚRGICO DE ALTO NIVEL ---
fondo_style = ""
if logo_bg_base64:
    # Bajamos la opacidad del logo de fondo al 5% para que sea ultra sutil (Aesthetic)
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

    /* Tipografía Negra Total por directiva */
    html, body, [class*="st-"], div, p, h1, h2, h3, h4 {{
        color: #000000 !important;
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background-color: #FFFFFF;
    }}

    .bg-watermark {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        {fondo_style}
        z-index: -1;
    }}

    /* HEADER FIJO MEJORADO */
    .fixed-header {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 110px;
        background-color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 5%;
        border-bottom: 2px solid #F2E8DF;
        z-index: 999999;
    }}
    
    .header-logo-img {{
        max-height: 85px; /* Agrandado para matchear con botones */
        width: auto;
    }}

    .nav-buttons {{
        display: flex;
        gap: 30px;
    }}

    .nav-link {{
        text-decoration: none;
        color: #000000 !important;
        font-family: 'Cinzel', serif;
        font-size: 1.1rem;
        letter-spacing: 2px;
        font-weight: 700;
        cursor: pointer;
    }}

    /* Margen para el contenido principal */
    .main-content {{
        margin-top: 140px;
        padding: 0 5%;
    }}

    /* Cards de Producto */
    .product-card {{
        background: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 0px;
        border: 1px solid #F2E8DF;
        text-align: center;
        margin-bottom: 25px;
        transition: 0.4s;
    }}
    .product-card:hover {{
        border: 1px solid #A66355;
    }}

    /* Botones Monú (Fondo marca, Letra negra) */
    .stButton>button {{
        width: 100%;
        border-radius: 0px;
        background-color: #A66355 !important;
        color: #000000 !important;
        border: none;
        padding: 12px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        letter-spacing: 2px;
        font-size: 0.9rem;
    }}
    .stButton>button:hover {{
        background-color: #D4A373 !important;
        color: #000000 !important;
    }}

    /* Ocultar elementos de Streamlit */
    header, footer {{visibility: hidden;}}
    .block-container {{padding-top: 0rem;}}
    </style>
    <div class="bg-watermark"></div>
    """, unsafe_allow_html=True)

# --- CARRITO (Manejo de estado infalible) ---
if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# --- RENDER DEL HEADER FIJO ---
logo_html = f'<img src="data:image/png;base64,{logo_header_base64}" class="header-logo-img">' if logo_header_base64 else '<h1 style="font-family:Cinzel; margin:0;">MONÚ</h1>'

st.markdown(f"""
    <div class="fixed-header">
        <div>{logo_html}</div>
        <div class="nav-buttons">
            <a class="nav-link" href="#catalogo">CATÁLOGO</a>
            <span class="nav-link">CARRITO ({len(st.session_state.carrito)})</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Espaciador
st.markdown('<div class="main-content" id="catalogo"></div>', unsafe_allow_html=True)

# --- CUERPO DE LA TIENDA ---
st.markdown("<h2 style='text-align: center; font-family: Cinzel; letter-spacing: 8px; color: #000000;'>COLECCIÓN MONÚ</h2>", unsafe_allow_html=True)
st.divider()

# Inventario (Aseguramos que todos tengan la clave 'sku' para evitar el KeyError)
productos = [
    {"id": 1, "nombre": "Bala Labial 10 Vel.", "precio": 19999, "img": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=500", "sku": "EMI-B10"},
    {"id": 2, "nombre": "Conjunto Puntilla Soft", "precio": 14000, "img": "https://images.unsplash.com/photo-1541310588484-ad456b40e94f?w=500", "sku": "EMI-CP1"},
    {"id": 3, "nombre": "Lubricante Anal LUBE", "precio": 11000, "img": "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=500", "sku": "EMI-LUB"},
    {"id": 4, "nombre": "Body Splash SEXITIVE", "precio": 11000, "img": "https://images.unsplash.com/photo-1594035910387-fea47794261f?w=500", "sku": "EMI-BS1"}
]

# Grid de productos
cols = st.columns(2)
for i, prod in enumerate(productos):
    with cols[i % 2]:
        st.markdown(f"""
            <div class="product-card">
                <img src="{prod['img']}" style="width:100%; height:280px; object-fit:cover; margin-bottom:15px;">
                <h4 style="font-family: 'Cinzel'; color: #000000; letter-spacing: 1px;">{prod['nombre']}</h4>
                <p style="color: #000000; font-weight: 700; font-size: 1.3rem;">${prod['precio']:,}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Botón con lógica de actualización
        if st.button(f"LO QUIERO", key=f"btn_{prod['id']}"):
            st.session_state.carrito.append(prod)
            st.rerun()

# --- SIDEBAR (EL CARRITO) ---
with st.sidebar:
    st.markdown("<h2 style='font-family: Cinzel; color: #000000;'>Mi Selección</h2>", unsafe_allow_html=True)
    if not st.session_state.carrito:
        st.write("Tu pedido está vacío.")
    else:
        total = 0
        resumen = ""
        for item in st.session_state.carrito:
            # Validación de clave SKU para evitar errores en sesiones viejas
            sku_item = item.get('sku', 'N/A')
            st.write(f"✨ **{item['nombre']}**")
            st.write(f"Ref: {sku_item} | ${item['precio']:,}")
            total += item['precio']
            resumen += f"- {item['nombre']} ({sku_item}): ${item['precio']:,}%0A"
        
        st.divider()
        st.markdown(f"### Total: ${total:,}")
        
        # WhatsApp Final
        ws_msg = f"Hola Monú! ✨%0A{resumen}%0ATotal: ${total:,}"
        ws_url = f"https://wa.me/5491112345678?text={ws_msg}" 
        
        st.markdown(f"""
            <a href="{ws_url}" target="_blank" style="text-decoration: none;">
                <button style="width: 100%; border-radius: 0px; background-color: #25d366 !important; color: #000000 !important; border: none; padding: 15px; font-weight: bold; cursor: pointer; letter-spacing: 1px;">
                    CONSULTAR POR WHATSAPP 💬
                </button>
            </a>
        """, unsafe_allow_html=True)
        
        if st.button("VACIAR CARRITO"):
            st.session_state.carrito = []
            st.rerun()