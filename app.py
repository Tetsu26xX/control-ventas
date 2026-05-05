import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import base64
from supabase import create_client
import time
import hmac
import hashlib
from datetime import datetime
from zoneinfo import ZoneInfo

ZONA_LOCAL = ZoneInfo("America/Lima")

def ahora_local():
    return datetime.now(ZONA_LOCAL)

def fecha_hoy_local():
    return ahora_local().date()

def timestamp_hoy_local():
    return pd.Timestamp(ahora_local())

def es_jefe():
    return str(st.session_state.get("rol", "")).strip().lower() == "jefe"

st.set_page_config(page_title="Sistema Ventas", layout="wide")
st.markdown("""
<style>

/* Ocultar barra superior de Streamlit */
header {visibility: hidden;}

/* Ocultar menú */
#MainMenu {visibility: hidden;}

/* Ocultar footer */
footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

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
# LOGIN PERSISTENTE
# =========================

SESSION_SECRET = st.secrets.get("SESSION_SECRET", "control_ventas_secret")
SESSION_DURATION = 8 * 60 * 60  # 8 horas

def crear_token_sesion(usuario, rol, vendedor):
    expira = int(time.time()) + SESSION_DURATION
    payload = f"{usuario}|{rol}|{vendedor}|{expira}"

    firma = hmac.new(
        SESSION_SECRET.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

    return f"{payload}|{firma}"


def validar_token_sesion(token):
    try:
        usuario, rol, vendedor, expira, firma = token.split("|")
        payload = f"{usuario}|{rol}|{vendedor}|{expira}"

        firma_valida = hmac.new(
            SESSION_SECRET.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(firma, firma_valida):
            return False

        if int(expira) < int(time.time()):
            return False

        st.session_state["login_ok"] = True
        st.session_state["usuario"] = usuario
        st.session_state["rol"] = rol
        st.session_state["vendedor"] = vendedor

        return True

    except:
        return False

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
        <div class="login-logo">Control<span>Ventas</span>Plaza Vea-Hyo</span></div>
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
                        
                        token = crear_token_sesion(
                            st.session_state["usuario"],
                            st.session_state["rol"],
                            st.session_state["vendedor"]
                        )
                        
                        st.query_params["session"] = token
                        
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
                <div class="hero-sub">Sistema para registrar ventas, controlar stock,.</div>
                <div class="hero-sub">revisar rankings.</div>
                <div class="hero-sub">y consultar IMEI por marca y fecha.</div>
            </div>
            {mascota_html}
            <div class="feature-row">
                <div class="feature-card"><div class="feature-icon">🛒</div><div class="feature-title">Ventas</div><div class="feature-text">Registra y consulta todas tus ventas.</div></div>
                <div class="feature-card"><div class="feature-icon">📦</div><div class="feature-title">Stock</div><div class="feature-text">Controla ingresos, salidas y traslados.</div></div>
                <div class="feature-card"><div class="feature-icon">📊</div><div class="feature-title">Reportes</div><div class="feature-text">Rankings y estadísticas rápidas.</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style="
            position: fixed;
            bottom: 10px;
            left: 20px;
            font-size: 11px;
            opacity: 0.5;
            color: white;
            z-index: 9999;
        ">
            Control Ventas v1.0 · © {datetime.now().year} KeevinPR.
        </div>
        """, unsafe_allow_html=True)

if not st.session_state["login_ok"]:

    token_url = st.query_params.get("session", None)

    if token_url and validar_token_sesion(token_url):
        st.rerun()

    login()
    st.stop()

