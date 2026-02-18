import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import requests
from bs4 import BeautifulSoup
import urllib.parse

# 1. CONFIGURACIÓN DE PÁGINA (Debe ser lo primero)
st.set_page_config(page_title="Monú | Boutique", layout="wide")

# 2. CSS PROFESIONAL B&W (Fuerza fondo gris claro y letras negras)
def inject_custom_css():
    st.markdown("""
    <style>
        :root { --background-color: #F0F2F6; --text-color: #000000; }
        .stApp { background-color: #F0F2F6 !important; }
        h1, h2, h3, h4, p, span, div, label { color: #000000 !important; font-family: 'Helvetica', sans-serif; }
        
        .product-card {
            background-color: #FFFFFF;
            border: 2px solid #000000;
            padding: 20px;
            margin-bottom: 20px;
            text-align: center;
            border-radius: 0px;
        }
        .product-img {
            filter: grayscale(100%);
            max-width: 100%;
            height: auto;
            margin-bottom: 15px;
        }
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

# 3. MOTOR DE SCRAPING (Extrae info de la URL)
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

# 4. LÓGICA DE CONEXIÓN AL SHEET (Plan A y Plan B)
def load_data():
    try:
        # Intentar conectar usando Secrets
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read()
    except Exception:
        try:
            # Plan B: Si falla el conector, leer como CSV público
            sheet_id = "13WPtfzC4qY-Z3nu4kJv6vnVEneI_ikyDtUBuNzl83Fc"
            url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
            df = pd.read_csv(url)
        except:
            return pd.DataFrame()
            
    # Limpieza de nombres de columnas
    df.columns = [str(c).lower().strip() for c in df.columns]
    return df.dropna(subset=['url']) if 'url' in df.columns else pd.DataFrame()

# 5. UI PRINCIPAL
if 'cart' not in st.session_state:
    st.session_state['cart'] = []

def main():
    inject_custom_css()
    st.markdown("<h1 style='text-align:center;'>M O N Ú</h1>", unsafe_allow_html=True)
    
    df = load_data()
    
    if df.empty:
        st.error("No se pudo conectar con el Google Sheet. Revisa los Secrets y que el Sheet sea Público.")
        return

    # Sidebar: Carrito
    with st.sidebar:
        st.title("🛒 PEDIDO")
        if not st.session_state['cart']:
            st.write("Carrito vacío")
        else:
            for item in st.session_state['cart']:
                st.write(f"▪️ {item['name']} ({item['price']})")
            
            items_txt = "\n".join([f"- {i['name']} ({i['price']})" for i in st.session_state['cart']])
            wa_url = f"https://wa.me/5491122334455?text={urllib.parse.quote('Pedido Monú:\n'+items_txt)}"
            st.link_button("ENVIAR A WHATSAPP", wa_url)
            if st.button("Vaciar"):
                st.session_state['cart'] = []
                st.rerun()

    # Catálogo
    cols = st.columns(3)
    for idx, row in df.iterrows():
        product = get_product_details(row['url'])
        if product:
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="product-card">
                    <img src="{product['img']}" class="product-img">
                    <h4>{product['name']}</h4>
                    <p><b>{product['price']}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("AÑADIR", key=f"btn_{idx}"):
                    st.session_state['cart'].append(product)
                    st.toast("Añadido")
                    st.rerun()

if __name__ == "__main__":
    main()