import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib.parse

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Monú | Boutique", layout="wide")

# 2. CSS PROFESIONAL B&W
def inject_custom_css():
    st.markdown("""
    <style>
        :root { --background-color: #F0F2F6; }
        .stApp { background-color: #F0F2F6 !important; }
        * { color: #000000 !important; font-family: 'Helvetica', sans-serif; }
        .product-card {
            background-color: #FFFFFF;
            border: 2px solid #000000;
            padding: 20px;
            margin-bottom: 20px;
            text-align: center;
        }
        .product-img { filter: grayscale(100%); max-width: 100%; height: auto; margin-bottom: 15px; }
        div.stButton > button {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            border-radius: 0px !important;
            width: 100%;
            font-weight: bold;
        }
        [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 2px solid #000000; }
    </style>
    """, unsafe_allow_html=True)

# 3. MOTOR DE SCRAPING
@st.cache_data(ttl=3600)
def get_product_details(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        name = soup.find("meta", property="og:title")
        name = name["content"].split(" - ")[0] if name else "Producto Monú"
        img = soup.find("meta", property="og:image")
        img_url = img["content"] if img else "https://via.placeholder.com/400"
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
        # Tu ID de Sheet que ya está publicado
        sheet_id = "13WPtfzC4qY-Z3nu4kJv6vnVEneI_ikyDtUBuNzl83Fc"
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        df = pd.read_csv(csv_url)
        df.columns = [str(c).lower().strip() for c in df.columns]
        return df.dropna(subset=['url'])
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

# 5. UI
if 'cart' not in st.session_state: st.session_state['cart'] = []

def main():
    inject_custom_css()
    st.markdown("<h1 style='text-align:center;'>M O N Ú</h1>", unsafe_allow_html=True)
    
    df = load_data()
    
    if df.empty:
        st.warning("Aún no hay productos en el Sheet o la columna 'url' no existe.")
        return

    # Sidebar
    with st.sidebar:
        st.title("🛒 CARRITO")
        for item in st.session_state['cart']:
            st.write(f"▪️ {item['name']}")
        if st.session_state['cart']:
            msg = "Hola Monú! Pedido:\n" + "\n".join([f"- {i['name']}" for i in st.session_state['cart']])
            st.link_button("PEDIR POR WHATSAPP", f"https://wa.me/5491122334455?text={urllib.parse.quote(msg)}")
            if st.button("Vaciar"):
                st.session_state['cart'] = []
                st.rerun()

    # Catálogo
    cols = st.columns(3)
    for idx, row in df.iterrows():
        product = get_product_details(row['url'])
        if product:
            with cols[idx % 3]:
                st.markdown(f'<div class="product-card"><img src="{product["img"]}" class="product-img"><h4>{product["name"]}</h4><p>{product["price"]}</p></div>', unsafe_allow_html=True)
                if st.button("AÑADIR", key=f"b_{idx}"):
                    st.session_state['cart'].append(product)
                    st.rerun()

if __name__ == "__main__":
    main()