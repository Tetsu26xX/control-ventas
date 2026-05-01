import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import base64
from supabase import create_client

st.set_page_config(page_title="Sistema Ventas", layout="wide")

# =========================
# IMÁGENES
# =========================
def get_base64_image(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""


# =========================
# CONEXIÓN SUPABASE
# =========================
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# =========================
# LOGIN
# =========================
if "login_ok" not in st.session_state:
    st.session_state["login_ok"] = False

def login():
    mascota_b64 = get_base64_image("assets/mascota_dashboard.png")

    st.markdown(f"""
    <style>
    .stApp {{
        background:
            radial-gradient(circle at 78% 18%, rgba(205, 230, 80, .20), transparent 18%),
            radial-gradient(circle at 92% 68%, rgba(205, 230, 80, .12), transparent 28%),
            linear-gradient(120deg, #17191f 0%, #1c1f27 42%, #101216 100%) !important;
        background-attachment: fixed !important;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background:
            radial-gradient(circle at 78% 10%, rgba(224,255,76,.28) 0 2px, transparent 3px),
            radial-gradient(circle at 84% 23%, rgba(224,255,76,.25) 0 2px, transparent 3px),
            radial-gradient(circle at 89% 38%, rgba(224,255,76,.20) 0 2px, transparent 3px),
            radial-gradient(circle at 75% 72%, rgba(224,255,76,.16) 0 2px, transparent 3px);
        opacity: .85;
        z-index: 0;
    }}
    .stApp::after {{
        content: "";
        position: fixed;
        right: -80px;
        top: -70px;
        width: 55vw;
        height: 110vh;
        pointer-events: none;
        background:
            linear-gradient(115deg, transparent 0 44%, rgba(210,245,62,.10) 45%, transparent 47%),
            linear-gradient(118deg, transparent 0 52%, rgba(210,245,62,.16) 53%, transparent 55%),
            radial-gradient(circle at 60% 30%, rgba(225,255,90,.22), transparent 9%),
            radial-gradient(circle at 70% 47%, rgba(225,255,90,.16), transparent 7%);
        filter: blur(1px);
        opacity: .9;
        z-index: 0;
    }}
    header[data-testid="stHeader"] {{ background: transparent !important; }}
    #MainMenu, footer {{ visibility: hidden !important; }}
    .block-container {{
        max-width: 1280px !important;
        padding-top: 3.2rem !important;
        padding-bottom: 0rem !important;
        position: relative;
        z-index: 2;
    }}
    div[data-testid="stHorizontalBlock"]:first-of-type {{
        min-height: calc(100vh - 125px);
        align-items: center !important;
        gap: 4rem !important;
    }}
    div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="column"]:first-child {{
        max-width: 390px !important;
        padding-left: 1.8rem !important;
    }}
    .login-logo {{
        color: #ffffff;
        font-size: 3rem;
        line-height: .94;
        font-weight: 1000;
        letter-spacing: -1px;
        margin-bottom: 1.35rem;
        text-transform: uppercase;
        transform: skew(-7deg);
        text-shadow: 0 10px 30px rgba(0,0,0,.35);
    }}
    .login-logo span {{ color: #d9f34c; display: block; }}
    .login-divider {{
        display: flex;
        align-items: center;
        gap: 12px;
        color: rgba(255,255,255,.66);
        font-size: .76rem;
        margin: 1.1rem 0 1.25rem;
    }}
    .login-divider::before, .login-divider::after {{
        content: "";
        height: 1px;
        flex: 1;
        background: rgba(255,255,255,.34);
    }}
    .helper-link {{
        text-align:center;
        color:#d9f34c;
        font-size:.78rem;
        font-weight:800;
        margin-top: 1.15rem;
        opacity:.92;
    }}
    .login-terms {{
        color: rgba(255,255,255,.68);
        text-align:center;
        font-size:.68rem;
        line-height:1.45;
        margin-top:1.55rem;
    }}
    .login-terms b {{ color:#d9f34c; }}
    .google-btn {{
        height: 2.55rem;
        border: 1px solid rgba(255,255,255,.34);
        color: rgba(255,255,255,.82);
        display:flex;
        align-items:center;
        justify-content:center;
        gap:.55rem;
        font-size:.76rem;
        font-weight:800;
        margin-bottom:.85rem;
        background: rgba(0,0,0,.08);
    }}
    div[data-testid="stTextInput"] label {{
        color: rgba(255,255,255,.88) !important;
        font-weight: 700 !important;
        font-size: .8rem !important;
    }}
    div[data-testid="stTextInput"] input {{
        background: #2b2d36 !important;
        border: 1px solid rgba(255,255,255,.08) !important;
        color: white !important;
        border-radius: 0 !important;
        min-height: 2.75rem !important;
        font-weight: 700 !important;
        box-shadow: none !important;
    }}
    div[data-testid="stTextInput"] input:focus {{
        border-color: #d9f34c !important;
        box-shadow: 0 0 0 1px rgba(217,243,76,.55), 0 0 26px rgba(217,243,76,.12) !important;
    }}
    .stButton > button, [data-testid="stFormSubmitButton"] button {{
        width: 100% !important;
        min-height: 2.85rem !important;
        border-radius: 2px !important;
        border: none !important;
        background: #d9f34c !important;
        color: #22252b !important;
        font-weight: 900 !important;
        box-shadow: 0 0 0 rgba(217,243,76,0) !important;
        transition: all .22s ease !important;
    }}
    .stButton > button:hover, [data-testid="stFormSubmitButton"] button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 0 18px rgba(217,243,76,.35), 0 14px 30px rgba(0,0,0,.28) !important;
        filter: brightness(1.04);
    }}
    .hero-wrap {{
        width: min(660px, 100%);
        min-height: 560px;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    .hero-copy {{
        position: absolute;
        left: 0;
        top: 28px;
        max-width: 390px;
        color: white;
        z-index: 3;
    }}
    .hero-kicker {{ color:#d9f34c; font-weight:1000; font-size:.9rem; margin-bottom:.45rem; }}
    .hero-title {{
        margin:0;
        color:#ffffff;
        font-size: clamp(2.7rem, 4.4vw, 4.45rem);
        line-height:.96;
        font-weight:1000;
        letter-spacing:-1.5px;
        text-shadow: 0 15px 45px rgba(0,0,0,.45);
    }}
    .hero-title span {{ color:#d9f34c; }}
    .hero-sub {{
        margin-top:1.15rem;
        color: rgba(255,255,255,.88);
        font-weight:750;
        line-height:1.45;
        max-width: 520px;
    }}
    .mascot-box {{
        position:absolute;
        right: 4%;
        bottom: 18px;
        width: min(420px, 72%);
        z-index: 2;
        filter: drop-shadow(0 20px 35px rgba(0,0,0,.42));
        transition: all .25s ease;
    }}
    .mascot-box:hover {{
        transform: translateY(-5px) scale(1.015);
        filter: drop-shadow(0 0 24px rgba(217,243,76,.22)) drop-shadow(0 24px 38px rgba(0,0,0,.44));
    }}
    .mascot-box img {{ width:100%; display:block; }}
    .feature-row {{
        position: absolute;
        left: 0;
        bottom: 40px;
        width: 430px;
        display:grid;
        grid-template-columns: repeat(3, 1fr);
        gap:12px;
        z-index: 4;
    }}
    .feature-card {{
        min-height:84px;
        padding:12px 12px;
        border-radius:4px;
        background: rgba(30,32,40,.72);
        border:1px solid rgba(255,255,255,.13);
        color:white;
        backdrop-filter: blur(12px);
        box-shadow: 0 14px 34px rgba(0,0,0,.24);
        transition: all .24s ease;
    }}
    .feature-card:hover {{
        transform: translateY(-5px);
        border-color: rgba(217,243,76,.55);
        box-shadow: 0 0 18px rgba(217,243,76,.20), 0 18px 38px rgba(0,0,0,.34);
    }}
    .feature-icon {{font-size:1.4rem; margin-bottom:.35rem;}}
    .feature-title {{font-weight:1000; font-size:.92rem;}}
    .feature-text {{font-size:.70rem; opacity:.76; margin-top:.25rem; line-height:1.3;}}
    @media (max-width: 900px) {{
        .block-container {{ padding-top: 1.5rem !important; }}
        div[data-testid="stHorizontalBlock"]:first-of-type {{ min-height: auto; gap: 1.5rem !important; }}
        .hero-wrap {{ min-height: 500px; }}
        .hero-copy {{ position:relative; top:auto; left:auto; }}
        .mascot-box {{ position:relative; right:auto; bottom:auto; width:80%; margin: 1rem auto 0; }}
        .feature-row {{ position:relative; left:auto; bottom:auto; width:100%; margin-top:1rem; }}
    }}
    </style>
    """, unsafe_allow_html=True)

    col_login, col_hero = st.columns([0.38, 0.62], gap="large")

    with col_login:
        st.markdown("""
        <div class="login-logo">Control<span>Ventas</span></div>
        <div class="google-btn">🔐 Acceso autorizado</div>
        <div class="login-divider">O</div>
        """, unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            usuario = st.text_input("Usuario 🧐", placeholder="Usuario").strip().upper()
            password = st.text_input("Contraseña 🔑", type="password", placeholder="Contraseña").strip()
            submitted = st.form_submit_button("Iniciar sesión")

        st.markdown("""
        <div class="helper-link">Olvidé mi contraseña</div>
        <div class="login-terms">
            ¿Me valoran?-_- porque siento que no<br>
            Al iniciar sesión, aceptas el uso autorizado del sistema <b>Control Ventas</b>.
        </div>
        """, unsafe_allow_html=True)

        if submitted:
            if not usuario or not password:
                st.error("Ingresa usuario y contraseña.")
            else:
                with st.spinner("Validando acceso..."):
                    data = supabase.table("usuarios").select("*").eq("usuario", usuario).execute().data

                if data:
                    user = data[0]
                    if str(user.get("password", "")) == password and str(user.get("estado", "")).upper() == "ACTIVO":
                        st.session_state["login_ok"] = True
                        st.session_state["usuario"] = user.get("usuario", "")
                        st.session_state["rol"] = user.get("rol", "")
                        st.session_state["vendedor"] = user.get("vendedor", "")
                        st.rerun()
                    else:
                        st.error("Contraseña incorrecta o usuario inactivo.")
                else:
                    st.error("Usuario no existe.")

    with col_hero:
        mascota_html = f'<div class="mascot-box"><img src="data:image/png;base64,{mascota_b64}"></div>' if mascota_b64 else ""
        st.markdown(f"""
        <div class="hero-wrap">
            <div class="hero-copy">
                <div class="hero-kicker">Bienvenido a</div>
                <h1 class="hero-title">Control<br><span>Ventas</span></h1>
                <div class="hero-sub">Sistema para registrar ventas, controlar stock, revisar rankings y consultar IMEI por marca y fecha.</div>
            </div>
            {mascota_html}
            <div class="feature-row">
                <div class="feature-card"><div class="feature-icon">🛒</div><div class="feature-title">Ventas</div><div class="feature-text">Registra y consulta todas tus ventas.</div></div>
                <div class="feature-card"><div class="feature-icon">📦</div><div class="feature-title">Stock</div><div class="feature-text">Controla ingresos, salidas y traslados.</div></div>
                <div class="feature-card"><div class="feature-icon">📊</div><div class="feature-title">Reportes</div><div class="feature-text">Rankings y estadísticas rápidas.</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

if not st.session_state["login_ok"]:
    login()
    st.stop()

# =========================
# AVISO INSTRUCCIONES
# =========================
if "aviso_instrucciones_visto" not in st.session_state:
    st.session_state["aviso_instrucciones_visto"] = False

if not st.session_state["aviso_instrucciones_visto"]:

    st.warning("⚠️ IMPORTANTE: antes de usar el sistema, lee las instrucciones.")

    st.markdown("""
    <div class="glass-card">
        <h3>📌 Lee las instrucciones antes de trabajar</h3>
        <p>
        Verifica siempre la información antes de guardar.  
        No edites órdenes de otros vendedores.  
        No registres datos incompletos.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("✅ Entendido, continuar", use_container_width=True):
        st.session_state["aviso_instrucciones_visto"] = True
        st.session_state["menu_actual"] = "📌 Instrucciones"
        st.rerun()

    st.stop()


def cargar_tabla(nombre, columnas=None):
    try:
        data = supabase.table(nombre).select("*").execute().data
        df = pd.DataFrame(data)
        if columnas:
            for col in columnas:
                if col not in df.columns:
                    df[col] = ""
            df = df[columnas]
        return df
    except Exception as e:
        st.error(f"Error cargando tabla {nombre}: {e}")
        return pd.DataFrame(columns=columnas or [])

def insertar_registro(tabla, registro):
    return supabase.table(tabla).insert(registro).execute()

def actualizar_registro(tabla, registro_id, cambios):
    return supabase.table(tabla).update(cambios).eq("id", registro_id).execute()

def eliminar_registro(tabla, registro_id):
    return supabase.table(tabla).delete().eq("id", registro_id).execute()



# =========================
# ESTILO VISUAL PERSONALIZADO
# =========================
fondo_menu = get_base64_image("assets/fondo_menu.png")

st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(135deg, #07111f 0%, #0e1726 45%, #111827 100%);
}}

[data-testid="stSidebar"] {{
    background-image:
        linear-gradient(180deg, rgba(0,30,65,0.55), rgba(0,87,168,0.55), rgba(227,6,19,0.45)),
        url("data:image/png;base64,{fondo_menu}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}

[data-testid="stSidebar"] * {{
    color: white !important;
}}

[data-testid="stSidebar"] details {{
    background: rgba(255,255,255,0.10);
    border-radius: 14px;
    margin-bottom: 10px;
    padding: 4px 8px;
    border: 1px solid rgba(255,255,255,0.18);
    backdrop-filter: blur(8px);
}}

[data-testid="stSidebar"] summary {{
    font-weight: 900 !important;
    font-size: 17px !important;
}}

[data-testid="stSidebar"] .stButton > button {{
    background: rgba(255,255,255,0.13) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.20) !important;
    box-shadow: none !important;
    text-align: left !important;
    justify-content: flex-start !important;
    margin: 3px 0 !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
}}

[data-testid="stSidebar"] .stButton > button:hover {{
    background: rgba(255,255,255,0.26) !important;
    transform: translateX(3px) !important;
}}

h1 {{
    color: #FFFFFF !important;
    font-size: 42px !important;
    font-weight: 900 !important;
    letter-spacing: -0.5px;
    animation: glowPulse 3s infinite;
}}

h2, h3 {{
    color: #F8FAFC !important;
    font-weight: 800 !important;
}}

[data-testid="stMetric"] {{
    background: linear-gradient(135deg, rgba(0,87,168,0.90), rgba(14,165,233,0.85));
    padding: 18px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.18);
    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
}}

.stButton > button {{
    background: linear-gradient(135deg, #E30613 0%, #FF6B00 100%);
    color: white !important;
    border: none;
    border-radius: 14px;
    padding: 0.65rem 1.2rem;
    font-weight: 900;
}}

[data-testid="stDataFrame"] {{
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 8px 28px rgba(0,0,0,0.28);
}}

.glass-primary {{
    background: linear-gradient(135deg, rgba(0,87,168,0.78), rgba(227,6,19,0.65));
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.25);
    box-shadow: 0 18px 45px rgba(0,0,0,0.36);
    border-radius: 28px;
    padding: 22px 26px;
    margin-bottom: 22px;
}}

.glass-primary h3, .glass-primary p {{
    color: white !important;
    margin: 0;
}}

@keyframes glowPulse {{
    0% {{ text-shadow: 0 0 8px rgba(14,165,233,0.35); }}
    50% {{ text-shadow: 0 0 18px rgba(227,6,19,0.35); }}
    100% {{ text-shadow: 0 0 8px rgba(14,165,233,0.35); }}
}}
</style>
""", unsafe_allow_html=True)


# =========================
# OVERRIDE VISUAL: combina con login oscuro/lima
# =========================
st.markdown(f"""
<style>
.stApp {{
    background:
        radial-gradient(circle at top left, rgba(207, 237, 62, 0.13), transparent 34%),
        radial-gradient(circle at bottom right, rgba(207, 237, 62, 0.10), transparent 30%),
        linear-gradient(135deg, #17191f 0%, #1c1f27 52%, #101216 100%) !important;
}}

[data-testid="stSidebar"] {{
    background-image:
        linear-gradient(180deg, rgba(14, 16, 22, 0.76), rgba(20, 23, 31, 0.74), rgba(10, 11, 15, 0.82)),
        url("data:image/png;base64,{fondo_menu}") !important;
    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
    border-right: 1px solid rgba(210,245,62,0.20) !important;
    box-shadow: 10px 0 35px rgba(0,0,0,.24), 0 0 24px rgba(210,245,62,.10) !important;
}}

[data-testid="stSidebar"] * {{ color: #F6F7EE !important; }}

[data-testid="stSidebar"] details {{
    background: linear-gradient(135deg, rgba(255,255,255,0.105), rgba(255,255,255,0.045)) !important;
    border-radius: 18px !important;
    margin-bottom: 12px !important;
    padding: 5px 8px !important;
    border: 1px solid rgba(255,255,255,0.16) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.16), 0 8px 20px rgba(0,0,0,.18) !important;
    backdrop-filter: blur(14px) !important;
    -webkit-backdrop-filter: blur(14px) !important;
}}

[data-testid="stSidebar"] summary {{
    font-weight: 900 !important;
    font-size: 17px !important;
}}

[data-testid="stSidebar"] .stButton > button {{
    background: linear-gradient(135deg, rgba(255,255,255,0.13), rgba(255,255,255,0.055)) !important;
    color: #F8FAFC !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.16), 0 8px 18px rgba(0,0,0,.14) !important;
    text-align: left !important;
    justify-content: flex-start !important;
    margin: 4px 0 !important;
    border-radius: 15px !important;
    font-weight: 850 !important;
    transition: all .22s ease !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
}}

[data-testid="stSidebar"] .stButton > button:hover {{
    transform: translateX(5px) translateY(-1px) !important;
    background: linear-gradient(135deg, rgba(210,245,62,.18), rgba(255,255,255,.08)) !important;
    border-color: rgba(210,245,62,.55) !important;
    box-shadow:
        0 0 0 1px rgba(210,245,62,.14),
        0 0 18px rgba(210,245,62,.25),
        0 10px 24px rgba(0,0,0,.22) !important;
}}

h1 {{ color: #F3F5EB !important; }}
h2, h3 {{ color: #F8FAFC !important; }}

[data-testid="stMetric"] {{
    background: linear-gradient(135deg, rgba(30,33,42,0.92), rgba(44,48,58,0.82)) !important;
    border: 1px solid rgba(210,245,62,0.18) !important;
    box-shadow: 0 10px 25px rgba(0,0,0,0.25), 0 0 18px rgba(210,245,62,.08) !important;
}}

.stButton > button {{
    background: linear-gradient(90deg, #d7f54a 0%, #9acb31 100%) !important;
    color: #14161b !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 900 !important;
    box-shadow: 0 8px 22px rgba(210,245,62,.20) !important;
    transition: all .22s ease !important;
}}

.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 0 18px rgba(210,245,62,.42), 0 14px 28px rgba(0,0,0,.24) !important;
}}

[data-testid="stDataFrame"] {{
    border: 1px solid rgba(210,245,62,0.13) !important;
    box-shadow: 0 8px 28px rgba(0,0,0,0.28) !important;
}}

.glass-primary {{
    background: linear-gradient(135deg, rgba(255,255,255,0.10), rgba(255,255,255,0.045)) !important;
    border: 1px solid rgba(210,245,62,0.16) !important;
    box-shadow: 0 18px 45px rgba(0,0,0,0.34), 0 0 22px rgba(210,245,62,.08) !important;
}}
</style>
""", unsafe_allow_html=True)

# =========================
# FUNCIONES BASE
# =========================
def cargar_csv(ruta, sep=","):
    try:
        df = pd.read_csv(ruta, sep=sep, dtype=str, keep_default_na=False)
        df.columns = df.columns.str.strip()
        return df
    except FileNotFoundError:
        return pd.DataFrame()

def guardar_csv(df, ruta):
    # CSV queda solo como respaldo local; Supabase es la base principal.
    df.to_csv(ruta, index=False)

def guardar_ventas(df):
    pass

def guardar_movimientos_stock(df):
    pass

def mostrar_confeti():
    piezas = ""
    colores = [
        "#ff4757", "#ffa502", "#2ed573", "#1e90ff", "#a55eea", "#ff6b81",
        "#70a1ff", "#7bed9f", "#feca57", "#ff9ff3", "#54a0ff", "#5f27cd",
        "#00d2d3", "#ff9f43", "#ee5253", "#10ac84", "#341f97", "#48dbfb",
        "#ff3838", "#32ff7e", "#18dcff", "#7d5fff", "#fff200", "#ffb8b8",
        "#c56cf0", "#3ae374", "#67e6dc", "#ffd32a", "#ff4d4d", "#4b7bec"
    ]
    for i in range(1, 61):
        color = colores[i % len(colores)]
        piezas += f'<span style="--i:{i}; --c:{color}; --x:{(i * 17) % 100}; --d:{(i % 9) / 10}s;"></span>'

    components.html(
        f"""
        <div class="confetti-wrap">{piezas}</div>
        <style>
        .confetti-wrap {{
            position: relative;
            height: 140px;
            overflow: hidden;
            background: transparent;
        }}
        .confetti-wrap span {{
            position: absolute;
            top: -25px;
            left: calc(var(--x) * 1%);
            width: 9px;
            height: 15px;
            background: var(--c);
            opacity: 0.95;
            animation: fall 2.4s linear forwards;
            animation-delay: var(--d);
            transform: rotate(20deg);
            border-radius: 2px;
        }}
        .confetti-wrap span:nth-child(3n) {{
            width: 7px;
            height: 7px;
            border-radius: 50%;
        }}
        .confetti-wrap span:nth-child(4n) {{
            width: 12px;
            height: 6px;
        }}
        @keyframes fall {{
            0% {{ transform: translateY(0) rotate(0deg); opacity: 1; }}
            100% {{ transform: translateY(160px) rotate(900deg); opacity: 0; }}
        }}
        </style>
        """,
        height=150,
    )

def texto_top_vendedor(row):
    if pd.isna(row["vendedor"]) or row["vendedor"] == "":
        return ""
    return f'{row["vendedor"]} ({int(row["cantidad"])})'

def semana_del_mes(fecha):
    if pd.isna(fecha):
        return None
    return ((fecha.day - 1) // 7) + 1

def oscurecer_color(hex_color, factor=0.55):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255
    return (r * factor, g * factor, b * factor)

def seleccionar_producto(df_productos, prefijo="", default_marca=None, default_modelo=None, default_color=None, default_tipo=None):
    marcas = sorted(df_productos["marca"].dropna().unique())

    if default_marca in marcas:
        marca_index = marcas.index(default_marca)
    else:
        marca_index = 0

    marca = st.selectbox(
        "Marca",
        marcas,
        index=marca_index,
        key=f"{prefijo}_marca"
    )

    color_marca = COLORES_MARCA.get(str(marca).upper(), "#95A5A6")
    st.markdown(
        f"<div style='background:{color_marca}; color:white; padding:8px 12px; "
        f"border-radius:10px; display:inline-block; font-weight:700;'>Marca seleccionada: {marca}</div>",
        unsafe_allow_html=True
    )

    modelos = sorted(df_productos[df_productos["marca"] == marca]["modelo"].dropna().unique())
    if default_modelo in modelos:
        modelo_index = modelos.index(default_modelo)
    else:
        modelo_index = 0

    modelo = st.selectbox(
        "Modelo",
        modelos,
        index=modelo_index,
        key=f"{prefijo}_modelo"
    )

    colores = sorted(df_productos[
        (df_productos["marca"] == marca) &
        (df_productos["modelo"] == modelo)
    ]["color"].dropna().unique())

    if default_color in colores:
        color_index = colores.index(default_color)
    else:
        color_index = 0

    color = st.selectbox(
        "Color",
        colores,
        index=color_index,
        key=f"{prefijo}_color"
    )

    tipos = sorted(df_productos[
        (df_productos["marca"] == marca) &
        (df_productos["modelo"] == modelo) &
        (df_productos["color"] == color)
    ]["tipo"].dropna().unique())

    if default_tipo in tipos:
        tipo_index = tipos.index(default_tipo)
    else:
        tipo_index = 0

    tipo = st.selectbox(
        "Tipo",
        tipos,
        index=tipo_index,
        key=f"{prefijo}_tipo"
    )

    resultado = df_productos[
        (df_productos["marca"] == marca) &
        (df_productos["modelo"] == modelo) &
        (df_productos["color"] == color) &
        (df_productos["tipo"] == tipo)
    ]

    return resultado.iloc[0], resultado

def calcular_stock(productos, movimientos_stock, ventas):
    base = productos.copy()
    base["sku"] = base["sku"].astype(str)

    if movimientos_stock.empty:
        mov_resumen = pd.DataFrame(columns=["sku", "movimiento_stock"])
    else:
        mov = movimientos_stock.copy()
        mov["cantidad"] = pd.to_numeric(mov["cantidad"], errors="coerce").fillna(0)
        mov["signo"] = mov["tipo_movimiento"].map({
            "STOCK INICIAL": 1,
            "INGRESO": 1,
            "TRASLADO INGRESO": 1,
            "SALIDA": -1,
            "TRASLADO SALIDA": -1,
        }).fillna(0)
        mov["movimiento_stock"] = mov["cantidad"] * mov["signo"]
        mov_resumen = mov.groupby("sku")["movimiento_stock"].sum().reset_index()

    if ventas.empty:
        ventas_resumen = pd.DataFrame(columns=["sku", "ventas_stock"])
    else:
        ven = ventas.copy()
        ven["cantidad"] = pd.to_numeric(ven["cantidad"], errors="coerce").fillna(0)
        ven = ven[ven["sku"].astype(str).str.strip() != ""]
        ventas_resumen = ven.groupby("sku")["cantidad"].sum().reset_index()
        ventas_resumen["ventas_stock"] = ventas_resumen["cantidad"] * -1
        ventas_resumen = ventas_resumen[["sku", "ventas_stock"]]

    stock = base.merge(mov_resumen, on="sku", how="left")
    stock = stock.merge(ventas_resumen, on="sku", how="left")
    stock["movimiento_stock"] = pd.to_numeric(stock["movimiento_stock"], errors="coerce").fillna(0)
    stock["ventas_stock"] = pd.to_numeric(stock["ventas_stock"], errors="coerce").fillna(0)
    stock["stock_actual"] = stock["movimiento_stock"] + stock["ventas_stock"]

    stock = stock.sort_values(["marca", "modelo", "color", "tipo"])
    return stock

def preparar_fecha_hora(df):
    df = df.copy()
    if "fecha" in df.columns:
        df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce").dt.strftime("%Y-%m-%d").fillna("")
    if "creado_en" in df.columns:
        dt = pd.to_datetime(df["creado_en"], errors="coerce")
        # Mostrar fecha/hora local aproximada restando 5 horas de UTC (Perú/Colombia)
        dt = dt - pd.Timedelta(hours=5)
        df["hora"] = dt.dt.strftime("%H:%M:%S").fillna("")
        df = df.drop(columns=["creado_en"], errors="ignore")
    return df

def ordenar_columnas_existentes(df, columnas):
    existentes = [c for c in columnas if c in df.columns]
    restantes = [c for c in df.columns if c not in existentes]
    return df[existentes + restantes]

def registrar_movimiento_stock(tipo_movimiento, requiere_jefe=False):
    st.subheader(tipo_movimiento.title())

    if st.session_state.get("stock_guardado_ok", ""):
        st.success(st.session_state["stock_guardado_ok"])
        mostrar_confeti()
        st.session_state["stock_guardado_ok"] = ""

    version = st.session_state.get("stock_form_version", 0)
    prefijo = f"stock_{tipo_movimiento}_{version}"

    fecha = st.date_input("Fecha", key=f"{prefijo}_fecha")

    # Para INGRESO y STOCK INICIAL se muestran todos los productos.
    # Para SALIDA/TRASLADO SALIDA se muestran solo productos con stock disponible.
    df_productos = productos.copy()
    if tipo_movimiento in ["SALIDA", "TRASLADO SALIDA"]:
        stock_para_salida = calcular_stock(productos, movimientos_stock, ventas)
        stock_para_salida["stock_actual"] = pd.to_numeric(
            stock_para_salida["stock_actual"], errors="coerce"
        ).fillna(0).astype(int)

        df_productos = stock_para_salida[stock_para_salida["stock_actual"] > 0].copy()

        if df_productos.empty:
            st.warning("No hay productos con stock disponible para salida o traslado.")
            return

    producto, producto_df = seleccionar_producto(df_productos, prefijo=prefijo)

    st.write("Producto seleccionado:")
    st.dataframe(producto_df.astype(str), use_container_width=True)

    stock_disponible = None
    if tipo_movimiento in ["SALIDA", "TRASLADO SALIDA"]:
        stock_disponible = int(pd.to_numeric(producto.get("stock_actual", 0), errors="coerce"))
        st.info(f"Stock disponible: {stock_disponible}")

    cantidad = st.number_input("Cantidad", min_value=1, step=1, key=f"{prefijo}_cantidad")

    jefe_solicita = ""
    if requiere_jefe:
        jefes_activos = jefes[jefes["estado"] == "ACTIVO"]["nombre"]
        jefe_solicita = st.selectbox("Jefe que solicita", jefes_activos, key=f"{prefijo}_jefe")

    vendedores_activos = vendedores[vendedores["estado"] == "ACTIVO"]["nombre"]

    if st.session_state.get("rol") == "admin":
        vendedor_responsable = st.selectbox(
            "Vendedor responsable",
            vendedores_activos,
            key=f"{prefijo}_vendedor"
        )
    else:
        vendedor_responsable = st.session_state.get("vendedor", "")
        st.text_input(
            "Vendedor responsable",
            vendedor_responsable,
            disabled=True,
            key=f"{prefijo}_vendedor"
        )

    detalle = st.text_input("Detalle / observación", key=f"{prefijo}_detalle")

    if st.button(f"Guardar {tipo_movimiento.title()}", key=f"{prefijo}_guardar"):
        if stock_disponible is not None and int(cantidad) > stock_disponible:
            st.error(f"No puedes sacar {cantidad}. Solo hay {stock_disponible} en stock.")
            return

        nuevo_mov = {
            "fecha": fecha.strftime("%Y-%m-%d"),
            "tipo_movimiento": tipo_movimiento,
            "sku": producto["sku"],
            "cantidad": int(cantidad),
            "jefe_solicita": jefe_solicita,
            "vendedor_responsable": vendedor_responsable,
            "detalle": detalle
        }

        insertar_registro("movimientos_stock", nuevo_mov)

        st.session_state["stock_guardado_ok"] = (
            f"{tipo_movimiento.title()} guardado correctamente ✅ Ya puedes registrar otro movimiento."
        )
        st.session_state["stock_form_version"] = version + 1
        st.rerun()

# =========================
# COLORES Y MESES
# =========================
COLORES_MARCA = {
    "OPPO": "#2ECC71",
    "SAMSUNG": "#3498DB",
    "XIAOMI": "#F39C12",
    "HONOR": "#9B59B6",
    "APPLE": "#BDC3C7",
    "MOTOROLA": "#E67E22",
    "ZTE": "#E74C3C",
    "VIVO": "#6C5CE7",
}

MESES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}
MESES_INVERSO = {v: k for k, v in MESES.items()}

# =========================
# CARGA DE DATOS
# =========================
productos = cargar_tabla("productos", ["id", "marca", "sku", "modelo", "color", "tipo"])
accesorios = cargar_tabla("accesorios", ["id", "marca", "sku", "descripcion"])
vendedores = cargar_tabla("vendedores", ["id", "nombre", "estado"])
jefes = cargar_tabla("jefes", ["id", "nombre", "estado"])
usuarios = cargar_tabla("usuarios", ["id", "usuario", "password", "rol", "vendedor", "estado"])
ventas = cargar_tabla("ventas", [
    "id", "fecha", "creado_en", "vendedor", "orden", "chip", "tipo_chip", "imei",
    "sku", "marca", "modelo", "color", "tipo", "cantidad",
    "accesorio_sku", "accesorio", "cantidad_accesorio"
])
movimientos_stock = cargar_tabla("movimientos_stock", [
    "id", "fecha", "creado_en", "tipo_movimiento", "sku", "cantidad",
    "jefe_solicita", "vendedor_responsable", "detalle"
])

columnas_ventas = [
    "id", "fecha", "creado_en", "vendedor", "orden", "chip", "tipo_chip", "imei",
    "sku", "marca", "modelo", "color", "tipo", "cantidad",
    "accesorio_sku", "accesorio", "cantidad_accesorio"
]
for col in columnas_ventas:
    if col not in ventas.columns:
        ventas[col] = ""
ventas = ventas[columnas_ventas]

columnas_stock = [
    "id", "fecha", "creado_en", "tipo_movimiento", "sku", "cantidad",
    "jefe_solicita", "vendedor_responsable", "detalle"
]
for col in columnas_stock:
    if col not in movimientos_stock.columns:
        movimientos_stock[col] = ""
movimientos_stock = movimientos_stock[columnas_stock]

if "form_version" not in st.session_state:
    st.session_state["form_version"] = 0

if "stock_form_version" not in st.session_state:
    st.session_state["stock_form_version"] = 0

if "stock_guardado_ok" not in st.session_state:
    st.session_state["stock_guardado_ok"] = ""

stock_actual_df = calcular_stock(productos, movimientos_stock, ventas)

# =========================
# MENÚ
# =========================
st.sidebar.title("⚡ Control Ventas")
if st.session_state.get("login_ok", False):
    rol_txt = str(st.session_state.get("rol", "")).upper()
    vendedor_txt = str(st.session_state.get("vendedor", "")).upper()
    if rol_txt == "ADMIN":
        st.sidebar.success(f"👑 {vendedor_txt} · VENDEDOR ADMIN")
    else:
        st.sidebar.success(f"👤 {vendedor_txt} · VENDEDOR")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state["login_ok"] = False
        st.session_state["usuario"] = ""
        st.session_state["rol"] = ""
        st.session_state["vendedor"] = ""
        st.rerun()

st.sidebar.markdown("### 📲 Menú")

if "menu_actual" not in st.session_state:
    st.session_state["menu_actual"] = "📊 Dashboard"

def boton_menu(texto):
    activo = st.session_state["menu_actual"] == texto
    etiqueta = f"✅ {texto}" if activo else f"　{texto}"
    if st.button(etiqueta, use_container_width=True, key=f"btn_{texto}"):
        st.session_state["menu_actual"] = texto
        st.rerun()

with st.sidebar.expander("✨ Principal", expanded=True):
    boton_menu("📊 Dashboard")
    boton_menu("🧾 Registrar Orden")
    boton_menu("📌 Instrucciones")

with st.sidebar.expander("🛒 Gestión de Venta", expanded=False):
    boton_menu("🔍 Buscar")
    boton_menu("✏️ Editar Venta")
    boton_menu("📋 Ventas Registradas")
    boton_menu("📱 Buscar IMEI")

with st.sidebar.expander("📦 Inventario", expanded=False):
    boton_menu("📦 Inventario")

with st.sidebar.expander("🧩 Productos", expanded=False):
    boton_menu("📱 Catálogo Equipos")
    boton_menu("🎧 Catálogo Accesorios")
    boton_menu("➕ Nuevo Equipo")
    boton_menu("➕ Nuevo Accesorio")

with st.sidebar.expander("👥 Equipo", expanded=False):
    boton_menu("🧑‍💼 Vendedores")

menu = st.session_state["menu_actual"]

# =========================
# DASHBOARD
# =========================
if menu == "📌 Instrucciones":
    st.title("📌 Guía de uso del sistema")

    st.markdown("""
    <div class="glass-primary">
        <h3>⚠️ Uso correcto obligatorio</h3>
        <p>Este sistema controla ventas e inventario en tiempo real. Un error afecta todo el stock.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
    <h4>🧾 Registro de ventas</h4>
    <ul>
        <li>Selecciona correctamente si la orden incluye: Chip, Equipo o Accesorio.</li>
        <li>Si hay equipo, ingresa el IMEI correctamente.</li>
        <li>Verifica marca, modelo, color y tipo antes de guardar.</li>
        <li>No repitas órdenes ya registradas.</li>
        <li>Presiona <b>Guardar una sola vez</b> y espera la confirmación.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
    <h4>📦 Ingreso de mercadería</h4>
    <ul>
        <li>Usa esta opción solo cuando ingresen equipos nuevos.</li>
        <li>Elige bien marca, modelo, color y tipo.</li>
        <li>Verifica la cantidad antes de guardar.</li>
        <li>Presiona guardar una sola vez y espera confirmación.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
    <h4>🔁 Traslados y salidas</h4>
    <ul>
        <li>Usa traslado solo cuando el equipo se mueve de ubicación o responsable.</li>
        <li>Usa salida cuando el equipo debe descontarse del stock.</li>
        <li>No registres cantidades mayores al stock disponible.</li>
        <li>Revisa siempre el producto antes de guardar.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
    <h4>🚫 Reglas importantes</h4>
    <ul>
        <li>No tocar vendedores sin autorización.</li>
        <li>No editar ni eliminar órdenes de otros vendedores.</li>
        <li>No registrar información incompleta.</li>
        <li>Todo cambio afecta ventas, reportes e inventario.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
    <h4>✅ Recomendación final</h4>
    <ul>
        <li>Revisa todo antes de guardar.</li>
        <li>Registra con calma.</li>
        <li>Ante cualquier duda, consulta antes de ingresar datos.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

elif menu == "📊 Dashboard":
    st.title("📊 Dashboard de Ventas")
    st.markdown("""
    <div class="glass-primary">
        <h3>🚀 Control en tiempo real</h3>
        <p>Ventas, rankings, stock y seguimiento en un solo panel.</p>
    </div>
    """, unsafe_allow_html=True)

    mascota_dashboard = get_base64_image("assets/mascota_dashboard.png")
    if mascota_dashboard:
        st.markdown(f"""
        <div style="position: fixed; bottom: 14px; right: 24px; z-index: 999;">
            <img src="data:image/png;base64,{mascota_dashboard}" width="170">
        </div>
        """, unsafe_allow_html=True)

    if ventas.empty or ventas["orden"].fillna("").eq("").all():
        st.info("Aún no hay ventas registradas.")
    else:
        ventas_dash = ventas.copy()
        ventas_dash["fecha"] = pd.to_datetime(ventas_dash["fecha"], errors="coerce")
        ventas_dash["cantidad"] = pd.to_numeric(ventas_dash["cantidad"], errors="coerce").fillna(0)
        ventas_dash["cantidad_accesorio"] = pd.to_numeric(
            ventas_dash["cantidad_accesorio"], errors="coerce"
        ).fillna(0)
        ventas_dash["semana_mes"] = ventas_dash["fecha"].apply(semana_del_mes)

        ventas_validas_fecha = ventas_dash.dropna(subset=["fecha"])

        st.subheader("Filtros")
        col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns(5)

        años = sorted(ventas_validas_fecha["fecha"].dt.year.unique(), reverse=True)
        with col_f1:
            año = st.selectbox("Año", ["TODOS"] + años)

        temp_fechas = ventas_validas_fecha.copy()
        if año != "TODOS":
            temp_fechas = temp_fechas[temp_fechas["fecha"].dt.year == año]

        meses_numeros = sorted(temp_fechas["fecha"].dt.month.unique())
        meses_nombres = [MESES[m] for m in meses_numeros]

        with col_f2:
            mes_nombre = st.selectbox("Mes", ["TODOS"] + meses_nombres)

        mes_numero = MESES_INVERSO.get(mes_nombre, "TODOS")

        if mes_numero != "TODOS":
            temp_fechas = temp_fechas[temp_fechas["fecha"].dt.month == mes_numero]

        semanas_disponibles = sorted(temp_fechas["fecha"].apply(semana_del_mes).dropna().unique())
        semanas_opciones = [f"Semana {int(s)}" for s in semanas_disponibles]

        with col_f3:
            semana_nombre = st.selectbox("Semana del mes", ["TODAS"] + semanas_opciones)

        semana_numero = "TODAS"
        if semana_nombre != "TODAS":
            semana_numero = int(semana_nombre.replace("Semana ", ""))

        if semana_numero != "TODAS":
            temp_fechas = temp_fechas[temp_fechas["fecha"].apply(semana_del_mes) == semana_numero]

        dias_disponibles = sorted(temp_fechas["fecha"].dt.day.unique())
        with col_f4:
            dia = st.selectbox("Día", ["TODOS"] + dias_disponibles)

        marcas_disponibles = sorted(ventas_dash["marca"].dropna().replace("", pd.NA).dropna().unique())
        with col_f5:
            marca_filtro = st.selectbox("marca", ["TODAS"] + marcas_disponibles)

        ventas_filtradas = ventas_dash.copy()

        if año != "TODOS":
            ventas_filtradas = ventas_filtradas[ventas_filtradas["fecha"].dt.year == año]
        if mes_numero != "TODOS":
            ventas_filtradas = ventas_filtradas[ventas_filtradas["fecha"].dt.month == mes_numero]
        if semana_numero != "TODAS":
            ventas_filtradas = ventas_filtradas[ventas_filtradas["semana_mes"] == semana_numero]
        if dia != "TODOS":
            ventas_filtradas = ventas_filtradas[ventas_filtradas["fecha"].dt.day == dia]
        if marca_filtro != "TODAS":
            ventas_filtradas = ventas_filtradas[ventas_filtradas["marca"] == marca_filtro]

        ventas_equipos = ventas_filtradas[
            (ventas_filtradas["marca"].fillna("") != "") &
            (ventas_filtradas["cantidad"] > 0)
        ]

        st.divider()

        c1, c2, c3 = st.columns(3)
        c1.metric("Órdenes", ventas_filtradas["orden"].nunique())
        c2.metric("Equipos vendidos", int(ventas_equipos["cantidad"].sum()))
        c3.metric("Accesorios vendidos", int(ventas_filtradas["cantidad_accesorio"].sum()))

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🏆 Ranking de Marcas")
            if ventas_equipos.empty:
                st.info("No hay ventas de equipos para este filtro.")
            else:
                ranking_marca = (
                    ventas_equipos.groupby("marca")["cantidad"]
                    .sum()
                    .sort_values(ascending=False)
                    .reset_index()
                )
                ranking_marca.columns = ["marca", "Total"]
                st.dataframe(ranking_marca.astype(str), use_container_width=True)
                st.bar_chart(ranking_marca.set_index("marca"))

        with col2:
            st.subheader("🥧 Participación de Marcas")
            if ventas_equipos.empty:
                st.info("No hay datos para participación.")
            else:
                pie_data = ventas_equipos.groupby("marca")["cantidad"].sum().sort_values(ascending=False)
                colores = [COLORES_MARCA.get(str(marca).upper(), "#95A5A6") for marca in pie_data.index]
                colores_sombra = [oscurecer_color(c, 0.50) for c in colores]

                fig, ax = plt.subplots(figsize=(7, 4), facecolor="#0E1117")
                ax.set_facecolor("#0E1117")

                for i in range(10, 0, -1):
                    ax.pie(
                        pie_data.values,
                        radius=1.0,
                        colors=colores_sombra,
                        startangle=90,
                        center=(0, -0.025 * i),
                        wedgeprops={"linewidth": 0, "edgecolor": "none"}
                    )

                ax.pie(
                    pie_data.values,
                    labels=pie_data.index,
                    autopct="%1.1f%%",
                    startangle=90,
                    colors=colores,
                    shadow=True,
                    explode=[0.03] * len(pie_data),
                    pctdistance=0.72,
                    labeldistance=1.15,
                    center=(0, 0),
                    textprops={"color": "white", "fontsize": 9, "fontweight": "bold"},
                    wedgeprops={"linewidth": 0.8, "edgecolor": "#222222"}
                )

                ax.set_aspect(0.55)
                ax.set_xlim(-1.55, 1.55)
                ax.set_ylim(-1.05, 1.20)
                ax.axis("off")
                st.pyplot(fig)

        st.divider()

        st.subheader("🏅 Top vendedores por marca")
        if ventas_equipos.empty:
            st.info("No hay datos suficientes.")
        else:
            top_base = (
                ventas_equipos.groupby(["marca", "vendedor"])["cantidad"]
                .sum()
                .reset_index()
                .sort_values(["marca", "cantidad"], ascending=[True, False])
            )

            top_base["puesto"] = (
                top_base.groupby("marca")["cantidad"]
                .rank(method="first", ascending=False)
                .astype(int)
            )
            top_base["texto"] = top_base.apply(texto_top_vendedor, axis=1)
            top_filtrado = top_base[top_base["puesto"] <= 4]

            tabla_top = top_filtrado.pivot(index="marca", columns="puesto", values="texto").reset_index()
            for n in range(1, 5):
                if n not in tabla_top.columns:
                    tabla_top[n] = ""

            tabla_top = tabla_top.rename(columns={
                "marca": "MARCAS",
                1: "🥇 VENDEDOR TOP 1",
                2: "🥈 VENDEDOR TOP 2",
                3: "🥉 VENDEDOR TOP 3",
                4: "🏅 VENDEDOR TOP 4",
            })

            totales_marca = (
                ventas_equipos.groupby("marca")["cantidad"]
                .sum()
                .reset_index()
                .rename(columns={"marca": "MARCAS", "cantidad": "TOTAL"})
            )

            tabla_top = tabla_top.merge(totales_marca, on="MARCAS", how="left")
            tabla_top = tabla_top.sort_values("TOTAL", ascending=False)

            columnas_top = [
                "MARCAS", "🥇 VENDEDOR TOP 1", "🥈 VENDEDOR TOP 2",
                "🥉 VENDEDOR TOP 3", "🏅 VENDEDOR TOP 4", "TOTAL"
            ]
            tabla_top = tabla_top[columnas_top].fillna("")
            st.dataframe(tabla_top.astype(str), use_container_width=True)

        st.divider()

        col3, col4 = st.columns(2)

        with col3:
            st.subheader("📱 Ranking de Modelos")
            if ventas_equipos.empty:
                st.info("No hay modelos vendidos para este filtro.")
            else:
                ranking_modelo = (
                    ventas_equipos.groupby("modelo")["cantidad"]
                    .sum()
                    .sort_values(ascending=False)
                    .reset_index()
                )
                ranking_modelo.columns = ["modelo", "Cantidad"]
                st.dataframe(ranking_modelo.astype(str), use_container_width=True)
                st.bar_chart(ranking_modelo.set_index("modelo"))

        with col4:
            st.subheader("📅 Ventas por Día")
            if ventas_equipos.empty:
                st.info("No hay ventas por día para este filtro.")
            else:
                ventas_dia = (
                    ventas_equipos.groupby(ventas_equipos["fecha"].dt.date)["cantidad"]
                    .sum()
                    .reset_index()
                )
                ventas_dia.columns = ["Fecha", "Ventas"]
                st.dataframe(ventas_dia.astype(str), use_container_width=True)
                st.line_chart(ventas_dia.set_index("Fecha"))

        st.divider()
        st.subheader("Últimas órdenes del filtro")
        ultimas_ordenes = ventas_filtradas.drop(columns=["semana_mes"], errors="ignore").tail(30).copy()
        ultimas_ordenes = preparar_fecha_hora(ultimas_ordenes)
        ultimas_ordenes = ordenar_columnas_existentes(
            ultimas_ordenes,
            ["fecha", "hora", "vendedor", "orden", "imei", "chip", "marca", "modelo", "color", "tipo"]
        )
        ultimas_ordenes = ultimas_ordenes.replace({"None": "", "nan": "", "NaN": ""})
        st.dataframe(ultimas_ordenes.astype(str), use_container_width=True)

# =========================
# INVENTARIO
# =========================
elif menu == "📦 Inventario":
    st.title("📦 Inventario")
    st.markdown("""
    <div class="glass-primary">
        <h3>📦 Inventario vivo</h3>
        <p>Stock inicial, ingresos, salidas, traslados y disponibilidad.</p>
    </div>
    """, unsafe_allow_html=True)

    opcion_inv = st.radio(
        "Elige una opción",
        [
            "📊 Ver Stock Actual",
            "➕ Ingresar Stock",
            "📥 Ingreso Mercadería",
            "📤 Salida Traslado",
            "📋 Historial Movimientos"
        ],
        horizontal=True
    )

    if opcion_inv == "📊 Ver Stock Actual":
        st.subheader("📊 Stock Actual")

        stock_vista = stock_actual_df.copy()
        stock_vista["stock_actual"] = pd.to_numeric(stock_vista["stock_actual"], errors="coerce").fillna(0).astype(int)

        col1, col2, col3 = st.columns(3)
        marcas_stock = sorted(stock_vista["marca"].dropna().unique())
        marca_stock = col1.selectbox("Filtrar marca", ["TODAS"] + marcas_stock)
        solo_con_stock = col2.checkbox("Mostrar solo con stock", value=False)
        texto_buscar = col3.text_input("Buscar modelo / SKU / color")

        if marca_stock != "TODAS":
            stock_vista = stock_vista[stock_vista["marca"] == marca_stock]

        if solo_con_stock:
            stock_vista = stock_vista[stock_vista["stock_actual"] > 0]

        if texto_buscar.strip():
            t = texto_buscar.strip().lower()
            stock_vista = stock_vista[
                stock_vista["modelo"].str.lower().str.contains(t, na=False) |
                stock_vista["sku"].str.lower().str.contains(t, na=False) |
                stock_vista["color"].str.lower().str.contains(t, na=False)
            ]

        mostrar_cols = ["marca", "sku", "modelo", "color", "tipo", "stock_actual"]
        st.dataframe(stock_vista[mostrar_cols].astype(str), use_container_width=True)

    elif opcion_inv == "➕ Ingresar Stock":
        st.info("Usa esta opción para cargar tu stock inicial por primera vez.")
        registrar_movimiento_stock("STOCK INICIAL", requiere_jefe=False)

    elif opcion_inv == "📥 Ingreso Mercadería":
        tipo_ingreso = st.selectbox("Tipo de ingreso", ["INGRESO", "TRASLADO INGRESO"])
        requiere_jefe = tipo_ingreso == "TRASLADO INGRESO"
        registrar_movimiento_stock(tipo_ingreso, requiere_jefe=requiere_jefe)

    elif opcion_inv == "📤 Salida Traslado":
        tipo_salida = st.selectbox("Tipo de salida", ["TRASLADO SALIDA", "SALIDA"])
        requiere_jefe = tipo_salida == "TRASLADO SALIDA"
        registrar_movimiento_stock(tipo_salida, requiere_jefe=requiere_jefe)

    elif opcion_inv == "📋 Historial Movimientos":
        st.subheader("📋 Historial de movimientos de stock")
        mov_vista = movimientos_stock.copy()
        mov_vista = preparar_fecha_hora(mov_vista)
        mov_vista = ordenar_columnas_existentes(
            mov_vista,
            ["fecha", "hora", "tipo_movimiento", "sku", "cantidad", "jefe_solicita", "vendedor_responsable", "detalle"]
        )
        st.dataframe(mov_vista.astype(str), use_container_width=True)

# =========================
# CATÁLOGOS
# =========================
elif menu == "📱 Catálogo Equipos":
    st.title("📱 Catálogo Equipos")
    st.dataframe(productos.astype(str), use_container_width=True)

elif menu == "🎧 Catálogo Accesorios":
    st.title("🎧 Catálogo Accesorios")
    st.dataframe(accesorios.astype(str), use_container_width=True)


elif menu == "➕ Nuevo Equipo":
    st.title("➕ Nuevo Equipo")
    st.markdown("""
    <div class="glass-primary">
        <h3>📱 Agregar modelo al catálogo</h3>
        <p>Este producto aparecerá para stock, ventas e inventario.</p>
    </div>
    """, unsafe_allow_html=True)

    nueva_marca = st.text_input("marca").strip().upper()
    nuevo_sku = st.text_input("SKU").strip().upper()
    nuevo_modelo = st.text_input("modelo").strip().upper()
    nuevo_color = st.text_input("color").strip().upper()
    nuevo_tipo = st.selectbox("tipo", ["SOLO", "PACK"])

    if st.button("Guardar nuevo equipo"):
        if not nueva_marca or not nuevo_sku or not nuevo_modelo or not nuevo_color:
            st.error("Completa Marca, SKU, Modelo y Color.")
        elif nuevo_sku in productos["sku"].astype(str).str.strip().values:
            st.error("Ese SKU ya existe en el catálogo.")
        else:
            nuevo_producto = pd.DataFrame([{
                "marca": nueva_marca,
                "sku": nuevo_sku,
                "modelo": nuevo_modelo,
                "color": nuevo_color,
                "tipo": nuevo_tipo
            }])
            registro = nuevo_producto.iloc[0].to_dict()
            insertar_registro("productos", registro)
            st.success("Nuevo equipo agregado correctamente ✅")
            mostrar_confeti()
            st.info("Ahora ve a Inventario → Ingresar Stock para cargar unidades.")
            st.rerun()

elif menu == "➕ Nuevo Accesorio":
    st.title("➕ Nuevo Accesorio")
    st.markdown("""
    <div class="glass-primary">
        <h3>🎧 Agregar accesorio al catálogo</h3>
        <p>Este accesorio aparecerá al registrar órdenes.</p>
    </div>
    """, unsafe_allow_html=True)

    marca_acc_nueva = st.text_input("Marca accesorio").strip().upper()
    sku_acc_nuevo = st.text_input("SKU accesorio").strip().upper()
    desc_acc_nueva = st.text_input("Descripción").strip().upper()

    if st.button("Guardar nuevo accesorio"):
        if not marca_acc_nueva or not sku_acc_nuevo or not desc_acc_nueva:
            st.error("Completa Marca, SKU y Descripción.")
        elif sku_acc_nuevo in accesorios["sku"].astype(str).str.strip().values:
            st.error("Ese SKU de accesorio ya existe.")
        else:
            nuevo_accesorio = pd.DataFrame([{
                "MARCA": marca_acc_nueva,
                "SKU": sku_acc_nuevo,
                "DESCRIPCION": desc_acc_nueva
            }])
            accesorios_actualizados = pd.concat([accesorios, nuevo_accesorio], ignore_index=True)
            accesorios_actualizados = accesorios_actualizados.sort_values(["MARCA", "DESCRIPCION"])
            accesorios_actualizados.to_csv("data/catalogo_accesorios.csv", sep="\t", index=False)
            st.success("Nuevo accesorio agregado correctamente ✅")
            mostrar_confeti()

elif menu == "🧑‍💼 Vendedores":
    st.title("🧑‍💼 Vendedores")

    if st.session_state.get("rol") == "admin":
        tab_vendedores, tab_nuevo = st.tabs(["📋 Lista", "➕ Nuevo vendedor / usuario"])

        with tab_vendedores:
            st.dataframe(vendedores.astype(str), use_container_width=True)

        with tab_nuevo:
            st.subheader("➕ Crear vendedor y usuario")
            st.info("Esto crea al vendedor y también su acceso de login.")

            nuevo_nombre = st.text_input("Nombre del vendedor").strip().upper()
            nuevo_usuario = st.text_input("Usuario").strip().upper()
            nueva_password = st.text_input("Contraseña inicial", type="password").strip()
            nuevo_rol = st.selectbox("Rol", ["vendedor", "admin"])
            nuevo_estado = st.selectbox("Estado", ["ACTIVO", "INACTIVO"])

            if st.button("Crear vendedor / usuario"):
                if not nuevo_nombre or not nuevo_usuario or not nueva_password:
                    st.error("Completa nombre, usuario y contraseña.")
                else:
                    existe_vendedor = nuevo_nombre in vendedores["nombre"].astype(str).str.upper().values
                    existe_usuario = nuevo_usuario in usuarios["usuario"].astype(str).str.upper().values if not usuarios.empty else False

                    if existe_usuario:
                        st.error("Ese usuario ya existe.")
                    else:
                        if not existe_vendedor:
                            insertar_registro("vendedores", {
                                "nombre": nuevo_nombre,
                                "estado": nuevo_estado
                            })

                        insertar_registro("usuarios", {
                            "usuario": nuevo_usuario,
                            "password": nueva_password,
                            "rol": nuevo_rol,
                            "vendedor": nuevo_nombre,
                            "estado": nuevo_estado
                        })

                        st.success("Vendedor / usuario creado correctamente ✅")
                        st.rerun()
    else:
        st.warning("Solo el administrador puede ver y crear vendedores.")

# =========================
# REGISTRAR ORDEN
# =========================
elif menu == "🧾 Registrar Orden":
    st.title("🧾 Registrar Orden")
    st.markdown("""
    <div class="glass-primary">
        <h3>🧾 Registro rápido</h3>
        <p>Registra chip, equipo y accesorio desde una sola orden.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get("guardado_ok", False):
        st.success("Orden guardada correctamente ✅ Ya puedes registrar otra.")
        mostrar_confeti()
        st.session_state["guardado_ok"] = False

    version = st.session_state["form_version"]
    vendedores_activos = vendedores[vendedores["estado"] == "ACTIVO"]["nombre"]

    fecha = st.date_input("Fecha", key=f"fecha_{version}")

    if st.session_state.get("rol") == "admin":
        vendedor = st.selectbox("Vendedor", vendedores_activos, key=f"vendedor_{version}")
    else:
        vendedor = st.session_state.get("vendedor", "")
        st.text_input("Vendedor", vendedor, disabled=True, key=f"vendedor_{version}")
    orden = st.text_input("Número de Orden", key=f"orden_{version}")

    st.subheader("¿Qué incluye la orden?")
    col1, col2, col3 = st.columns(3)
    incluye_chip = col1.checkbox("Chip", key=f"incluye_chip_{version}")
    incluye_equipo = col2.checkbox("Equipo", key=f"incluye_equipo_{version}")
    incluye_accesorio = col3.checkbox("Accesorio", key=f"incluye_accesorio_{version}")

    chip = ""
    tipo_chip = ""
    imei = ""
    sku = ""
    marca = ""
    modelo = ""
    color = ""
    tipo = ""
    accesorio_sku = ""
    accesorio_desc = ""
    cantidad_accesorio = 0

    if incluye_chip:
        st.subheader("📶 Datos del Chip")
        tipo_chip = st.selectbox("Tipo de chip", ["PREPAGO", "POSPAGO"], key=f"tipo_chip_{version}")
        chip = st.text_input("Número de chip", key=f"chip_{version}")

    if incluye_equipo:
        st.subheader("📱 Datos del Equipo")

        productos_disponibles = stock_actual_df[pd.to_numeric(stock_actual_df["stock_actual"], errors="coerce").fillna(0) > 0].copy()

        if productos_disponibles.empty:
            st.error("No hay equipos con stock disponible. Primero ingresa stock en Inventario.")
        else:
            producto, producto_df = seleccionar_producto(productos_disponibles, prefijo=f"venta_{version}")
            sku = producto["sku"]
            marca = producto["marca"]
            modelo = producto["modelo"]
            color = producto["color"]
            tipo = producto["tipo"]
            stock_disponible = int(pd.to_numeric(producto["stock_actual"], errors="coerce"))

            imei = st.text_input("IMEI", key=f"imei_{version}")

            st.write(f"Stock disponible: **{stock_disponible}**")
            st.write("Producto seleccionado:")
            st.dataframe(producto_df.astype(str), use_container_width=True)

    if incluye_accesorio:
        st.subheader("🎧 Datos del Accesorio")

        marca_acc = st.selectbox("Marca accesorio", sorted(accesorios["marca"].dropna().unique()), key=f"marca_acc_{version}")
        accesorios_filtrados = accesorios[accesorios["marca"] == marca_acc]

        accesorio_desc = st.selectbox(
            "Accesorio",
            sorted(accesorios_filtrados["descripcion"].dropna().unique()),
            key=f"accesorio_{version}"
        )

        acc_resultado = accesorios_filtrados[
            accesorios_filtrados["descripcion"] == accesorio_desc
        ]

        accesorio_sku = acc_resultado.iloc[0]["sku"]
        cantidad_accesorio = 1

        st.write("Accesorio seleccionado:")
        st.dataframe(acc_resultado.astype(str), use_container_width=True)

    if st.button("Guardar Orden", key=f"guardar_{version}"):
        orden_limpia = orden.strip()

        if orden_limpia == "":
            st.error("Debes ingresar el número de orden.")
        elif orden_limpia in ventas["orden"].astype(str).str.strip().values:
            st.error("Esa orden ya está registrada. No se puede duplicar.")
        elif not incluye_chip and not incluye_equipo and not incluye_accesorio:
            st.error("Debes seleccionar al menos Chip, Equipo o Accesorio.")
        elif incluye_equipo and sku == "":
            st.error("No se seleccionó equipo válido.")
        elif incluye_equipo and imei.strip() == "":
            st.error("Debes ingresar el IMEI del equipo.")
        elif incluye_chip and chip.strip() == "":
            st.error("Debes ingresar el número de chip.")
        else:
            nueva_venta = pd.DataFrame([{
                "fecha": fecha.strftime("%Y-%m-%d"),
                "vendedor": vendedor,
                "orden": orden_limpia,
                "chip": chip.strip(),
                "tipo_chip": tipo_chip,
                "imei": imei.strip(),
                "sku": sku,
                "marca": marca,
                "modelo": modelo,
                "color": color,
                "tipo": tipo,
                "cantidad": 1 if incluye_equipo else 0,
                "accesorio_sku": accesorio_sku,
                "accesorio": accesorio_desc,
                "cantidad_accesorio": cantidad_accesorio if incluye_accesorio else 0
            }])

            registro = nueva_venta.iloc[0].to_dict()
            registro["cantidad"] = int(registro.get("cantidad", 0) or 0)
            registro["cantidad_accesorio"] = int(registro.get("cantidad_accesorio", 0) or 0)
            insertar_registro("ventas", registro)

            st.session_state["guardado_ok"] = True
            st.session_state["form_version"] += 1
            st.rerun()

# =========================
# VENTAS REGISTRADAS
# =========================
elif menu == "📋 Ventas Registradas":
    st.title("📋 Ventas Registradas")

    if ventas.empty:
        st.info("No hay ventas registradas.")
    else:
        ventas_limpias = ventas.copy().replace({"None": "", "nan": "", "NaN": ""})
        ventas_limpias = preparar_fecha_hora(ventas_limpias)
        ventas_limpias = ordenar_columnas_existentes(
            ventas_limpias,
            [
                "fecha", "hora", "vendedor", "orden", "imei",
                "marca", "modelo", "color", "tipo",
                "chip", "tipo_chip", "accesorio", "cantidad", "cantidad_accesorio"
            ]
        )
        st.dataframe(ventas_limpias.astype(str), use_container_width=True)

        st.subheader("🗑 Eliminar venta")

        ventas_para_borrar = ventas.copy()
        ventas_para_borrar["orden"] = ventas_para_borrar["orden"].astype(str)

        ordenes_disponibles = sorted(
            [o for o in ventas_para_borrar["orden"].dropna().unique() if o.strip() != ""]
        )

        if not ordenes_disponibles:
            st.info("No hay órdenes disponibles para eliminar.")
        else:
            orden_eliminar = st.selectbox(
                "Selecciona la orden que quieres eliminar",
                ordenes_disponibles
            )

            venta_seleccionada = ventas_para_borrar[
                ventas_para_borrar["orden"].astype(str) == str(orden_eliminar)
            ]

            st.warning("Revisa bien antes de eliminar. Esta acción borra la venta seleccionada de Supabase.")
            venta_preview = preparar_fecha_hora(venta_seleccionada.copy())
            st.dataframe(venta_preview.astype(str), use_container_width=True)

            confirmar = st.checkbox("Confirmo que quiero eliminar esta orden")

            if st.button("Eliminar venta"):
                if not confirmar:
                    st.error("Primero marca la confirmación para evitar borrar por error.")
                else:
                    if "id" in venta_seleccionada.columns and str(venta_seleccionada.iloc[0].get("id", "")).strip() != "":
                        venta_id = venta_seleccionada.iloc[0]["id"]
                        eliminar_registro("ventas", venta_id)
                    else:
                        supabase.table("ventas").delete().eq("orden", orden_eliminar).execute()

                    st.success("Venta eliminada correctamente ✅")
                    st.rerun()

elif menu == "📱 Buscar IMEI":
    st.title("📱 Buscar IMEI por Marca y Fecha")

    if ventas.empty:
        st.info("No hay ventas registradas.")
    else:
        ventas_imei_base = ventas.copy()
        ventas_imei_base["fecha_dt"] = pd.to_datetime(ventas_imei_base["fecha"], errors="coerce")
        ventas_imei_base["cantidad"] = pd.to_numeric(ventas_imei_base["cantidad"], errors="coerce").fillna(0).astype(int)

        st.markdown("""
        <div class="glass-primary">
            <h3>📲 Reporte para promotores</h3>
            <p>Filtra por rango de fechas y marca para obtener orden e IMEI de equipos vendidos.</p>
        </div>
        """, unsafe_allow_html=True)

        fechas_validas = ventas_imei_base["fecha_dt"].dropna()
        if not fechas_validas.empty:
            fecha_min = fechas_validas.min().date()
            fecha_max = fechas_validas.max().date()
        else:
            fecha_min = pd.Timestamp.today().date()
            fecha_max = pd.Timestamp.today().date()

        c1, c2, c3 = st.columns(3)
        fecha_desde = c1.date_input("Fecha inicio", value=fecha_min)
        fecha_hasta = c2.date_input("Fecha fin", value=fecha_max)

        marcas = sorted([m for m in ventas_imei_base["marca"].astype(str).unique() if m.strip() != ""])
        marca_sel = c3.selectbox("Marca", ["TODAS"] + marcas)

        resultado_imei = ventas_imei_base[
            (ventas_imei_base["fecha_dt"].dt.date >= fecha_desde) &
            (ventas_imei_base["fecha_dt"].dt.date <= fecha_hasta) &
            (ventas_imei_base["cantidad"] > 0)
        ]

        if marca_sel != "TODAS":
            resultado_imei = resultado_imei[resultado_imei["marca"] == marca_sel]

        resultado_imei = resultado_imei.sort_values(["fecha_dt", "marca", "modelo", "vendedor", "orden"])

        st.divider()

        m1, m2 = st.columns(2)
        m1.metric("Órdenes encontradas", resultado_imei["orden"].nunique())
        m2.metric("Equipos vendidos", int(resultado_imei["cantidad"].sum()))

        vista_imei = resultado_imei.drop(columns=["fecha_dt"], errors="ignore").copy()
        vista_imei = preparar_fecha_hora(vista_imei)
        vista_imei = ordenar_columnas_existentes(
            vista_imei,
            ["fecha", "hora", "marca", "modelo", "color", "tipo", "vendedor", "orden", "imei"]
        )
        vista_imei = vista_imei[
            [c for c in ["fecha", "hora", "marca", "modelo", "color", "tipo", "vendedor", "orden", "imei"] if c in vista_imei.columns]
        ]
        vista_imei = vista_imei.replace({"None": "", "nan": "", "NaN": ""})

        st.dataframe(vista_imei.astype(str), use_container_width=True)

        csv_imei = vista_imei.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "📥 Descargar reporte IMEI",
            data=csv_imei,
            file_name="reporte_imei_por_marca_fecha.csv",
            mime="text/csv"
        )

# =========================
# EDITAR VENTA
# =========================


elif menu == "✏️ Editar Venta":
    st.title("✏️ Editar Venta")

    if ventas.empty or ventas["orden"].fillna("").eq("").all():
        st.info("No hay ventas para editar.")
    else:
        ordenes = ventas["orden"].astype(str).dropna().unique()
        orden_editar = st.selectbox("Selecciona la orden", sorted(ordenes))

        idx = ventas[ventas["orden"].astype(str) == str(orden_editar)].index[0]
        venta = ventas.loc[idx].copy()

        st.subheader("Datos actuales")
        st.dataframe(pd.DataFrame([venta]).astype(str), use_container_width=True)

        st.subheader("Editar datos permitidos")

        nueva_orden = st.text_input("Orden", value=str(venta.get("orden", "")))
        nuevo_chip = st.text_input("Chip", value=str(venta.get("chip", "")))

        tipo_chip_actual = str(venta.get("tipo_chip", ""))
        opciones_chip = ["", "PREPAGO", "POSPAGO"]
        if tipo_chip_actual not in opciones_chip:
            tipo_chip_actual = ""
        nuevo_tipo_chip = st.selectbox(
            "Tipo de chip",
            opciones_chip,
            index=opciones_chip.index(tipo_chip_actual)
        )

        nuevo_imei = st.text_input("IMEI", value=str(venta.get("imei", "")))

        tiene_equipo = str(venta.get("marca", "")) != ""

        nueva_marca = str(venta.get("marca", ""))
        nuevo_modelo = str(venta.get("modelo", ""))
        nuevo_color = str(venta.get("color", ""))
        nuevo_tipo = str(venta.get("tipo", ""))
        nuevo_sku = str(venta.get("sku", ""))

        if tiene_equipo:
            st.subheader("Editar equipo con selectores seguros")
            producto, producto_df = seleccionar_producto(
                productos,
                prefijo=f"editar_{idx}",
                default_marca=nueva_marca,
                default_modelo=nuevo_modelo,
                default_color=nuevo_color,
                default_tipo=nuevo_tipo
            )
            nuevo_sku = producto["sku"]
            nueva_marca = producto["marca"]
            nuevo_modelo = producto["modelo"]
            nuevo_color = producto["color"]
            nuevo_tipo = producto["tipo"]

            st.write("Nuevo producto seleccionado:")
            st.dataframe(producto_df.astype(str), use_container_width=True)

        if st.button("Guardar edición"):
            nueva_orden_limpia = nueva_orden.strip()
            ordenes_existentes = ventas.drop(index=idx)["orden"].astype(str).str.strip().values

            if nueva_orden_limpia == "":
                st.error("La orden no puede quedar vacía.")
            elif nueva_orden_limpia in ordenes_existentes:
                st.error("Esa orden ya existe en otra venta.")
            else:
                ventas.loc[idx, "orden"] = nueva_orden_limpia
                ventas.loc[idx, "chip"] = nuevo_chip.strip()
                ventas.loc[idx, "tipo_chip"] = nuevo_tipo_chip
                ventas.loc[idx, "imei"] = nuevo_imei.strip()

                if tiene_equipo:
                    ventas.loc[idx, "sku"] = nuevo_sku
                    ventas.loc[idx, "marca"] = nueva_marca
                    ventas.loc[idx, "modelo"] = nuevo_modelo
                    ventas.loc[idx, "color"] = nuevo_color
                    ventas.loc[idx, "tipo"] = nuevo_tipo

                venta_id = ventas.loc[idx, "id"]
                cambios = {
                    "orden": nueva_orden_limpia,
                    "chip": nuevo_chip.strip(),
                    "tipo_chip": nuevo_tipo_chip,
                    "imei": nuevo_imei.strip(),
                }
                if tiene_equipo:
                    cambios.update({
                        "sku": nuevo_sku,
                        "marca": nueva_marca,
                        "modelo": nuevo_modelo,
                        "color": nuevo_color,
                        "tipo": nuevo_tipo,
                    })
                actualizar_registro("ventas", venta_id, cambios)
                st.success("Venta editada correctamente ✅")
                st.rerun()

# =========================
# BUSCAR
# =========================
elif menu == "🔍 Buscar":
    st.title("🔍 Buscar Orden / IMEI / CHIP / Accesorio / Vendedor")

    if ventas.empty:
        st.info("No hay ventas registradas.")
    else:
        opcion = st.selectbox(
            "Buscar por",
            ["ORDEN", "IMEI", "CHIP", "ACCESORIO", "REPORTE VENDEDOR"]
        )

        # ================= BUSQUEDAS NORMALES =================
        if opcion in ["ORDEN", "IMEI", "CHIP", "ACCESORIO"]:
            texto = st.text_input("Escribe lo que quieres buscar").strip()

            if texto:
                ventas_busqueda = ventas.astype(str)

                if opcion == "ORDEN":
                    resultado = ventas_busqueda[
                        ventas_busqueda["orden"].str.contains(texto, case=False, na=False)
                    ]
                elif opcion == "IMEI":
                    resultado = ventas_busqueda[
                        ventas_busqueda["imei"].str.contains(texto, case=False, na=False)
                    ]
                elif opcion == "CHIP":
                    resultado = ventas_busqueda[
                        ventas_busqueda["chip"].str.contains(texto, case=False, na=False)
                    ]
                else:
                    resultado = ventas_busqueda[
                        ventas_busqueda["accesorio"].str.contains(texto, case=False, na=False) |
                        ventas_busqueda["accesorio_sku"].str.contains(texto, case=False, na=False)
                    ]

                if resultado.empty:
                    st.warning("No se encontraron resultados.")
                else:
                    st.success(f"Se encontraron {len(resultado)} resultado(s).")
                    resultado = resultado.replace({"None": "", "nan": "", "NaN": ""})
                    st.dataframe(resultado, use_container_width=True)

        # ================= REPORTE POR VENDEDOR =================
        if opcion == "REPORTE VENDEDOR":
            st.subheader("📊 Reporte por vendedor")

            ventas_rep = ventas.copy()
            ventas_rep["fecha_dt"] = pd.to_datetime(ventas_rep["fecha"], errors="coerce")

            fechas_validas = ventas_rep["fecha_dt"].dropna()
            if not fechas_validas.empty:
                fecha_min = fechas_validas.min().date()
                fecha_max = fechas_validas.max().date()
            else:
                fecha_min = pd.Timestamp.today().date()
                fecha_max = pd.Timestamp.today().date()

            vendedores_lista = sorted([
                v for v in ventas_rep["vendedor"].astype(str).unique()
                if v.strip() != ""
            ])

            if not vendedores_lista:
                st.warning("No hay vendedores registrados en ventas.")
            else:
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    fecha_inicio = st.date_input("Desde", value=fecha_min, key="reporte_vendedor_desde")

                with col2:
                    fecha_fin = st.date_input("Hasta", value=fecha_max, key="reporte_vendedor_hasta")

                with col3:
                    vendedor_sel = st.selectbox("Vendedor", vendedores_lista, key="reporte_vendedor_nombre")

                with col4:
                    tipo_reporte = st.selectbox("Tipo", ["EQUIPO", "ACCESORIO"], key="reporte_vendedor_tipo")

                resultado = ventas_rep[
                    (ventas_rep["fecha_dt"].dt.date >= fecha_inicio) &
                    (ventas_rep["fecha_dt"].dt.date <= fecha_fin) &
                    (ventas_rep["vendedor"].astype(str) == str(vendedor_sel))
                ].copy()

                if tipo_reporte == "EQUIPO":
                    resultado["cantidad"] = pd.to_numeric(
                        resultado["cantidad"], errors="coerce"
                    ).fillna(0).astype(int)
                    resultado = resultado[resultado["cantidad"] > 0]

                    columnas = [
                        "fecha", "hora", "vendedor", "orden", "imei",
                        "marca", "modelo", "color", "tipo", "cantidad"
                    ]
                    nombre_archivo = f"reporte_equipos_{vendedor_sel}.csv"
                else:
                    resultado["cantidad_accesorio"] = pd.to_numeric(
                        resultado["cantidad_accesorio"], errors="coerce"
                    ).fillna(0).astype(int)
                    resultado = resultado[resultado["cantidad_accesorio"] > 0]

                    columnas = [
                        "fecha", "hora", "vendedor", "orden",
                        "accesorio_sku", "accesorio", "cantidad_accesorio"
                    ]
                    nombre_archivo = f"reporte_accesorios_{vendedor_sel}.csv"

                st.divider()

                if resultado.empty:
                    st.warning("No hay datos con ese filtro.")
                else:
                    resultado_vista = preparar_fecha_hora(resultado)

                    for col in columnas:
                        if col not in resultado_vista.columns:
                            resultado_vista[col] = ""

                    resultado_vista = resultado_vista[columnas]
                    resultado_vista = resultado_vista.replace({"None": "", "nan": "", "NaN": ""})

                    st.success(f"{len(resultado_vista)} registros encontrados")

                    if tipo_reporte == "EQUIPO":
                        total = pd.to_numeric(resultado_vista["cantidad"], errors="coerce").fillna(0).sum()
                        st.metric("Total equipos vendidos", int(total))
                    else:
                        total = pd.to_numeric(resultado_vista["cantidad_accesorio"], errors="coerce").fillna(0).sum()
                        st.metric("Total accesorios vendidos", int(total))

                    st.dataframe(resultado_vista.astype(str), use_container_width=True)

                    csv = resultado_vista.to_csv(index=False).encode("utf-8-sig")
                    st.download_button(
                        "📥 Descargar reporte",
                        data=csv,
                        file_name=nombre_archivo,
                        mime="text/csv"
                    )
