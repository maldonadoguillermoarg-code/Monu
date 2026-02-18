import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib.parse

# 1. CONFIGURACIÓN
st.set_page_config(page_title="MONÚ | Boutique", layout="wide")

# 2. CSS AESTHETIC MODERNO (RECORREGIDO)
def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
        
        :root { --bg: #F0F2F5; --text: #000000; }
        .stApp { background-color: var(--bg) !important; }
        * { font-family: 'Inter', sans-serif !important; }

        /* Títulos */
        .header-container { text-align: center; padding: 60px 0; }
        .main-title { letter-spacing: 15px; font-weight: 700; font-size: 3rem; text-transform: uppercase; margin: 0; color: #000 !important; }
        
        /* Cards */
        .product-card {
            background: #FFF;
            border: 1px solid #000;
            padding: 0;
            transition: 0.3s;
            margin-bottom: 20px;
        }
        .product-img { width: 100%; height: 400px; object-fit: cover; filter: grayscale(100%); transition: 0.5s; }
        .product-card:hover .product-img { filter: grayscale(0%); }
        
        .info-area { padding: 20px; text-align: center; }
        .price-tag { font-weight: 700; font-size: 1.2rem; margin-top: 5px; color: #000 !important; }

        /* BOTONES - CORREGIDOS PARA LEERSE BIEN */
        div.stButton > button {
            background-color: #000000 !important;
            color: #FFFFFF !important; /* TEXTO BLANCO */
            border-radius: 0px !important;
            border: 1px solid #000 !important;
            width: 100%;
            height: 45px;
            font-size: 0.75rem !important;
            letter-spacing: 2px;
            text-transform: uppercase;
            font-weight: 700 !important;
            cursor: pointer;
        }
        
        div.stButton > button:hover {
            background-color: #333333 !important;
            color: #FFFFFF !important;
        }

        /* Modal / Detalles */
        .detail-box { background: white; border: 2px solid black; padding: 30px; margin-top: 20px; }
        
        /* Ocultar basurita de Streamlit */
        #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. SCRAPING AVANZADO (AHORA TRAE DESCRIPCIÓN)
@st.cache_data(ttl=3600)
def get_full_details(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        name = soup.find("meta", property="og:title")
        name = name["content"].split(" - ")[0] if name else "Objeto Monú"
        
        img = soup.find("meta", property="og:image")
        img_url = img["content"] if img else ""
        
        # Extraer descripción (WooCommerce standard)
        desc = soup.find("meta", property="og:description")
        desc_text = desc["content"] if desc else "No hay descripción disponible para este objeto."
        
        price_meta = soup.find("meta", property="product:price:amount")
        price = f"${price_meta['content']}" if price_meta else "Consultar"
            
        return {"name": name, "img": img_url, "price": price, "desc": desc_text, "url": url}
    except:
        return None

# 4. DATA
def load_data():
    try:
        sheet_id = "13WPtfzC4qY-Z3nu4kJv6vnVEneI_ikyDtUBuNzl83Fc"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        df = pd.read_csv(url)
        df.columns = [str(c).lower().strip() for c in df.columns]
        return df.dropna(subset=['url'])
    except:
        return pd.DataFrame()

# 5. UI & LÓGICA
if 'cart' not in st.session_state: st.session_state['cart'] = []
if 'viewing_product' not in st.session_state: st.session_state['viewing_product'] = None

def main():
    inject_custom_css()
    
    # Header
    st.markdown('<div class="header-container"><div class="main-title">M O N Ú</div><p style="letter-spacing:5px; font-size:10px; color:#666;">EST. 2024 — GLOBAL BOUTIQUE</p></div>', unsafe_allow_html=True)
    
    df = load_data()
    
    # --- VISTA DE DETALLES (MODAL INTERNO) ---
    if st.session_state['viewing_product']:
        p = st.session_state['viewing_product']
        col_img, col_info = st.columns([1, 1])
        with col_img:
            st.image(p['img'], use_container_width=True)
        with col_info:
            st.markdown(f"## {p['name']}")
            st.markdown(f"### {p['price']}")
            st.write(p['desc'])
            st.markdown("---")
            if st.button("← VOLVER AL CATÁLOGO"):
                st.session_state['viewing_product'] = None
                st.rerun()
        st.divider()

    # --- CATÁLOGO ---
    st.markdown("### PIEZAS DISPONIBLES")
    cols = st.columns(3)
    
    for idx, row in df.iterrows():
        product = get_full_details(row['url'])
        if product:
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="product-card">
                    <img src="{product['img']}" class="product-img">
                    <div class="info-area">
                        <div style="font-size:12px; letter-spacing:2px; text-transform:uppercase;">{product['name']}</div>
                        <div class="price-tag">{product['price']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Botones corregidos
                if st.button("VER DETALLES", key=f"det_{idx}"):
                    st.session_state['viewing_product'] = product
                    st.rerun()
                
                if st.button("AÑADIR AL PEDIDO", key=f"add_{idx}"):
                    st.session_state['cart'].append(product)
                    st.toast(f"Añadido: {product['name']}")

    # --- SIDEBAR (PEDIDO FINAL) ---
    with st.sidebar:
        st.markdown("<h2 style='letter-spacing:3px;'>PEDIDO</h2>", unsafe_allow_html=True)
        if not st.session_state['cart']:
            st.caption("Tu selección está vacía.")
        else:
            for i in st.session_state['cart']:
                st.markdown(f"**{i['name']}** - {i['price']}")
            
            st.divider()
            msg = "Hola Monú! Quisiera consultar por:\n" + "\n".join([f"- {i['name']}" for i in st.session_state['cart']])
            st.link_button("FINALIZAR POR WHATSAPP", f"https://wa.me/5491122334455?text={urllib.parse.quote(msg)}")
            
            if st.button("VACIAR CARRITO"):
                st.session_state['cart'] = []
                st.rerun()

if __name__ == "__main__":
    main()