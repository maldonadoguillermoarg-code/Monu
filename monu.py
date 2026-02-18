import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib.parse

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="MONÚ | Boutique", layout="wide")

# 2. CSS AESTHETIC MINIMALISTA (El alma del diseño)
def inject_custom_css():
    st.markdown("""
    <style>
        /* Importar fuente moderna */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');

        :root {
            --bg-color: #F8F9FA;
            --card-bg: #FFFFFF;
            --accent-color: #000000;
            --text-main: #1A1A1A;
            --text-muted: #666666;
        }

        .stApp {
            background-color: var(--bg-color) !important;
        }

        * {
            font-family: 'Inter', sans-serif !important;
            color: var(--text-main) !important;
        }

        /* Título Principal Aesthetic */
        .main-title {
            font-weight: 700;
            letter-spacing: 12px;
            text-align: center;
            margin-top: 50px;
            margin-bottom: 10px;
            text-transform: uppercase;
            font-size: 2.5rem;
        }

        .sub-title {
            text-align: center;
            letter-spacing: 4px;
            color: var(--text-muted) !important;
            font-size: 0.8rem;
            margin-bottom: 50px;
            text-transform: uppercase;
        }

        /* Tarjeta de Producto Moderno */
        .product-card {
            background-color: var(--card-bg);
            border: 1px solid #EAEAEA;
            padding: 0px;
            margin-bottom: 25px;
            transition: all 0.4s ease-in-out;
            border-radius: 4px;
            overflow: hidden;
        }

        .product-card:hover {
            border-color: #000000;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            transform: translateY(-5px);
        }

        .product-img-container {
            width: 100%;
            height: 350px;
            overflow: hidden;
            background-color: #F2F2F2;
        }

        .product-img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            filter: grayscale(100%);
            transition: 0.6s ease;
        }

        .product-card:hover .product-img {
            filter: grayscale(0%);
            transform: scale(1.05);
        }

        .product-info {
            padding: 20px;
            text-align: center;
        }

        .product-name {
            font-size: 0.9rem;
            font-weight: 400;
            letter-spacing: 1px;
            margin-bottom: 8px;
            text-transform: uppercase;
        }

        .product-price {
            font-size: 1.1rem;
            font-weight: 700;
            color: #000000 !important;
        }

        /* Botones Estilizados */
        div.stButton > button {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            border: 1px solid #000000 !important;
            border-radius: 0px !important;
            width: 100%;
            height: 45px;
            font-size: 0.7rem !important;
            letter-spacing: 2px;
            text-transform: uppercase;
            transition: 0.3s;
        }

        div.stButton > button:hover {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }

        /* Sidebar Minimalista */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #EAEAEA;
        }

        /* Ocultar elementos de Streamlit */
        #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. MOTOR DE SCRAPING (Optimizado)
@st.cache_data(ttl=3600)
def get_product_details(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        name = soup.find("meta", property="og:title")
        name = name["content"].split(" - ")[0] if name else "L'Art de Monú"
        
        img = soup.find("meta", property="og:image")
        img_url = img["content"] if img else "https://via.placeholder.com/600x800"
        
        price_meta = soup.find("meta", property="product:price:amount")
        if price_meta:
            price = f"${price_meta['content']}"
        else:
            price_tag = soup.select_one(".woocommerce-Price-amount bdi, .price")
            price = price_tag.get_text() if price_tag else "Consultar"
            
        return {"name": name, "img": img_url, "price": price, "url": url}
    except:
        return None

# 4. CARGA DE DATOS (Directo desde Publicación Web)
def load_data():
    try:
        sheet_id = "13WPtfzC4qY-Z3nu4kJv6vnVEneI_ikyDtUBuNzl83Fc"
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        df = pd.read_csv(csv_url)
        df.columns = [str(c).lower().strip() for c in df.columns]
        return df.dropna(subset=['url'])
    except:
        return pd.DataFrame()

# 5. UI PRINCIPAL
if 'cart' not in st.session_state:
    st.session_state['cart'] = []

def main():
    inject_custom_css()
    
    # Header Aesthetic
    st.markdown('<div class="main-title">M O N Ú</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Selection Mondiale & Boutique</div>', unsafe_allow_html=True)
    
    df = load_data()
    
    if df.empty:
        st.info("Configurando el catálogo...")
        return

    # SIDEBAR: Carrito Minimal
    with st.sidebar:
        st.markdown("<br><br><h2 style='letter-spacing:2px; font-size:1.2rem;'>SELECCIÓN</h2>", unsafe_allow_html=True)
        if not st.session_state['cart']:
            st.markdown("<p style='font-size:0.8rem; color:#999 !important;'>Tu bolsa está vacía.</p>", unsafe_allow_html=True)
        else:
            total_items = 0
            for i, item in enumerate(st.session_state['cart']):
                st.markdown(f"<p style='font-size:0.8rem; margin-bottom:2px;'>{item['name']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:0.7rem; font-weight:700;'>{item['price']}</p>", unsafe_allow_html=True)
                st.divider()
            
            # WhatsApp Checkout
            msg = "Hola Monú! Quisiera consultar por este pedido:\n" + "\n".join([f"- {i['name']} ({i['price']})" for i in st.session_state['cart']])
            st.link_button("FINALIZAR PEDIDO", f"https://wa.me/5491122334455?text={urllib.parse.quote(msg)}")
            
            if st.button("VACIAR BOLSA"):
                st.session_state['cart'] = []
                st.rerun()

    # CATÁLOGO: Grill de productos
    cols = st.columns(3)
    for idx, row in df.iterrows():
        product = get_product_details(row['url'])
        if product:
            with cols[idx % 3]:
                # Estructura de tarjeta con HTML personalizado
                st.markdown(f"""
                <div class="product-card">
                    <div class="product-img-container">
                        <img src="{product['img']}" class="product-img">
                    </div>
                    <div class="product-info">
                        <div class="product-name">{product['name']}</div>
                        <div class="product-price">{product['price']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Botones de Acción
                b_col1, b_col2 = st.columns(2)
                with b_col1:
                    st.link_button("DETALLES", product['url'])
                with b_col2:
                    if st.button("AÑADIR", key=f"btn_{idx}"):
                        st.session_state['cart'].append(product)
                        st.toast(f"Agregado: {product['name']}")
                        st.rerun()

if __name__ == "__main__":
    main()