# =========================
# ENTRAR DIRECTO A INSTRUCCIONES AL INICIAR
# =========================
if "inicio_instrucciones_ok" not in st.session_state:
    st.session_state["inicio_instrucciones_ok"] = True
    st.session_state["menu_actual"] = "📌 Instrucciones"
    st.markdown("""
    <div id="noti-custom">
        📘 Revisa las instrucciones antes de registrar ventas o movimientos.
    </div>
    
    <style>
    #noti-custom {
        position: fixed;
        top: 10%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: linear-gradient(135deg, #d7f54a, #7CFF6B);
        color: #111;
        padding: 18px 28px;
        border-radius: 14px;
        font-weight: 900;
        font-size: 16px;
        z-index: 999999;
        box-shadow: 0 0 25px rgba(210,245,62,0.6), 0 20px 40px rgba(0,0,0,0.4);
        animation: fadeInOut 6s ease forwards;
    }
    
    @keyframes fadeInOut {
        0% { opacity: 0; transform: translate(-50%, -60%); }
        10% { opacity: 1; transform: translate(-50%, -50%); }
        80% { opacity: 1; }
        100% { opacity: 0; transform: translate(-50%, -40%); }
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=30, show_spinner=False)
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


def limpiar_cache_datos():
    st.cache_data.clear()


def insertar_registro(tabla, registro):
    resultado = supabase.table(tabla).insert(registro).execute()
    limpiar_cache_datos()
    return resultado


def actualizar_registro(tabla, registro_id, cambios):
    resultado = supabase.table(tabla).update(cambios).eq("id", registro_id).execute()
    limpiar_cache_datos()
    return resultado


def eliminar_registro(tabla, registro_id):
    resultado = supabase.table(tabla).delete().eq("id", registro_id).execute()
    limpiar_cache_datos()
    return resultado


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

def notificacion_flotante(mensaje):
    st.markdown(f"""
    <div id="noti-custom">
        {mensaje}
    </div>

    <style>
    #noti-custom {{
        position: fixed;
        top: 10%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: linear-gradient(135deg, #d7f54a, #7CFF6B);
        color: #111;
        padding: 18px 28px;
        border-radius: 14px;
        font-weight: 900;
        font-size: 16px;
        z-index: 999999;
        box-shadow: 0 0 25px rgba(210,245,62,0.6), 0 20px 40px rgba(0,0,0,0.4);
        animation: fadeInOut 6s ease forwards;
    }}

    @keyframes fadeInOut {{
        0% {{ opacity: 0; transform: translate(-50%, -60%); }}
        10% {{ opacity: 1; transform: translate(-50%, -50%); }}
        80% {{ opacity: 1; }}
        100% {{ opacity: 0; transform: translate(-50%, -40%); }}
    }}
    </style>
    """, unsafe_allow_html=True)

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
    es_edicion = any([default_marca, default_modelo, default_color, default_tipo])

    marca_index = marcas.index(default_marca) if default_marca in marcas else (0 if es_edicion and marcas else None)
    marca = st.selectbox(
        "Marca",
        marcas,
        index=marca_index,
        placeholder="Ingresar marca",
        key=f"{prefijo}_marca"
    )

    if marca is None:
        st.info("Selecciona una marca para continuar.")
        st.stop()

    color_marca = COLORES_MARCA.get(str(marca).upper(), "#95A5A6")
    st.markdown(
        f"<div style='background:{color_marca}; color:white; padding:8px 12px; "
        f"border-radius:10px; display:inline-block; font-weight:700;'>Marca seleccionada: {marca}</div>",
        unsafe_allow_html=True
    )

    modelos = sorted(df_productos[df_productos["marca"] == marca]["modelo"].dropna().unique())
    modelo_index = modelos.index(default_modelo) if default_modelo in modelos else (0 if es_edicion and modelos else None)
    modelo = st.selectbox(
        "Modelo",
        modelos,
        index=modelo_index,
        placeholder="Ingresar modelo",
        key=f"{prefijo}_modelo"
    )

    if modelo is None:
        st.info("Selecciona un modelo para continuar.")
        st.stop()

    colores = sorted(df_productos[
        (df_productos["marca"] == marca) &
        (df_productos["modelo"] == modelo)
    ]["color"].dropna().unique())

    color_index = colores.index(default_color) if default_color in colores else (0 if es_edicion and colores else None)
    color = st.selectbox(
        "Color",
        colores,
        index=color_index,
        placeholder="Ingresar color",
        key=f"{prefijo}_color"
    )

    if color is None:
        st.info("Selecciona un color para continuar.")
        st.stop()

    tipos = sorted(df_productos[
        (df_productos["marca"] == marca) &
        (df_productos["modelo"] == modelo) &
        (df_productos["color"] == color)
    ]["tipo"].dropna().unique())

    tipo_index = tipos.index(default_tipo) if default_tipo in tipos else (0 if es_edicion and tipos else None)
    tipo = st.selectbox(
        "Tipo",
        tipos,
        index=tipo_index,
        placeholder="Ingresar tipo",
        key=f"{prefijo}_tipo"
    )

    if tipo is None:
        st.info("Selecciona un tipo para continuar.")
        st.stop()

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

    # IMPORTANTE:
    # "fecha" es la fecha de venta/movimiento elegida en el formulario.
    # "creado_en" es la fecha y hora real en que se registró en Supabase.
    # No debemos reemplazar "fecha" usando "creado_en", porque eso rompe filtros del dashboard.
    if "fecha" in df.columns:
        df["fecha"] = pd.to_datetime(
            df["fecha"], errors="coerce"
        ).dt.strftime("%Y-%m-%d").fillna("")

    if "creado_en" in df.columns:
        dt = pd.to_datetime(df["creado_en"], errors="coerce", utc=True)
        dt_local = dt.dt.tz_convert("America/Lima")

        df["fecha_registro"] = dt_local.dt.strftime("%Y-%m-%d").fillna("")
        df["hora"] = dt_local.dt.strftime("%H:%M:%S").fillna("")

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

    fecha = st.date_input("Fecha", value=fecha_hoy_local(), key=f"{prefijo}_fecha")

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
        
        st.session_state["notificacion_flotante"] = f"📦 {tipo_movimiento.title()} guardado correctamente ✅ Ya puedes registrar otro movimiento."
        
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
        st.sidebar.success(f"👑 {vendedor_txt} · ADMIN")
    elif rol_txt == "JEFE":
        st.sidebar.success(f"👑 {vendedor_txt} · JEFE")
    else:
        st.sidebar.success(f"👤 {vendedor_txt} · VENDEDOR")
    if st.sidebar.button("Cerrar sesión"):
        
        st.query_params.clear()

        st.markdown("""
        <div style="
            position: fixed;
            inset: 0;
            z-index: 999999;
            background: rgba(5, 8, 18, 0.92);
            backdrop-filter: blur(10px);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 28px;
            font-weight: 900;
            text-shadow: 0 0 18px #7CFF6B;
        ">
            🔒 Cerrando sesión...
        </div>
        """, unsafe_allow_html=True)
    
        for key in list(st.session_state.keys()):
            del st.session_state[key]
    
        st.session_state["login_ok"] = False
    
        st.rerun()

if st.sidebar.button("🔄 Actualizar datos", use_container_width=True):
    limpiar_cache_datos()
    st.toast("Datos actualizados correctamente", icon="🔄")
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
    if not es_jefe():
        boton_menu("🧾 Registrar Orden")
    boton_menu("📌 Instrucciones")

with st.sidebar.expander("🛒 Gestión de Venta", expanded=False):
    boton_menu("🔍 Buscar")
    if not es_jefe():
        boton_menu("✏️ Editar Venta")
    boton_menu("📋 Ventas Registradas")
    boton_menu("📱 Buscar IMEI")

with st.sidebar.expander("📦 Inventario", expanded=False):
    boton_menu("📦 Inventario")

with st.sidebar.expander("🧩 Productos", expanded=False):
    boton_menu("📱 Catálogo Equipos")
    boton_menu("🎧 Catálogo Accesorios")
    if not es_jefe():
        boton_menu("➕ Nuevo Equipo")
        boton_menu("➕ Nuevo Accesorio")

if not es_jefe():
    with st.sidebar.expander("👥 Equipo", expanded=False):
        boton_menu("🧑‍💼 Vendedores")

menu = st.session_state["menu_actual"]

if es_jefe() and menu in ["🧾 Registrar Orden", "✏️ Editar Venta", "➕ Nuevo Equipo", "➕ Nuevo Accesorio", "🧑‍💼 Vendedores"]:
    st.session_state["menu_actual"] = "📊 Dashboard"
    st.rerun()

if "notificacion_flotante" in st.session_state:
    notificacion_flotante(st.session_state["notificacion_flotante"])
    del st.session_state["notificacion_flotante"]

# =========================
# DASHBOARD
# =========================
if menu == "📌 Instrucciones":
    st.title("📌 Instrucciones rápidas")

    st.markdown("""
    <div class="glass-primary">
        <h3>⚠️ Leer antes de registrar</h3>
        <p>Registra con calma. Si te equivocas, avisa o usa Editar Venta.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
    <h4>🧾 Registrar una venta</h4>
    <ul>
        <li>Entra a <b>Registrar Orden</b>.</li>
        <li>Escribe la orden correctamente.</li>
        <li>Si vendiste equipo, selecciona marca, modelo, color y tipo.</li>
        <li>Si vendiste chip, escribe el número y elige PREPAGO o POSPAGO.</li>
        <li>Si vendiste accesorio, selecciónalo y coloca la cantidad.</li>
        <li>Presiona <b>Guardar una sola vez</b>.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
    <h4>📦 Ver stock</h4>
    <ul>
        <li>Entra a <b>Inventario</b>.</li>
        <li>Usa <b>Ver Stock Actual</b>.</li>
        <li>Puedes filtrar por marca.</li>
        <li>También puedes buscar por modelo, SKU o color.</li>
        <li>Revisa la cantidad antes de vender o mover mercadería.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
    <h4>📥 Ingreso de mercadería</h4>
    <ul>
        <li>Usa <b>INGRESO</b> cuando llegó mercadería nueva.</li>
        <li>Usa <b>TRASLADO INGRESO</b> cuando recibiste mercadería de otra tienda o persona.</li>
        <li>Selecciona producto y cantidad.</li>
        <li>Si es traslado, coloca quién lo pidió o quién lo envió en el campo que corresponde.</li>
        <li>Esto <b>suma stock</b>.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
    <h4>📤 Salida o traslado</h4>
    <ul>
        <li>Usa <b>TRASLADO SALIDA</b> cuando mandas mercadería a otra tienda o persona.</li>
        <li>Usa <b>SALIDA</b> cuando el producto sale del stock por otro motivo.</li>
        <li>Selecciona producto y cantidad.</li>
        <li>Coloca quién lo pidió o el motivo en detalle.</li>
        <li>Esto <b>resta stock</b>.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
    <h4>✏️ Editar venta</h4>
    <ul>
        <li>Entra a <b>Editar Venta</b>.</li>
        <li>Filtra por fecha o busca la orden.</li>
        <li>Presiona <b>Editar</b>.</li>
        <li>Cambia solo lo que está mal.</li>
        <li>Guarda la edición.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
    <h4>🚫 Reglas importantes</h4>
    <ul>
        <li>No registres dos veces la misma orden.</li>
        <li>No inventes IMEI, chip ni cantidades.</li>
        <li>Si no estás segura, pregunta antes de guardar.</li>
        <li>Todo lo que guardas afecta ventas, stock y reportes.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

