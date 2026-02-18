import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import urllib.parse

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Minimalist E-commerce B&W",
    page_icon="🛍️",
    layout="wide"
)

# --- INYECCIÓN DE CSS (CUSTOM UI/UX) ---
def inject_custom_css():
    st.markdown(f"""
    <style>
        /* Paleta Monocromática y Tipografía */
        :root {{
            --primary-color: #000000;
            --bg-color: #FFFFFF;
        }}
        
        .main {{
            background-image: url("https://www.transparenttextures.com/patterns/white-diamond.png"); /* Ejemplo de textura sutil */
            background-color: rgba(255, 255, 255, 0.9);
        }}

        /* Forzar texto negro absoluto */
        h1, h2, h3, p, span, div, label {{
            color: #000000 !important;
            font-family: 'Helvetica', sans-serif;
        }}

        /* Logo Large (280px-300px) */
        .logo-container {{
            display: flex;
            justify-content: center;
            padding: 20px;
        }}
        .logo-img {{
            width: 300px;
            filter: grayscale(100%);
        }}

        /* Cards de Producto */
        .product-card {{
            border: 1px solid #000000;
            padding: 15px;
            border-radius: 0px;
            margin-bottom: 20px;
            transition: transform 0.2s ease;
        }}
        .product-card:hover {{
            box-shadow: 5px 5px 0px #000000;
            transform: translateY(-2px);
        }}

        /* Botones Estilo Minimalista */
        .stButton>button {{
            width: 100%;
            border-radius: 0px;
            border: 2px solid #000000;
            background-color: #FFFFFF;
            color: #000000;
            font-weight: bold;
            transition: 0.3s;
        }}
        .stButton>button:hover {{
            background-color: #000000;
            color: #FFFFFF;
            border: 2px solid #000000;
        }}
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE DATOS (GOOGLE SHEETS) ---
@st.cache_data(ttl=600)  # Cache de 10 min para optimizar cuota API
def load_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl="10m")
        # Validamos columnas obligatorias
        required_cols = ['id', 'nombre', 'categoria', 'precio', 'descripcion', 'imagen_url', 'info_url', 'stock']
        for col in required_cols:
            if col not in df.columns:
                st.error(f"Error: La columna '{col}' no existe en el Google Sheet.")
                return pd.DataFrame()
        return df
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return pd.DataFrame()

# --- GESTIÓN DE CARRITO (SESSION STATE) ---
if 'cart' not in st.session_state:
    st.session_state['cart'] = {}

def add_to_cart(product_id: int, product_name: str, price: float):
    if product_id in st.session_state['cart']:
        st.session_state['cart'][product_id]['quantity'] += 1
    else:
        st.session_state['cart'][product_id] = {'name': product_name, 'price': price, 'quantity': 1}
    st.toast(f"✅ {product_name} añadido")

# --- MÓDULO DE CHECKOUT ---
def process_payment():
    """Vía Futura: Portal de Pagos"""
    st.info("🔄 Redirigiendo a plataforma de pago...")

def generate_whatsapp_link(phone_number: str):
    cart = st.session_state['cart']
    if not cart:
        return None
    
    mensaje = "*Nuevo Pedido - B&W Store*\n\n"
    total_general = 0
    for item in cart.values():
        subtotal = item['price'] * item['quantity']
        mensaje += f"• {item['name']} x{item['quantity']} = ${subtotal:,.2f}\n"
        total_general += subtotal
    
    mensaje += f"\n*TOTAL FINAL: ${total_general:,.2f}*"
    encoded_msg = urllib.parse.quote(mensaje)
    return f"https://wa.me/{phone_number}?text={encoded_msg}"

# --- UI PRINCIPAL ---
def main():
    inject_custom_css()
    
    # Header / Logo
    st.markdown('<div class="logo-container"><img src="https://via.placeholder.com/300x100?text=LOGO+B%26W" class="logo-img"></div>', unsafe_allow_html=True)
    
    df = load_data()
    if df.empty:
        st.warning("No hay productos disponibles actualmente.")
        return

    # Sidebar: Filtros y Carrito
    with st.sidebar:
        st.header("FILTROS")
        categoria = st.selectbox("Categoría", ["Todos"] + list(df['categoria'].unique()))
        
        st.divider()
        st.header("TU CARRITO")
        total_cart = 0
        for pid, item in st.session_state['cart'].items():
            st.write(f"**{item['name']}** x{item['quantity']}")
            total_cart += item['price'] * item['quantity']
        
        st.subheader(f"Total: ${total_cart:,.2f}")
        
        if st.button("FINALIZAR COMPRA (WhatsApp)"):
            link = generate_whatsapp_link("5491122334455") # Reemplazar con tu número
            if link:
                st.markdown(f'<a href="{link}" target="_blank" style="text-decoration:none;"><button style="width:100%; cursor:pointer;">Confirmar en WhatsApp 📱</button></a>', unsafe_allow_html=True)
            else:
                st.warning("El carrito está vacío")
        
        if st.button("Pagar con Tarjeta (Beta)"):
            process_payment()

    # Catálogo Dinámico
    st.markdown(f"### Catálogo / {categoria}")
    
    filtered_df = df if categoria == "Todos" else df[df['categoria'] == categoria]
    
    # Grilla de 3 columnas
    cols = st.columns(3)
    for index, row in filtered_df.iterrows():
        with cols[index % 3]:
            st.markdown(f"""
            <div class="product-card">
                <img src="{row['imagen_url']}" style="width:100%; filter:grayscale(100%);">
                <h4>{row['nombre']}</h4>
                <p><strong>${row['precio']:,.2f}</strong></p>
                <p style="font-size: 0.8em;">{row['descripcion'][:80]}...</p>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                st.link_button("Ver Info", row['info_url'])
            with c2:
                if st.button("Añadir", key=f"btn_{row['id']}"):
                    add_to_cart(row['id'], row['nombre'], row['precio'])

if __name__ == "__main__":
    main()