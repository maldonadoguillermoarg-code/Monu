import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import requests
from bs4 import BeautifulSoup
import urllib.parse

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Monú | Boutique Auto-Store", layout="wide")

# 2. CSS B&W PROFESIONAL (Anula modo oscuro y fuerza estética Minimal)
def inject_custom_css():
    st.markdown("""
    <style>
        :root {
            --background-color: #F0F2F6;
            --text-color: #000000;
        }
        /* Fondo General */
        .stApp, [data-testid="stAppViewContainer"] {
            background-color: #F0F2F6 !important;
        }
        /* Forzar texto negro */
        h1, h2, h3, h4, p, span, div, label {
            color: #000000 !important;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }
        /* Contenedor de Producto */
        .product-card {
            background-color: #FFFFFF;
            border: 2px solid #000000;
            padding: 20px;
            margin-bottom: 20px;
            text-align: center;
            min-height: 450px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        /* Imagen B&W con Hover a Color */
        .product-img {
            filter: grayscale(100%);
            transition: 0.4s ease;
            max-width: 100%;
            height: auto;
            margin-bottom: 15px;
        }
        .product-img:hover {
            filter: grayscale(0%);
        }
        /* Botones Minimalistas */
        div.stButton > button {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            border-radius: 0px !important;
            border: none !important;
            font-weight: bold;
            width: 100%;
            padding: 10px;
        }
        div.stButton > button:hover {
            background-color: #444444 !important;
            box-shadow: 4px 4px 0px #000000;
        }
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 2px solid #000000;
        }
    </style>
    """, unsafe_allow_html=True)

# 3. MOTOR DE EXTRACCIÓN (Scraping Inteligente con Caché)
@st.cache_data(ttl=3600)
def get_product_info(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraer Nombre (Metadatos OG)
        name = soup.find("meta", property="og:title")
        name = name["content"].split(" - ")[0] if name else "Producto Monú"
        
        # Extraer Imagen
        img = soup.find("meta", property="og:image")
        img_url = img["content"] if img else "https://via.placeholder.com/400?text=Monu+Boutique"
        
        # Extraer Precio (Lógica para WooCommerce)
        price_meta = soup.find("meta", property="product:price:amount")
        if price_meta:
            price = f"${price_meta['content']}"
        else:
            # Búsqueda manual si falla el meta
            price_tag = soup.select_one(".woocommerce-Price-amount bdi, .price")
            price = price_tag.get_text() if price_tag else "Consultar"

        return {"name": name, "img": img_url, "price": price, "url": url}
    except Exception:
        return None

# 4. INICIALIZACIÓN DE CARRITO
if 'cart' not in st.session_state:
    st.session_state['cart'] = []

def main():
    inject_custom_css()
    
    # Logo o Título
    st.markdown("<h1 style='text-align:center; letter-spacing: 5px;'>M O N Ú</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; margin-bottom: 40px;'>BOUTIQUE ASTRAL & GLOBAL</p>", unsafe_allow_html=True)

    # Conexión a Google Sheets
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read()
        # Limpiar nombres de columnas y quitar filas vacías
        df.columns = [str(c).lower().strip() for c in df.columns]
        df = df.dropna(subset=['url'])
        urls = df['url'].tolist()
    except Exception as e:
        st.error("Error conectando con el Google Sheet. Verifica los Secrets.")
        return

    # SIDEBAR: Carrito
    with st.sidebar:
        st.markdown("### 🛒 TU SELECCIÓN")
        if not st.session_state['cart']:
            st.write("El carrito está vacío.")
        else:
            for i, item in enumerate(st.session_state['cart']):
                st.write(f"**{item['name']}** - {item['price']}")
            
            st.divider()
            
            # Generar link de WhatsApp
            items_list = "\n".join([f"- {i['name']} ({i['price']})" for i in st.session_state['cart']])
            wa_text = urllib.parse.quote(f"¡Hola Monú! Quisiera este pedido:\n\n{items_list}")
            
            st.link_button("FINALIZAR POR WHATSAPP", f"https://wa.me/5491122334455?text={wa_text}")
            
            if st.button("Limpiar Carrito"):
                st.session_state['cart'] = []
                st.rerun()

    # CATÁLOGO: Generación por cada fila del Sheet
    if urls:
        cols = st.columns(3)
        for idx, link in enumerate(urls):
            with st.spinner(f'Cargando producto {idx+1}...'):
                product = get_product_info(link)
                
            if product:
                with cols[idx % 3]:
                    # Renderizado de Tarjeta B&W
                    st.markdown(f"""
                    <div class="product-card">
                        <img src="{product['img']}" class="product-img">
                        <h4>{product['name']}</h4>
                        <p style="font-size: 1.2rem;"><b>{product['price']}</b></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Botones de Acción
                    st.link_button("VER WEB", product['url'])
                    if st.button("AÑADIR AL CARRITO", key=f"add_{idx}"):
                        st.session_state['cart'].append(product)
                        st.toast(f"Añadido: {product['name']}")
                        st.rerun()
    else:
        st.info("No hay links en el Google Sheet aún.")

if __name__ == "__main__":
    main()