elif menu == "📊 Dashboard":

    # =========================
    # TÍTULO PRO
    # =========================
    st.markdown("""
    <div style="
        padding: 18px 20px;
        border-radius: 22px;
        background: linear-gradient(135deg, rgba(255,255,255,0.10), rgba(255,255,255,0.035));
        border: 1px solid rgba(210,245,62,0.22);
        box-shadow: 0 16px 34px rgba(0,0,0,.30), 0 0 22px rgba(210,245,62,.08);
        margin-bottom: 16px;
    ">
        <div style="font-size: 30px; font-weight: 1000; color: #F8FAFC;">
            📊 Dashboard de Ventas
        </div>
        <div style="font-size: 14px; color: #d7f54a; font-weight: 800; margin-top: 4px;">
            Panel comercial · rankings · participación · stock crítico
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "mensaje_toast" in st.session_state:
        st.toast(st.session_state["mensaje_toast"], icon="✅")
        del st.session_state["mensaje_toast"]

    mascota_dashboard = get_base64_image("assets/mascota_dashboard.png")
    if mascota_dashboard:
        st.markdown(f"""
        <div style="position: fixed; bottom: 14px; right: 24px; z-index: 999;">
            <img src="data:image/png;base64,{mascota_dashboard}" width="155">
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

        # =========================
        # CSS DASHBOARD
        # =========================
        st.markdown("""
        <style>
        .dash-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.095), rgba(255,255,255,0.035));
            border: 1px solid rgba(210,245,62,0.15);
            border-radius: 24px;
            padding: 20px;
            margin-bottom: 18px;
            box-shadow: 0 14px 30px rgba(0,0,0,.28);
            transition: all .25s ease;
        }

        .dash-card:hover {
            transform: translateY(-3px);
            border-color: rgba(210,245,62,0.55);
            box-shadow: 0 0 24px rgba(210,245,62,0.24), 0 18px 38px rgba(0,0,0,.36);
        }

        .dash-title {
            color: #F8FAFC;
            font-weight: 1000;
            font-size: 24px;
            margin-bottom: 14px;
        }

        .kpi-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.11), rgba(255,255,255,0.035));
            border: 1px solid rgba(210,245,62,0.18);
            border-radius: 24px;
            padding: 19px 18px;
            box-shadow: 0 16px 34px rgba(0,0,0,.30), 0 0 20px rgba(210,245,62,.06);
            transition: all .25s ease;
            min-height: 150px;
        }

        .kpi-card:hover {
            transform: translateY(-4px);
            border-color: rgba(210,245,62,.65);
            box-shadow: 0 0 26px rgba(210,245,62,.32), 0 20px 42px rgba(0,0,0,.38);
        }

        .kpi-icon {
            font-size: 28px;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 17px;
            background: rgba(210,245,62,.15);
            box-shadow: 0 0 18px rgba(210,245,62,.15);
            margin-bottom: 12px;
        }

        .kpi-label {
            color: rgba(255,255,255,.80);
            font-size: 15px;
            font-weight: 900;
        }

        .kpi-value {
            color: #F8FAFC;
            font-size: 37px;
            font-weight: 1000;
            line-height: 1.05;
            margin-top: 5px;
        }

        .kpi-sub {
            color: #d7f54a;
            font-size: 13px;
            font-weight: 850;
            margin-top: 7px;
        }

        .alert-stock {
            background: linear-gradient(135deg, rgba(255,100,100,.16), rgba(255,255,255,.04));
            border: 1px solid rgba(255,120,120,.35);
            border-radius: 18px;
            padding: 14px 16px;
            color: #fff;
            margin: 8px 0 16px 0;
            box-shadow: 0 0 18px rgba(255,80,80,.08);
            font-size: 15px;
            font-weight: 800;
        }

        .ticker-box {
            height: 180px;
            margin-top: 18px;
            padding: 18px;
            border-radius: 20px;
            background: linear-gradient(135deg, rgba(255,255,255,0.075), rgba(255,255,255,0.025));
            border: 1px solid rgba(210,245,62,0.18);
            box-shadow: 0 0 18px rgba(210,245,62,0.08);
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .ticker-title {
            color: #F8FAFC;
            font-weight: 1000;
            font-size: 20px;
            margin-bottom: 18px;
        }

        .ticker {
            overflow: hidden;
            white-space: nowrap;
            width: 100%;
        }

        .ticker-track {
            display: inline-block;
            animation: scrollNews 38s linear infinite;
            font-size: 16px;
            font-weight: 900;
            color: #F8FAFC;
        }

        .ticker:hover .ticker-track {
            animation-play-state: paused;
        }

        .marca-news {
            display: inline !important;
            animation: none !important;
            padding-left: 0 !important;
        }

        @keyframes scrollNews {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
        </style>
        """, unsafe_allow_html=True)

        # =========================
        # FILTROS
        # =========================
        st.markdown("### 🎛️ Filtros")

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
            marca_filtro = st.selectbox("Marca", ["TODAS"] + marcas_disponibles)

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

        # =========================
        # KPIS
        # =========================
        stock_dash = stock_actual_df.copy()
        stock_dash["stock_actual"] = pd.to_numeric(
            stock_dash["stock_actual"], errors="coerce"
        ).fillna(0).astype(int)

        stock_bajo = stock_dash[
            (stock_dash["stock_actual"] > 0) &
            (stock_dash["stock_actual"] <= 2)
        ].copy()

        total_stock_bajo = len(stock_bajo)
        total_ordenes = ventas_filtradas["orden"].nunique()
        total_equipos = int(ventas_equipos["cantidad"].sum()) if not ventas_equipos.empty else 0
        total_accesorios = int(ventas_filtradas["cantidad_accesorio"].sum())

        chips_vendidos = ventas_filtradas[
            ventas_filtradas["chip"].fillna("").astype(str).str.strip() != ""
        ]["chip"].nunique()

        prepago_vendidos = ventas_filtradas[
            ventas_filtradas["tipo_chip"].fillna("").astype(str).str.upper().str.contains("PREPAGO", na=False)
        ]["chip"].nunique()

        if ventas_equipos.empty:
            marca_lider = "Sin datos"
        else:
            marca_lider = (
                ventas_equipos.groupby("marca")["cantidad"]
                .sum()
                .sort_values(ascending=False)
                .index[0]
            )

        col_k1, col_k2, col_k3, col_k4 = st.columns(4)

        with col_k1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">🧾</div>
                <div class="kpi-label">Órdenes</div>
                <div class="kpi-value">{total_ordenes}</div>
                <div class="kpi-sub">según filtro actual</div>
            </div>
            """, unsafe_allow_html=True)

        with col_k2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">📱</div>
                <div class="kpi-label">Equipos vendidos</div>
                <div class="kpi-value">{total_equipos}</div>
                <div class="kpi-sub">marca líder: {marca_lider}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_k3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">🎧</div>
                <div class="kpi-label">Accesorios vendidos</div>
                <div class="kpi-value">{total_accesorios}</div>
                <div class="kpi-sub">incluye ventas registradas</div>
            </div>
            """, unsafe_allow_html=True)

        with col_k4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">⚠️</div>
                <div class="kpi-label">Stock bajo</div>
                <div class="kpi-value">{total_stock_bajo}</div>
                <div class="kpi-sub">productos con 1 o 2 unidades</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="
            margin-top: 6px;
            margin-bottom: 12px;
            font-size: 12px;
            color: rgba(255,255,255,.55);
            font-weight: 800;
        ">
            🟢 Actualizado a las {ahora_local().strftime("%H:%M:%S")}
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style="
            display:flex;
            justify-content:space-between;
            font-size:11px;
            opacity:0.4;
            margin-top:10px;
        ">
            <span>Control Ventas v1.0</span>
            <span>© {ahora_local().year} KeevinPR.</span>
        </div>
        """, unsafe_allow_html=True)

        if total_stock_bajo > 0:
            st.markdown(f"""
            <div class="alert-stock">
                ⚠️ Tienes <b>{total_stock_bajo}</b> productos con stock bajo. Revisa inventario para evitar quedarte sin unidades.
            </div>
            """, unsafe_allow_html=True)

        # =========================
        # RANKING MARCAS + DONUT
        # =========================
        col_marca, col_participacion = st.columns([0.58, 0.42])

        with col_marca:
            st.markdown('<div class="dash-card"><div class="dash-title">📊 Ranking de marcas</div>', unsafe_allow_html=True)

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

                colores = [
                    COLORES_MARCA.get(str(m).upper(), "#95A5A6")
                    for m in ranking_marca["marca"]
                ]

                fig, ax = plt.subplots(figsize=(8, 4.2), facecolor="#15171d")
                ax.set_facecolor("#15171d")

                ax.barh(
                    ranking_marca["marca"],
                    ranking_marca["Total"],
                    color=colores,
                    edgecolor="#222222"
                )

                ax.invert_yaxis()
                ax.tick_params(colors="white", labelsize=10)
                ax.set_xlabel("Unidades vendidas", color="white", fontsize=10)

                for i, v in enumerate(ranking_marca["Total"]):
                    ax.text(v + 0.3, i, str(int(v)), color="white", va="center", fontsize=10, fontweight="bold")

                ax.grid(axis="x", alpha=0.12)
                for spine in ax.spines.values():
                    spine.set_visible(False)

                st.pyplot(fig)

                st.dataframe(
                    ranking_marca.astype(str),
                    use_container_width=True,
                    height=180
                )

            st.markdown('</div>', unsafe_allow_html=True)

        with col_participacion:
            st.markdown('<div class="dash-card"><div class="dash-title">🥧 Participación por marca</div>', unsafe_allow_html=True)

            if ventas_equipos.empty:
                st.info("No hay datos para participación.")
            else:
                pie_data = ventas_equipos.groupby("marca")["cantidad"].sum().sort_values(ascending=False)
                total_pie = pie_data.sum()

                colores = [
                    COLORES_MARCA.get(str(marca).upper(), "#95A5A6")
                    for marca in pie_data.index
                ]

                fig, ax = plt.subplots(figsize=(6.6, 5.0), facecolor="#15171d")
                ax.set_facecolor("#15171d")

                ax.pie(
                    pie_data.values,
                    radius=1.08,
                    colors=["#d7f54a"] * len(pie_data),
                    startangle=90,
                    wedgeprops={"width": 0.035, "edgecolor": "none", "alpha": 0.18}
                )

                wedges, texts, autotexts = ax.pie(
                    pie_data.values,
                    labels=None,
                    autopct="%1.1f%%",
                    startangle=90,
                    colors=colores,
                    pctdistance=0.78,
                    wedgeprops={"width": 0.42, "edgecolor": "#15171d", "linewidth": 2},
                    textprops={"color": "white", "fontsize": 10, "fontweight": "bold"}
                )

                ax.text(
                    0, 0,
                    f"{int(total_pie)}\nTotal",
                    ha="center",
                    va="center",
                    color="white",
                    fontsize=17,
                    fontweight="bold"
                )

                leyenda = [
                    f"{marca} - {valor / total_pie * 100:.1f}%"
                    for marca, valor in pie_data.items()
                ]

                ax.legend(
                    wedges,
                    leyenda,
                    loc="center left",
                    bbox_to_anchor=(1, 0.5),
                    frameon=False,
                    labelcolor="white",
                    fontsize=10
                )

                ax.axis("equal")
                st.pyplot(fig)

                ranking_news = pie_data.sort_values(ascending=False)

                marca_1 = ranking_news.index[0]
                valor_1 = int(ranking_news.iloc[0])
                porcentaje_1 = (valor_1 / total_pie) * 100 if total_pie > 0 else 0
                color_1 = COLORES_MARCA.get(str(marca_1).upper(), "#d7f54a")

                if len(ranking_news) > 1:
                    marca_2 = ranking_news.index[1]
                    valor_2 = int(ranking_news.iloc[1])
                    color_2 = COLORES_MARCA.get(str(marca_2).upper(), "#ffffff")
                    segunda_noticia = f'<span class="marca-news" style="color:{color_2}; font-weight:1000;">{marca_2}</span> sigue con {valor_2} equipos'
                else:
                    segunda_noticia = "Sin segunda marca en este filtro"

                noticia_chips = f"{chips_vendidos} chips vendidos"
                if prepago_vendidos > 0:
                    noticia_chips += f" · {prepago_vendidos} prepago"

                ticker_html = f"""
                📰 <span class="marca-news" style="color:{color_1}; font-weight:1000;">{marca_1}</span>
                lidera con {porcentaje_1:.1f}% ({valor_1} equipos) •
                {segunda_noticia} •
                {noticia_chips} •
                {total_ordenes} órdenes registradas •
                {total_stock_bajo} productos con stock bajo
                """

                st.markdown(f"""
                <div class="ticker-box">
                    <div class="ticker-title">📰 Noticias de Ultimo Minuto</div>
                    <div class="ticker">
                        <div class="ticker-track">
                            {ticker_html} &nbsp;&nbsp;&nbsp; • &nbsp;&nbsp;&nbsp; {ticker_html}
                """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        # =========================
        # TOP VENDEDORES + MODELOS
        # =========================
        col_top, col_modelos = st.columns([0.58, 0.42])

        with col_top:
            st.markdown('<div class="dash-card"><div class="dash-title">🏆 Top vendedores por marca</div>', unsafe_allow_html=True)

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

                st.dataframe(tabla_top.astype(str), use_container_width=True, height=330)

            st.markdown('</div>', unsafe_allow_html=True)

        with col_modelos:
            st.markdown('<div class="dash-card"><div class="dash-title">📱 Ranking de modelos</div>', unsafe_allow_html=True)

            if ventas_equipos.empty:
                st.info("No hay modelos vendidos para este filtro.")
            else:
                ranking_modelo = (
                    ventas_equipos.groupby(["modelo", "marca"])["cantidad"]
                    .sum()
                    .sort_values(ascending=False)
                    .reset_index()
                    .head(10)
                )
                ranking_modelo.columns = ["modelo", "marca", "Cantidad"]

                st.dataframe(
                    ranking_modelo.astype(str),
                    use_container_width=True,
                    height=330
                )

            st.markdown('</div>', unsafe_allow_html=True)

        # =========================
        # VENTAS POR DÍA + ÓRDENES
        # =========================
        col_dia, col_ordenes = st.columns([0.48, 0.52])

        with col_dia:
            st.markdown('<div class="dash-card"><div class="dash-title">📈 Ventas por día</div>', unsafe_allow_html=True)

            if ventas_equipos.empty:
                st.info("No hay ventas por día para este filtro.")
            else:
                ventas_dia = (
                    ventas_equipos.groupby(ventas_equipos["fecha"].dt.date)["cantidad"]
                    .sum()
                    .reset_index()
                )
                ventas_dia.columns = ["Fecha", "Ventas"]

                fig, ax = plt.subplots(figsize=(7, 3.6), facecolor="#15171d")
                ax.set_facecolor("#15171d")

                ax.plot(ventas_dia["Fecha"], ventas_dia["Ventas"], marker="o", linewidth=2.5, color="#d7f54a")
                ax.fill_between(ventas_dia["Fecha"], ventas_dia["Ventas"], alpha=0.18, color="#d7f54a")

                ax.tick_params(colors="white", labelsize=8)
                ax.set_ylabel("Equipos", color="white", fontsize=9)
                ax.grid(alpha=0.13)

                for spine in ax.spines.values():
                    spine.set_visible(False)

                plt.xticks(rotation=30)
                st.pyplot(fig)

            st.markdown('</div>', unsafe_allow_html=True)

        with col_ordenes:
            st.markdown('<div class="dash-card"><div class="dash-title">🧾 Últimas órdenes</div>', unsafe_allow_html=True)

            ultimas_ordenes = ventas_filtradas.drop(columns=["semana_mes"], errors="ignore").tail(15).copy()
            ultimas_ordenes = preparar_fecha_hora(ultimas_ordenes)
            ultimas_ordenes = ordenar_columnas_existentes(
                ultimas_ordenes,
                ["fecha", "hora", "vendedor", "orden", "imei", "chip", "marca", "modelo", "color", "tipo"]
            )
            ultimas_ordenes = ultimas_ordenes.replace({"None": "", "nan": "", "NaN": ""})

            st.dataframe(ultimas_ordenes.astype(str), use_container_width=True, height=330)

            st.markdown('</div>', unsafe_allow_html=True)
            
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

    opciones_inv = ["📊 Ver Stock Actual"]

    if st.session_state.get("rol") == "admin":
        opciones_inv.append("➕ Ingresar Stock")

    if not es_jefe():
        opciones_inv.extend([
            "📥 Ingreso Mercadería",
            "📤 Salida Traslado"
        ])

    opciones_inv.append("📋 Historial Movimientos")
    
    opcion_inv = st.radio(
        "Elige una opción",
        opciones_inv,
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
        stock_tabla = stock_vista[mostrar_cols].copy()
        stock_tabla["stock_actual"] = pd.to_numeric(stock_tabla["stock_actual"], errors="coerce").fillna(0).astype(int)

        def estilo_fila_marca(row):
            marca = str(row.get("marca", "")).strip().upper()
            colores_marca_pastel = {
                "APPLE": "#F5F5F5",      # blanco humo
                "SAMSUNG": "#CDEEFF",    # celeste pastel
                "XIAOMI": "#FFD8A8",     # naranja pastel
                "HONOR": "#FFB3B3",      # rojo pastel
                "MOTOROLA": "#D9B3FF",   # morado pastel
                "ZTE": "#D3D3D3",        # plomo pastel
                "VIVO": "#FFF4A3",       # amarillo pastel
                "OPPO": "#B9F6CA"        # verde pastel
            }
            color = colores_marca_pastel.get(marca, "")
            if color:
                return [f"background-color: {color}; color: #111111; font-weight: 650;"] * len(row)
            return [""] * len(row)

        def estilo_stock_actual(val):
            return ""
           
        stock_estilizado = (
            stock_tabla.style
            .map(estilo_stock_actual, subset=["stock_actual"])
        )

        st.dataframe(
            stock_estilizado,
            use_container_width=True,
            height=650
        )

    elif opcion_inv == "➕ Ingresar Stock":
    
        if st.session_state.get("rol") != "admin":
            st.error("No tienes permisos para esta acción.")
            st.stop()
    
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
    
        mov_vista["fecha_dt"] = pd.to_datetime(mov_vista["fecha"], errors="coerce")
    
        fechas_mov = sorted(
            mov_vista["fecha_dt"].dropna().dt.date.unique(),
            reverse=True
        )
    
        tipos_mov = sorted(
            mov_vista["tipo_movimiento"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().unique()
        )
    
        col_f1, col_f2 = st.columns(2)
    
        with col_f1:
            fecha_mov = st.date_input(
                "Filtrar por fecha",
                value=fechas_mov[0] if fechas_mov else fecha_hoy_local()
            )
    
        with col_f2:
            tipo_mov = st.selectbox(
                "Filtrar por tipo de movimiento",
                ["TODOS"] + tipos_mov
            )
    
        mov_vista = mov_vista[
            mov_vista["fecha_dt"].dt.date == fecha_mov
        ]
    
        if tipo_mov != "TODOS":
            mov_vista = mov_vista[
                mov_vista["tipo_movimiento"].astype(str).str.strip() == tipo_mov
            ]
    
        mov_vista = mov_vista.drop(columns=["fecha_dt"], errors="ignore")
    
        mov_vista = ordenar_columnas_existentes(
            mov_vista,
            ["fecha", "hora", "tipo_movimiento", "sku", "cantidad", "jefe_solicita", "vendedor_responsable", "detalle"]
        )
    
        if mov_vista.empty:
            st.warning("No hay movimientos con esos filtros.")
        else:
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

    if es_jefe():
        st.warning("👀 Modo jefe: solo visualización. No puedes crear equipos.")
        st.stop()

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
            
            st.session_state["notificacion_flotante"] = "📱 Nuevo equipo agregado correctamente ✅"
            
            st.rerun()

elif menu == "➕ Nuevo Accesorio":

    if es_jefe():
        st.warning("👀 Modo jefe: solo visualización. No puedes crear accesorios.")
        st.stop()

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
            st.session_state["notificacion_flotante"] = "🎧 Nuevo accesorio agregado correctamente ✅"

elif menu == "🧑‍💼 Vendedores":

    if es_jefe():
        st.warning("👀 Modo jefe: solo visualización. No puedes modificar vendedores.")
        st.stop()

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
                        st.session_state["notificacion_flotante"] = "👤 Vendedor / usuario creado correctamente ✅"
                        st.rerun()
    else:
        st.warning("Solo el administrador puede ver y crear vendedores.")

# =========================
# REGISTRAR ORDEN
# =========================
elif menu == "🧾 Registrar Orden":

    if es_jefe():
        st.warning("👀 Modo jefe: solo visualización. No puedes registrar ventas.")
        st.stop()

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

    fecha = st.date_input("Fecha", value=fecha_hoy_local(), key=f"fecha_{version}")

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

        marca_acc = st.selectbox(
            "Marca accesorio",
            sorted(accesorios["marca"].dropna().unique()),
            index=None,
            placeholder="Ingresar marca accesorio",
            key=f"marca_acc_{version}"
        )

        if marca_acc is None:
            st.info("Selecciona una marca de accesorio para continuar.")
            st.stop()

        accesorios_filtrados = accesorios[accesorios["marca"] == marca_acc]

        accesorio_desc = st.selectbox(
            "Accesorio",
            sorted(accesorios_filtrados["descripcion"].dropna().unique()),
            index=None,
            placeholder="Ingresar accesorio",
            key=f"accesorio_{version}"
        )

        if accesorio_desc is None:
            st.info("Selecciona un accesorio para continuar.")
            st.stop()

        acc_resultado = accesorios_filtrados[
            accesorios_filtrados["descripcion"] == accesorio_desc
        ]

        accesorio_sku = acc_resultado.iloc[0]["sku"]
        cantidad_accesorio = 1

        st.write("Accesorio seleccionado:")
        st.dataframe(acc_resultado.astype(str), use_container_width=True)

    if st.button("Guardar Orden", key=f"guardar_{version}"):
        orden_limpia = orden.strip()
        orden_limpia_norm = orden_limpia.upper()
        imei_limpio = imei.strip().upper()
        chip_limpio = chip.strip()

        ordenes_existentes = ventas["orden"].astype(str).str.strip().str.upper().values
        imeis_existentes = ventas["imei"].astype(str).str.strip().str.upper().values
        chips_existentes = ventas["chip"].astype(str).str.strip().values

        if orden_limpia == "":
            st.error("Debes ingresar el número de orden.")
        elif orden_limpia_norm in ordenes_existentes:
            st.error("Esa orden ya está registrada. No se puede duplicar.")
        elif not incluye_chip and not incluye_equipo and not incluye_accesorio:
            st.error("Debes seleccionar al menos Chip, Equipo o Accesorio.")
        elif incluye_equipo and sku == "":
            st.error("No se seleccionó equipo válido.")
        elif incluye_equipo and imei_limpio == "":
            st.error("Debes ingresar el IMEI del equipo.")
        elif incluye_equipo and imei_limpio in imeis_existentes:
            st.error("Ese IMEI ya está registrado en otra venta. Revisa antes de guardar.")
        elif incluye_chip and chip_limpio == "":
            st.error("Debes ingresar el número de chip.")
        elif incluye_chip and chip_limpio in chips_existentes:
            st.error("Ese chip ya está registrado en otra venta. Revisa antes de guardar.")
        else:
            nueva_venta = pd.DataFrame([{
                "fecha": fecha.strftime("%Y-%m-%d"),
                "vendedor": vendedor,
                "orden": orden_limpia,
                "chip": chip_limpio,
                "tipo_chip": tipo_chip,
                "imei": imei_limpio,
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
            st.session_state["notificacion_flotante"] = "🧾 Venta registrada correctamente ✅ Ya puedes registrar otra."
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

        if es_jefe():
            st.info("👀 Modo jefe: solo visualización de ventas. No puedes eliminar registros.")
            st.stop()

        st.subheader("🗑 Eliminar venta")

        ventas_para_borrar = ventas.copy()
        ventas_para_borrar["orden"] = ventas_para_borrar["orden"].astype(str)

        # Seguridad: los vendedores solo pueden eliminar sus propias órdenes.
        # El admin puede ver y eliminar todas.
        if st.session_state.get("rol") != "admin":
            vendedor_actual = str(st.session_state.get("vendedor", "")).strip().upper()
            ventas_para_borrar = ventas_para_borrar[
                ventas_para_borrar["vendedor"].astype(str).str.strip().str.upper() == vendedor_actual
            ]

        ordenes_disponibles = sorted(
            [o for o in ventas_para_borrar["orden"].dropna().unique() if o.strip() != ""]
        )

        if not ordenes_disponibles:
            st.info("No tienes órdenes disponibles para eliminar.")
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
                elif venta_seleccionada.empty:
                    st.error("No se encontró la venta seleccionada.")
                else:
                    venta_vendedor = str(venta_seleccionada.iloc[0].get("vendedor", "")).strip().upper()
                    vendedor_actual = str(st.session_state.get("vendedor", "")).strip().upper()

                    if st.session_state.get("rol") != "admin" and venta_vendedor != vendedor_actual:
                        st.error("No puedes eliminar órdenes de otros vendedores.")
                    else:
                        if "id" in venta_seleccionada.columns and str(venta_seleccionada.iloc[0].get("id", "")).strip() != "":
                            venta_id = venta_seleccionada.iloc[0]["id"]
                            eliminar_registro("ventas", venta_id)
                        else:
                            supabase.table("ventas").delete().eq("orden", orden_eliminar).execute()

                        st.success("Venta eliminada correctamente ✅")
                        st.session_state["mensaje_toast"] = "🗑️ Venta eliminada correctamente"
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
            fecha_min = fecha_hoy_local()
            fecha_max = fecha_hoy_local()

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

    if es_jefe():
        st.warning("👀 Modo jefe: solo visualización. No puedes editar ventas.")
        st.stop()

    st.title("✏️ Editar Venta")

    if ventas.empty or ventas["orden"].fillna("").eq("").all():
        st.info("No hay ventas para editar.")
    else:
        ventas_editables = ventas.copy()

        if st.session_state.get("rol") != "admin":
            vendedor_actual = str(st.session_state.get("vendedor", "")).strip().upper()
            ventas_editables = ventas_editables[
                ventas_editables["vendedor"].astype(str).str.strip().str.upper() == vendedor_actual
            ]

        if ventas_editables.empty or ventas_editables["orden"].fillna("").eq("").all():
            st.info("No tienes ventas propias para editar.")
        else:

            # =========================
            # LISTA POR FECHA
            # =========================
            if "orden_editar" not in st.session_state:

                st.subheader("📅 Filtrar ventas por fecha")

                ventas_filtradas = ventas_editables.copy()
                ventas_filtradas["fecha"] = pd.to_datetime(
                    ventas_filtradas["fecha"], errors="coerce"
                )

                fechas_disponibles = sorted(
                    ventas_filtradas["fecha"].dropna().dt.date.unique(),
                    reverse=True
                )

                if not fechas_disponibles:
                    st.warning("No hay fechas válidas para filtrar.")
                    st.stop()

                fecha_filtro = st.date_input(
                    "Selecciona fecha",
                    value=fechas_disponibles[0]
                )
                buscar_orden = st.text_input(
                    "🔎 Buscar por orden",
                    placeholder="Escribe el número de orden"
                ).strip()

                ventas_filtradas = ventas_filtradas[
                    ventas_filtradas["fecha"].dt.date == fecha_filtro
                ]
                if buscar_orden:
                    ventas_filtradas = ventas_filtradas[
                        ventas_filtradas["orden"].astype(str).str.contains(buscar_orden, case=False, na=False)
                    ]

                if ventas_filtradas.empty:
                    st.warning("No hay ventas en esa fecha.")
                    st.stop()

                st.subheader("Ventas del día")

                for i, row in ventas_filtradas.iterrows():
                    col1, col2 = st.columns([0.78, 0.22])

                    equipo_txt = ""
                    if str(row.get("marca", "")).strip() != "":
                        equipo_txt = f"📱 {row.get('marca', '')} {row.get('modelo', '')}"

                    accesorio_txt = ""
                    if str(row.get("accesorio", "")).strip() != "":
                        accesorio_txt = f"🎧 {row.get('accesorio', '')}"

                    chip_txt = ""
                    if str(row.get("chip", "")).strip() != "":
                        chip_txt = f"📶 {row.get('tipo_chip', '')} - {row.get('chip', '')}"

                    with col1:
                        st.markdown(f"""
                        **Orden:** {row.get('orden', '')}  
                        👤 {row.get('vendedor', '')}  
                        {equipo_txt}  
                        {accesorio_txt}  
                        {chip_txt}
                        """)

                    with col2:
                        if st.button("✏️ Editar", key=f"editar_venta_{i}"):
                            st.session_state["orden_editar"] = str(row.get("orden", ""))
                            st.rerun()

                st.stop()

            # =========================
            # FORMULARIO DE EDICIÓN
            # =========================
            orden_editar = st.session_state.get("orden_editar", "")

            venta_match = ventas_editables[
                ventas_editables["orden"].astype(str) == str(orden_editar)
            ]

            if venta_match.empty:
                st.error("No se encontró la orden seleccionada.")
                st.session_state.pop("orden_editar", None)
                st.stop()

            idx = venta_match.index[0]
            venta = ventas.loc[idx].copy()

            if st.button("🔙 Volver a ventas del día"):
                st.session_state.pop("orden_editar", None)
                st.rerun()

            st.subheader("Datos actuales")
            st.dataframe(pd.DataFrame([venta]).astype(str), use_container_width=True)

            st.subheader("Editar datos")

            fecha_actual = pd.to_datetime(venta.get("fecha", ""), errors="coerce")
            if pd.isna(fecha_actual):
                fecha_actual = timestamp_hoy_local()

            nueva_fecha = st.date_input("Fecha de venta", value=fecha_actual.date())

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

            # =========================
            # EQUIPO
            # =========================
            tiene_equipo_actual = str(venta.get("marca", "")).strip() != ""
            editar_equipo = st.checkbox("Esta venta tiene equipo", value=tiene_equipo_actual)

            nueva_marca = ""
            nuevo_modelo = ""
            nuevo_color = ""
            nuevo_tipo = ""
            nuevo_sku = ""
            nueva_cantidad = 0

            if editar_equipo:
                st.subheader("Equipo")

                producto, producto_df = seleccionar_producto(
                    productos,
                    prefijo=f"editar_{idx}",
                    default_marca=str(venta.get("marca", "")),
                    default_modelo=str(venta.get("modelo", "")),
                    default_color=str(venta.get("color", "")),
                    default_tipo=str(venta.get("tipo", ""))
                )

                nuevo_sku = producto["sku"]
                nueva_marca = producto["marca"]
                nuevo_modelo = producto["modelo"]
                nuevo_color = producto["color"]
                nuevo_tipo = producto["tipo"]
                nueva_cantidad = 1

                st.write("Equipo seleccionado:")
                st.dataframe(producto_df.astype(str), use_container_width=True)

            # =========================
            # ACCESORIO
            # =========================
            tiene_accesorio_actual = str(venta.get("accesorio", "")).strip() != ""
            editar_accesorio = st.checkbox("Esta venta tiene accesorio", value=tiene_accesorio_actual)

            nuevo_accesorio_sku = ""
            nuevo_accesorio = ""
            nueva_cantidad_accesorio = 0

            if editar_accesorio:
                st.subheader("Accesorio")

                accesorios_lista = accesorios.copy()

                if accesorios_lista.empty:
                    st.warning("No hay accesorios registrados.")
                else:
                    accesorios_lista["texto_acc"] = (
                        accesorios_lista["marca"].astype(str)
                        + " - "
                        + accesorios_lista["descripcion"].astype(str)
                    )

                    accesorio_actual = str(venta.get("accesorio", "")).strip()
                    opciones_acc = accesorios_lista["texto_acc"].tolist()

                    index_acc = 0
                    for j, opcion in enumerate(opciones_acc):
                        if accesorio_actual != "" and accesorio_actual in opcion:
                            index_acc = j
                            break

                    accesorio_sel = st.selectbox(
                        "Accesorio",
                        opciones_acc,
                        index=index_acc,
                        key=f"editar_acc_{idx}"
                    )

                    acc_row = accesorios_lista[
                        accesorios_lista["texto_acc"] == accesorio_sel
                    ].iloc[0]

                    nuevo_accesorio_sku = acc_row["sku"]
                    nuevo_accesorio = acc_row["descripcion"]

                    cantidad_acc_actual = pd.to_numeric(
                        venta.get("cantidad_accesorio", 1),
                        errors="coerce"
                    )

                    if pd.isna(cantidad_acc_actual) or cantidad_acc_actual < 1:
                        cantidad_acc_actual = 1

                    nueva_cantidad_accesorio = st.number_input(
                        "Cantidad accesorio",
                        min_value=1,
                        step=1,
                        value=int(cantidad_acc_actual),
                        key=f"editar_cant_acc_{idx}"
                    )

            if st.button("Guardar edición"):
                nueva_orden_limpia = nueva_orden.strip()
                nueva_orden_norm = nueva_orden_limpia.upper()
                nuevo_imei_limpio = nuevo_imei.strip().upper()
                nuevo_chip_limpio = nuevo_chip.strip()

                ordenes_existentes = ventas.drop(index=idx)["orden"].astype(str).str.strip().str.upper().values
                imeis_existentes = ventas.drop(index=idx)["imei"].astype(str).str.strip().str.upper().values
                chips_existentes = ventas.drop(index=idx)["chip"].astype(str).str.strip().values

                venta_vendedor = str(venta.get("vendedor", "")).strip().upper()
                vendedor_actual = str(st.session_state.get("vendedor", "")).strip().upper()

                if st.session_state.get("rol") != "admin" and venta_vendedor != vendedor_actual:
                    st.error("No puedes editar órdenes de otros vendedores.")
                elif nueva_orden_limpia == "":
                    st.error("La orden no puede quedar vacía.")
                elif nueva_orden_norm in ordenes_existentes:
                    st.error("Esa orden ya existe en otra venta.")
                elif editar_equipo and nuevo_imei_limpio == "":
                    st.error("El IMEI no puede quedar vacío si la venta tiene equipo.")
                elif editar_equipo and nuevo_imei_limpio in imeis_existentes:
                    st.error("Ese IMEI ya está registrado en otra venta.")
                elif nuevo_chip_limpio != "" and nuevo_chip_limpio in chips_existentes:
                    st.error("Ese chip ya está registrado en otra venta.")
                else:
                    venta_id = ventas.loc[idx, "id"]

                    cambios = {
                        "fecha": nueva_fecha.strftime("%Y-%m-%d"),
                        "orden": nueva_orden_limpia,
                        "chip": nuevo_chip_limpio,
                        "tipo_chip": nuevo_tipo_chip,
                        "imei": nuevo_imei_limpio if editar_equipo else "",
                        "sku": nuevo_sku,
                        "marca": nueva_marca,
                        "modelo": nuevo_modelo,
                        "color": nuevo_color,
                        "tipo": nuevo_tipo,
                        "cantidad": nueva_cantidad,
                        "accesorio_sku": nuevo_accesorio_sku,
                        "accesorio": nuevo_accesorio,
                        "cantidad_accesorio": int(nueva_cantidad_accesorio),
                    }

                    actualizar_registro("ventas", venta_id, cambios)

                    st.session_state["notificacion_flotante"] = "✏️ Venta editada correctamente ✅"
                    st.session_state.pop("orden_editar", None)
                    st.rerun()# =========================
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
                fecha_min = fecha_hoy_local()
                fecha_max = fecha_hoy_local()

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
