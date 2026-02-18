import streamlit as st
from streamlit_gsheets import GSheetsConnection

# --- CONEXIÓN AL SHEET (Mantenemos tu URL) ---
url = "https://docs.google.com/spreadsheets/d/13WPtfzC4qY-Z3nu4kJv6vnVEneI_ikyDtUBuNzl83Fc/edit?usp=sharing"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Leemos el sheet. Debe tener columnas: id, nombre, precio, img
    df = conn.read(spreadsheet=url)
    # Convertimos el DataFrame a la lista de diccionarios que usa tu código
    PRODUCTOS = df.to_dict('records')
except Exception:
    # Fallback por si el sheet está vacío o desconectado
    PRODUCTOS = []

# --- GRID INTELIGENTE (Tu código original) ---
# Usamos un contenedor para el grid
st.markdown('<div class="main-container">', unsafe_allow_html=True)

cols = st.columns(2) # Mantenemos tus 2 columnas fijas para estética Monú

for i, p in enumerate(PRODUCTOS):
    with cols[i % 2]:
        # Renderizado de tarjeta exactamente como pediste
        st.markdown(f"""
            <div class="card">
                <img src="{p['img']}" style="width:100%; height:auto; aspect-ratio:1/1; object-fit:cover;">
                <h3 style="margin: 10px 0; font-size: 1.1rem;">{p['nombre']}</h3>
                <h2 style="margin-bottom:15px; font-size: 1.4rem;">${int(p['precio']):,}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Lógica de botón que ya funciona con tu carrito
        if st.button(f"AGREGAR", key=f"add_{p['id']}"):
            if 'cart' not in st.session_state:
                st.session_state.cart = []
            st.session_state.cart.append(p)
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER (Tu código original) ---
st.markdown(f"""
    <div style="background: white; padding: 40px 20px; text-align: center; border-top: 1px solid #000;">
        <h2 class="cinzel" style="font-size: 1.2rem;">MONÚ</h2>
        <div style="display: flex; justify-content: center; gap: 20px; margin-top: 20px;">
            <a href="#" style="text-decoration: none; font-size: 0.8rem; font-weight: 700;">IG</a>
            <a href="#" style="text-decoration: none; font-size: 0.8rem; font-weight: 700;">WA</a>
        </div>
    </div>
    """, unsafe_allow_html=True)