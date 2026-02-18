import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import urllib.parse

# 1. CONFIGURACIÓN DE PÁGINA (Debe ser lo primero)
st.set_page_config(
    page_title="Monú | Boutique Astral & Global",
    page_icon="🎬",
    layout="wide"
)

# 2. INYECCIÓN DE CSS "BLINDADO" (Anula Modo Oscuro)
def inject_custom_css():
    st.markdown("""
    <style>
        /* Reescritura de variables internas de Streamlit */
        :root {
            --primary-color: #000000;
            --background-color: #F0F2F6;
            --secondary-background-color: #FFFFFF;
            --text-color: #000000;
        }

        /* Forzar fondo y texto en todos los contenedores principales */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #F0F2F6 !important;
            color: #000000 !important;
        }

        /* Forzar color negro a TODO el texto */
        h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown, small {
            color: #000000 !important;
        }

        /* Sidebar con estilo minimalista */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #000000;
        }

        /* Cards de producto: Fondo blanco y borde negro */
        div[data-testid="stVerticalBlock"] > div > div > div.stVerticalBlock {
            background-color: #FFFFFF !important;
            border: 2px solid #000000 !important;
            padding: 20px !important;
            border-radius: 0px !important;
            margin-bottom: 10px;
        }

        /* Botones estilo B&W */
        div.stButton > button {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            border-radius: 0px !important;
            border: none !important;
            width: 100%;
            font-weight: bold;
            transition: 0.3s;
        }

        div.stButton > button:hover {
            background-color: #444444 !important;
            box-shadow: 4px 4px 0px #000000;
        }

        /* Ajuste de imágenes para que no se vean raras con el fondo */
        img {
            border-radius: 0px;
            margin-bottom: 10px;
        }

        /* Ocultar elementos innecesarios de Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE DATOS
@st.cache_data(ttl=300)
def load_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read()
        return df.dropna(subset=['id', 'nombre', 'precio'])
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return pd.DataFrame()

# 4. GESTIÓN DE ESTADO (CARRITO)
if 'cart' not in st.session_state:
    st.session_state['cart'] = {}

def add_to_cart(prod_id, prod_name, prod_price):
    if prod_id in st.session_state['cart']:
        st.session_state['cart'][prod_id]['qty'] += 1
    else:
        st.session_state['cart'][prod_id] = {'name': prod_name, 'price': prod_price, 'qty': 1}
    st.toast(f"✅ Añadido: {prod_name}")

# 5. UI PRINCIPAL
def main():
    inject_custom_css()
    
    # Logo Superior
    st.markdown('<div style="text-align:center;"><img src="https://via.placeholder.com/300x120?text=MONU+BOUTIQUE" width="300"></div>', unsafe_allow_html=True)
    
    df = load_data()
    
    # Sidebar: Resumen de Compra
    with st.sidebar:
        st.title("TU PEDIDO")
        if not st.session_state['cart']:
            st.write("No hay productos.")
        else:
            total = 0
            for pid, item in list(st.session_state['cart'].items()):
                sub = item['price'] * item['qty']
                total += sub
                st.write(f"**{item['name']}**")
                st.caption(f"{item['qty']} x ${item['price']:,.2f} = ${sub:,.2f}")
            
            st.divider()
            st.subheader(f"Total: ${total:,.2f}")
            
            if st.button("FINALIZAR PEDIDO (WA)"):
                msg = f"Hola! Quisiera realizar este pedido:\n"
                for pid, item in st.session_state['cart'].items():
                    msg += f"- {item['name']} x{item['qty']}\n"
                msg += f"\nTotal: ${total:,.2f}"
                wa_url = f"https://wa.me/5491122334455?text={urllib.parse.quote(msg)}"
                st.link_button("Ir a WhatsApp 📱", wa_url)

            if st.button("Vaciar Carrito"):
                st.session_state['cart'] = {}
                st.rerun()

    # Catálogo
    if not df.empty:
        st.markdown("### ✦ CATÁLOGO")
        cols = st.columns(3)
        for idx, row in df.iterrows():
            with cols[idx % 3]:
                with st.container():
                    st.image(row['imagen_url'], width='stretch')
                    st.markdown(f"**{row['nombre']}**")
                    st.markdown(f"**${row['precio']:,.2f}**")
                    
                    st.link_button("DETALLES", row['info_url'])
                    if st.button("AÑADIR", key=f"add_{row['id']}"):
                        add_to_cart(row['id'], row['nombre'], row['precio'])
                        st.rerun()
    else:
        st.warning("No se encontraron productos en el Google Sheet.")

if __name__ == "__main__":
    main()