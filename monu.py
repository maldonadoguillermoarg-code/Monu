import streamlit as st

# Configuración de la página (El toque Pro)
st.set_page_config(
    page_title="Monu | Selección Global & Local",
    page_icon="🛍️",
    layout="wide"
)

# Estilo quirúrgico con CSS inyectado para mejorar la estética
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #1e293b;
        color: white;
        border: none;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #3b82f6;
        color: white;
    }
    .product-card {
        padding: 20px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER DE MARKETING (Empatía con el público Argento) ---
st.title("MONU.")
st.subheader("Lo mejor del mundo y lo nuestro, en un solo lugar. 🇦🇷")
st.write("Envíos a todo el país | Cuotas sin interés con Mercado Pago")

# --- BASE DE DATOS DE PRODUCTOS (Híbrido Dropi/Propio) ---
# En un futuro esto lo podés leer de un CSV o JSON
productos = [
    {"id": 1, "nombre": "Reloj Inteligente V2", "precio": 35000, "tag": "Dropi", "img": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500"},
    {"id": 2, "nombre": "Remera Monu Oversize", "precio": 15000, "tag": "Propio", "img": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500"},
    {"id": 3, "nombre": "Auriculares Noise Cancelling", "precio": 55000, "tag": "Dropi", "img": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500"},
    {"id": 4, "nombre": "Gorra Trucker Monu", "precio": 8000, "tag": "Propio", "img": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=500"}
]

# --- CARRITO (Manejo de estado) ---
if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# --- GRID DE PRODUCTOS ---
cols = st.columns(2) # Dos columnas para que se vea bien en celular

for i, prod in enumerate(productos):
    with cols[i % 2]:
        st.markdown(f"""
            <div class="product-card">
                <img src="{prod['img']}" style="width:100%; border-radius:10px;">
                <p style="font-size: 0.8rem; color: #3b82f6; font-weight: bold; margin-top:10px;">{prod['tag'].upper()}</p>
                <h3 style="margin: 0;">{prod['nombre']}</h3>
                <p style="font-size: 1.2rem; font-weight: bold;">${prod['precio']:,}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"Agregar al carrito", key=f"btn_{prod['id']}"):
            st.session_state.carrito.append(prod)
            st.toast(f"¡{prod['nombre']} agregado!")

# --- BARRA LATERAL / CHECKOUT ---
with st.sidebar:
    st.header("Tu Pedido 🛒")
    if not st.session_state.carrito:
        st.write("El carrito está vacío.")
    else:
        total = 0
        resumen = ""
        for item in st.session_state.carrito:
            st.write(f"• {item['nombre']} - ${item['precio']:,}")
            total += item['precio']
            resumen += f"- {item['nombre']} (%24{item['precio']:,})%0A"
        
        st.divider()
        st.write(f"### Total: ${total:,}")
        
        # Botón de cierre: Envío a WhatsApp (La que va en Argentina)
        numero_tel = "5491112345678" # TU NÚMERO ACÁ
        msg = f"Hola Monu! Quiero comprar:%0A{resumen}%0ATotal: ${total:,}"
        ws_link = f"https://wa.me/{numero_tel}?text={msg}"
        
        st.markdown(f"""
            <a href="{ws_link}" target="_blank">
                <button style="width: 100%; border-radius: 20px; background-color: #25d366; color: white; border: none; padding: 15px; font-weight: bold; cursor: pointer;">
                    Finalizar por WhatsApp 💬
                </button>
            </a>
        """, unsafe_allow_html=True)
        
        if st.button("Vaciar carrito"):
            st.session_state.carrito = []
            st.rerun()
            