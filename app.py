import json
import hashlib
import sqlite3
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from streamlit_autorefresh import st_autorefresh

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "respostas_alunos.sqlite3"

st.set_page_config(
    page_title="EVSimulator",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="auto",
)

CSS = """
<style>
:root {
    --bg-0: #030712;
    --bg-1: #07111f;
    --bg-2: #0b1627;
    --card: rgba(5, 12, 26, 0.78);
    --card-2: rgba(9, 19, 36, 0.92);
    --border: rgba(66, 185, 255, 0.22);
    --text: #eaf2ff;
    --muted: #a4b5cc;
    --blue: #23a0ff;
    --green: #76e72d;
    --teal: #19d3c5;
    --danger: #ff5c7a;
    --soft-shadow: 0 12px 34px rgba(0, 0, 0, 0.34);
}
html, body, [class*="css"] {
    font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}
[data-testid="stAppViewContainer"] {
    background:
      radial-gradient(circle at 12% 82%, rgba(0, 130, 255, 0.18), transparent 22%),
      radial-gradient(circle at 88% 18%, rgba(125, 255, 53, 0.16), transparent 18%),
      linear-gradient(135deg, var(--bg-0) 0%, var(--bg-1) 46%, var(--bg-2) 100%);
    color: var(--text);
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 1340px;
}
[data-testid="stSidebar"] {
    background: rgba(6, 15, 30, 0.98);
    border-right: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stSidebar"] * { color: var(--text); }
h1, h2, h3, h4, p, li, label, .stMarkdown, .stCaption, .stText, .stSubheader {
    color: var(--text);
}
.big-title {
    font-size: 3.6rem;
    line-height: 0.96;
    font-weight: 900;
    margin: 0 0 0.65rem 0;
    letter-spacing: -0.03em;
}
.brand-grad {
    background: linear-gradient(90deg, var(--blue) 0%, #3eb7ff 25%, var(--green) 80%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.subtitle {
    font-size: 1.15rem;
    color: var(--muted);
    margin-bottom: 1rem;
}
.hero-shell {
    min-height: 74vh;
    display: flex;
    align-items: center;
}
.hero-card {
    border: 1px solid rgba(255,255,255,0.05);
    background: linear-gradient(180deg, rgba(7, 16, 31, 0.74), rgba(2, 8, 18, 0.55));
    border-radius: 28px;
    padding: 2.2rem 2rem;
    box-shadow: var(--soft-shadow);
    backdrop-filter: blur(8px);
}
.login-panel {
    background: rgba(1, 10, 24, 0.82);
    border: 1px solid rgba(37, 169, 255, 0.22);
    border-radius: 28px;
    padding: 1.6rem 1.5rem;
    box-shadow: var(--soft-shadow);
    backdrop-filter: blur(8px);
}
.glow-line {
    height: 2px;
    width: 120px;
    background: linear-gradient(90deg, rgba(35,160,255,0), rgba(35,160,255,1), rgba(118,231,45,1), rgba(118,231,45,0));
    border-radius: 99px;
    margin: 1rem 0 1.4rem 0;
}
.neo-card {
    background: linear-gradient(180deg, rgba(5, 12, 26, 0.88), rgba(9, 19, 36, 0.9));
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 18px 20px;
    box-shadow: var(--soft-shadow);
    margin-bottom: 12px;
}
.metric-card {
    background: linear-gradient(180deg, rgba(8, 18, 34, 0.92), rgba(6, 14, 29, 0.92));
    border: 1px solid rgba(35,160,255,0.18);
    border-left: 5px solid var(--blue);
    border-radius: 16px;
    padding: 14px 16px;
    min-height: 84px;
    overflow-wrap: anywhere;
    box-shadow: var(--soft-shadow);
}
.label-muted { color: var(--muted); font-size: 0.9rem; }
.status-ok { color: #5bff93; font-weight: 800; }
.status-fail { color: #ff7a96; font-weight: 800; }
.small-note { color: var(--muted); font-size: 13px; }
.input-note { color: var(--muted); font-size: 0.88rem; margin-top: -0.3rem; }
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 999px;
    background: rgba(255,255,255,0.03);
    color: var(--muted);
    font-size: 0.9rem;
    margin-bottom: 1.2rem;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    overflow-x: auto;
}
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.04);
    border-radius: 12px;
    padding: 10px 14px;
    border: 1px solid rgba(255,255,255,0.08);
    color: var(--text);
    white-space: nowrap;
}
.stTabs [aria-selected="true"] {
    border-color: rgba(35,160,255,0.5);
    box-shadow: 0 0 0 1px rgba(35,160,255,0.14) inset;
}
.stTextInput input, .stSelectbox div[data-baseweb="select"] > div,
.stTextArea textarea, .stNumberInput input {
    background: rgba(6, 14, 29, 0.95) !important;
    color: var(--text) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 14px !important;
}
.stSlider label, .stSelectbox label, .stTextInput label, .stRadio label { color: var(--text) !important; }
button[kind="primary"], .stButton > button {
    min-height: 46px;
    border-radius: 14px;
    border: 0 !important;
    font-weight: 700;
    background: linear-gradient(90deg, rgba(70, 92, 130, 0.98), rgba(93, 111, 145, 0.98));
    color: #f6f8fb !important;
}
button[kind="primary"]:hover, .stButton > button:hover {
    filter: brightness(1.06);
}
.osc-panel {
    border: 1px solid rgba(35,160,255,0.18);
    border-radius: 18px;
    background: rgba(7,16,31,0.72);
    padding: 0.5rem;
}
.hero-svg-wrap {
    margin-top: 1rem;
    width: 100%;
    max-width: 720px;
}
.info-chip-row {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 1rem;
}
.info-chip {
    padding: 9px 12px;
    border-radius: 14px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    color: var(--muted);
    font-size: 0.9rem;
}
@media (max-width: 900px) {
    .big-title { font-size: 2.35rem; }
    .subtitle { font-size: 1rem; }
    .hero-shell { min-height: auto; }
    .hero-card, .login-panel { padding: 1.25rem 1rem; border-radius: 22px; }
    .block-container { padding-left: 0.7rem; padding-right: 0.7rem; padding-top: 0.6rem; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def init_db():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS respostas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                aluno_nome TEXT NOT NULL,
                turma TEXT,
                usuario TEXT,
                componente_id TEXT NOT NULL,
                componente_nome TEXT NOT NULL,
                falha TEXT NOT NULL,
                causa_provavel TEXT,
                primeiro_teste TEXT,
                alimentacao_esperada TEXT,
                sinal_esperado TEXT,
                dtcs TEXT
            )
            """
        )
        conn.commit()


def save_student_response(user, comp, fault, causa, teste):
    dtcs = "; ".join([f"{d.get('codigo')} - {d.get('descricao')}" for d in dtc_for_fault(comp, fault)])
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO respostas (
                timestamp, aluno_nome, turma, usuario, componente_id, componente_nome, falha,
                causa_provavel, primeiro_teste, alimentacao_esperada, sinal_esperado, dtcs
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                user.get("name", ""),
                user.get("turma", ""),
                user.get("username", ""),
                comp.get("id", ""),
                comp.get("nome", ""),
                fault,
                causa,
                teste,
                comp.get("alimentacao", ""),
                comp.get("sinal", ""),
                dtcs,
            ),
        )
        conn.commit()


def load_student_responses():
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query("SELECT * FROM respostas ORDER BY id DESC", conn)


init_db()


COMPONENTES = load_json(DATA_DIR / "componentes.json")
FALHAS = load_json(DATA_DIR / "falhas.json")
USERS = load_json(DATA_DIR / "users.json")


def hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def authenticate(username: str, password: str):
    user = USERS.get(username.strip())
    if not user:
        return None
    if hash_password(password, user["salt"]) == user["password_hash"]:
        return {
            "username": username.strip(),
            "name": user.get("name", username),
            "role": user.get("role", "aluno"),
        }
    return None


def card_open():
    st.markdown("<div class='neo-card'>", unsafe_allow_html=True)


def card_close():
    st.markdown("</div>", unsafe_allow_html=True)


def hero_vehicle_path():
    return BASE_DIR / "assets" / "hero" / "ev_vehicle_exact.png"



def login_screen():
    st.markdown("<div class='hero-shell'>", unsafe_allow_html=True)
    left, right = st.columns([1.3, 0.9], gap="large")

    with left:
        st.markdown("<div class='hero-card'>", unsafe_allow_html=True)
        st.markdown("<div class='hero-badge'>⚡ Plataforma interativa para diagnóstico automotivo e veículos eletrificados</div>", unsafe_allow_html=True)
        st.markdown("<div class='big-title'><span class='brand-grad'>EVSimulator</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='subtitle'>Bancada virtual para diagnóstico de sensores, atuadores e módulos. Visualize alimentação, sinal elétrico, forma de onda, falhas simuladas e DTCs em uma interface moderna para desktop e mobile.</div>", unsafe_allow_html=True)
        st.markdown("<div class='glow-line'></div>", unsafe_allow_html=True)
        hero_img = hero_vehicle_path()
        if hero_img.exists():
            st.image(str(hero_img), use_container_width=True)
        st.markdown(
            """
            <div class='info-chip-row'>
                <div class='info-chip'>📉 Osciloscópio em tempo real</div>
                <div class='info-chip'>🔌 Alimentação, terra e sinal</div>
                <div class='info-chip'>🧩 Sensores, atuadores e módulos</div>
                <div class='info-chip'>🛠️ Falhas e DTCs simulados</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='login-panel'>", unsafe_allow_html=True)
        st.markdown("### Acesso ao simulador")
        st.markdown("<p class='label-muted'>Preencha sua identificação e informe as credenciais de acesso.</p>", unsafe_allow_html=True)

        display_name = st.text_input("Nome", value=st.session_state.get("display_name", ""), placeholder="Digite seu nome")
        turma = st.text_input("Turma", value=st.session_state.get("turma", ""), placeholder="Digite sua turma")
        username = st.text_input("Usuário", value=st.session_state.get("last_username", ""), placeholder="professor ou aluno")
        password = st.text_input("Senha", type="password", value="", placeholder="Digite sua senha")

        st.markdown("<p class='input-note'>Acesso demonstrativo: <b>professor / Senai@2026</b> ou <b>aluno / 1234</b>.</p>", unsafe_allow_html=True)
        if st.button("Entrar", use_container_width=True):
            user = authenticate(username, password)
            if user:
                user["name"] = display_name.strip() or user["name"]
                user["turma"] = turma.strip()
                st.session_state["display_name"] = user["name"]
                st.session_state["turma"] = user["turma"]
                st.session_state["last_username"] = username.strip()
                st.session_state["user"] = user
                st.session_state.setdefault("layout_mode", "Automático")
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")

        st.markdown("---")
        st.markdown("**Publicação recomendada:** GitHub + Streamlit Cloud ou execução local no laboratório.")
        st.markdown("**Mobile:** execute com `--server.address=0.0.0.0` e acesse pelo IP do computador na mesma rede.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def component_by_id(cid: str):
    return next(c for c in COMPONENTES if c["id"] == cid)


def dtc_for_fault(comp, fault):
    dtcs = comp.get("dtcs", [])
    if not dtcs or fault == "Normal":
        return []
    mode = FALHAS[fault].get("mode", "range")
    keywords = {
        "gnd": ["baixo", "low"],
        "pos": ["alto", "high"],
        "open": ["circuito", "circuit"],
        "intermittent": ["intermitente", "intermittent"],
        "range": ["faixa", "desempenho", "performance", "correlação"],
    }.get(mode, [])
    selected = []
    for item in dtcs:
        text = (item["codigo"] + " " + item["descricao"]).lower()
        if any(k in text for k in keywords):
            selected.append(item)
    return selected if selected else dtcs[:1]


def apply_fault_to_signal(y, fault, max_v=5.0):
    y = np.array(y, dtype=float)
    mode = FALHAS[fault].get("mode")
    if fault == "Normal" or mode is None:
        return y
    if mode == "gnd":
        return np.zeros_like(y)
    if mode == "pos":
        return np.ones_like(y) * max_v
    if mode == "open":
        rng = np.random.default_rng(7)
        return np.clip(max_v * 0.5 + rng.normal(0, max_v * 0.18, size=len(y)), 0, max_v)
    if mode == "intermittent":
        out = y.copy()
        n = len(out)
        for start in range(n // 8, n, max(15, n // 5)):
            out[start:start + max(4, n // 25)] = 0
        return out
    if mode == "range":
        return np.clip(y * 0.62 + max_v * 0.12, 0, max_v)
    return y


def generate_signal(comp, fault, rpm=1500, load=45, temp=85, duration=2.0, samples=1200, phase_offset=0.0):
    tipo = comp["tipo_sinal"]
    t = np.linspace(0, duration, samples) + phase_offset
    p = comp.get("parametros", {})
    title = "Sinal simulado"
    y2 = None
    y2_name = None
    y_name = "Tensão [V]"
    max_v = float(p.get("amp_v", p.get("max_v", 5)))

    if tipo == "digital_freq":
        base = float(p.get("freq_base_hz", 10))
        freq = max(0.1, base * rpm / 1000.0)
        amp = float(p.get("amp_v", 5))
        duty = float(p.get("duty", 50)) / 100.0
        phase = (t * freq) % 1.0
        y = np.where(phase < duty, amp, 0.0)
        title = f"Onda digital/frequência - {freq:.1f} Hz"
        max_v = amp
    elif tipo == "analogico":
        min_v = float(p.get("min_v", 0.5)); max_v = float(p.get("max_v", 4.5))
        base = min_v + (max_v - min_v) * (load / 100)
        y = base + 0.04 * np.sin(2 * np.pi * 3 * t) + 0.02 * np.sin(2 * np.pi * 13 * t)
        title = f"Sinal analógico 0–5 V - carga {load}%"
    elif tipo == "ntc":
        tmin = float(p.get("temp_min", -10)); tmax = float(p.get("temp_max", 120))
        vcold = float(p.get("v_cold", 4.2)); vhot = float(p.get("v_hot", 0.4))
        frac = np.clip((temp - tmin) / (tmax - tmin), 0, 1)
        base = vcold + (vhot - vcold) * frac
        y = base + 0.015 * np.sin(2 * np.pi * 1.5 * t)
        max_v = 5.0
        title = f"Sensor NTC - {temp:.0f} °C"
    elif tipo == "lambda":
        min_v = float(p.get("min_v", 0.1)); max_v = float(p.get("max_v", 0.9)); freq = float(p.get("freq_hz", 1.2))
        y = (min_v + max_v) / 2 + ((max_v - min_v) / 2) * np.tanh(3 * np.sin(2 * np.pi * freq * t))
        title = "Sonda lambda narrowband - comutação rica/pobre"
    elif tipo == "piezo":
        amp = float(p.get("amp_v", 0.15)); fk = float(p.get("freq_khz", 6.0)) * 1000
        envelope = np.exp(-((t - 0.8) ** 2) / 0.002) + 0.7 * np.exp(-((t - 1.45) ** 2) / 0.0015)
        y = 2.5 + amp * envelope * np.sin(2 * np.pi * fk * t)
        max_v = 5.0
        title = "Sensor piezoelétrico - vibração/detonação"
    elif tipo == "pwm_current":
        freq = float(p.get("freq_hz", 50)); duty = float(p.get("duty", 20)) / 100; amp = float(p.get("amp_v", 12))
        phase = (t * freq) % 1
        y = np.where(phase < duty, amp, 0.0)
        current_peak = float(p.get("current_peak", 2.0))
        ramp = (phase / duty) if duty > 0 else phase
        y2 = np.where(phase < duty, current_peak * np.clip(ramp, 0, 1), 0)
        y2_name = "Corrente [A]"
        max_v = amp
        title = f"Comando PWM/driver - duty {duty * 100:.0f}%"
    elif tipo == "motor_dc":
        freq = float(p.get("freq_hz", 100)); duty = float(p.get("duty", 50)) / 100; amp = float(p.get("amp_v", 12))
        phase = (t * freq) % 1
        y = np.where(phase < duty, amp, 0.0)
        current_peak = float(p.get("current_peak", 5.0))
        y2 = current_peak * duty + 0.25 * np.sin(2 * np.pi * freq * t)
        y2_name = "Corrente [A]"
        max_v = amp
        title = f"Atuador/motor DC com PWM - duty {duty * 100:.0f}%"
    elif tipo == "can":
        bit_rate_demo = 20
        bits = ((np.sin(2 * np.pi * bit_rate_demo * t) + np.sin(2 * np.pi * 7 * t)) > 0).astype(float)
        y = 2.5 + 1.0 * bits
        y2 = 2.5 - 1.0 * bits
        y2_name = "CAN-L [V]"
        y_name = "CAN-H [V]"
        max_v = 5.0
        title = "Comunicação digital CAN - representação didática"
    elif tipo == "ultrasonic":
        distance = max(0.2, 3.0 - 2.6 * load / 100)
        bursts = np.zeros_like(t)
        for center in np.arange(0.2, duration, 0.35):
            bursts += np.exp(-((t - center) ** 2) / 0.0005) * np.sin(2 * np.pi * 40000 * t)
            echo = center + distance / 343 * 2
            bursts += 0.45 * np.exp(-((t - echo) ** 2) / 0.0008) * np.sin(2 * np.pi * 40000 * t)
        y = 2.5 + 1.2 * bursts
        max_v = 5.0
        title = f"Ultrassom - distância estimada {distance:.2f} m"
    elif tipo == "resistivo":
        min_v = float(p.get("min_v", 0.3)); max_v = float(p.get("max_v", 4.7))
        base = min_v + (max_v - min_v) * load / 100
        y = base + 0.02 * np.sin(2 * np.pi * 0.7 * t)
        title = f"Sensor resistivo - nível/posição {load}%"
    else:
        y = np.zeros_like(t)

    y_fault = apply_fault_to_signal(y, fault, max_v=max_v)
    if y2 is not None:
        y2 = apply_fault_to_signal(y2, fault, max_v=max(1.0, float(np.nanmax(y2)) * 1.1))
    return t, y_fault, y2, y_name, y2_name, title


def plot_signal(t, y, y2=None, y_name="Tensão [V]", y2_name=None, title="Sinal", mobile=False):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=y, mode="lines", name=y_name, line=dict(width=2.2, color="#22aaff")))
    if y2 is not None:
        fig.add_trace(go.Scatter(x=t, y=y2, mode="lines", name=y2_name or "Canal 2", yaxis="y2", line=dict(width=2.1, color="#8efc2f")))
        fig.update_layout(yaxis2=dict(title=y2_name or "Canal 2", overlaying="y", side="right", showgrid=False, color="#d7e4f5"))
    fig.update_layout(
        title=title,
        xaxis_title="Tempo [s]",
        yaxis_title=y_name,
        height=345 if mobile else 435,
        margin=dict(l=30 if mobile else 40, r=20 if mobile else 40, t=52 if mobile else 62, b=36 if mobile else 40),
        paper_bgcolor="rgba(7,16,31,1)",
        plot_bgcolor="rgba(2,8,18,0.98)",
        font=dict(color="#eaf2ff", size=11 if mobile else 13),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.08)", zeroline=False, color="#d7e4f5")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.08)", zeroline=False, color="#d7e4f5")
    return fig


def info_card(title, value):
    st.markdown(f"<div class='metric-card'><b>{title}</b><br>{value}</div>", unsafe_allow_html=True)


def render_header(user, mobile=False):
    left, right = st.columns([4, 1])
    with left:
        st.markdown("<div class='big-title'><span class='brand-grad'>EVSimulator</span></div>", unsafe_allow_html=True)
        if mobile:
            st.markdown("<div class='subtitle'>Modo mobile: escolha o componente, a falha e a seção desejada.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='subtitle'>Bancada virtual interativa para diagnóstico de sensores, atuadores e módulos em veículos convencionais e eletrificados.</div>", unsafe_allow_html=True)
    with right:
        nome = user.get("name", user.get("username", "Usuário"))
        turma = user.get("turma", "")
        st.write(f"**Usuário:** {nome}")
        st.write(f"**Perfil:** {user['role']}")
        if turma:
            st.write(f"**Turma:** {turma}")
        if st.button("Sair", use_container_width=True):
            st.session_state.clear()
            st.rerun()


def sidebar_config(user):
    with st.sidebar:
        st.header("Configuração")
        paginas = ["Simulador", "Mapa do veículo"]
        if user.get("role") == "professor":
            paginas.append("Painel do professor")
        pagina = st.radio("Tela", paginas, index=0)
        layout_mode = st.radio(
            "Modo de visualização",
            ["Automático", "Desktop", "Mobile"],
            index=["Automático", "Desktop", "Mobile"].index(st.session_state.get("layout_mode", "Automático")),
            help="Use Mobile no celular para trocar abas longas por seções verticais.",
        )
        st.session_state["layout_mode"] = layout_mode
        mobile = layout_mode == "Mobile"

        categorias = ["Todos"] + sorted(set(c["categoria"] for c in COMPONENTES))
        categoria = st.selectbox("Categoria", categorias)
        search = st.text_input("Buscar componente", placeholder="Ex.: MAP, ABS, injetor")
        filtered = COMPONENTES
        if categoria != "Todos":
            filtered = [c for c in filtered if c["categoria"] == categoria]
        if search.strip():
            s = search.lower().strip()
            filtered = [c for c in filtered if s in c["nome"].lower() or s in c["id"].lower() or s in c["sistema"].lower()]
        if not filtered:
            st.warning("Nenhum componente encontrado.")
            return None
        comp_names = {f"{c.get('icone', '')} {c['nome']}": c["id"] for c in filtered}
        labels = list(comp_names.keys())
        forced_id = st.session_state.pop("forced_component_id", None)
        default_index = 0
        if forced_id:
            for i, label in enumerate(labels):
                if comp_names[label] == forced_id:
                    default_index = i
                    break
        selected_label = st.selectbox("Componente", labels, index=default_index)
        comp = component_by_id(comp_names[selected_label])
        fault = st.selectbox("Falha simulada", list(FALHAS.keys()))
        rpm = st.slider("Rotação [rpm]", 600, 4500, 1500, 100)
        load = st.slider("Carga/posição [%]", 0, 100, 45, 5)
        temp = st.slider("Temperatura [°C]", -10, 130, int(comp.get("parametros", {}).get("normal_temp", 85)), 5)
        realtime = st.toggle("Sinais em tempo real", value=True, help="Atualiza automaticamente o osciloscópio, criando movimento contínuo dos sinais.")
        refresh_ms = st.slider("Velocidade da animação [ms]", 150, 1200, 350, 50, disabled=not realtime)
        st.divider()
        st.caption("Modo professor ativo." if user["role"] == "professor" else "Modo aluno: roteiro completo oculto.")
    return pagina, comp, fault, rpm, load, temp, mobile, realtime, refresh_ms


def render_component_summary(comp, fault, mobile=False):
    image_path = BASE_DIR / comp["imagem"]
    status = "<span class='status-ok'>NORMAL</span>" if fault == "Normal" else "<span class='status-fail'>FALHA ATIVA</span>"

    if mobile:
        card_open()
        st.subheader(comp["nome"])
        if image_path.exists():
            st.image(str(image_path), use_container_width=True)
        st.caption(comp["funcao"])
        card_close()
        m1, m2 = st.columns(2)
        with m1:
            info_card("Sistema", comp["sistema"])
        with m2:
            info_card("Status", status)
        card_open()
        st.subheader("Alimentação e sinal")
        st.write(f"**Alimentação:** {comp['alimentacao']}")
        st.write(f"**Terra/retorno:** {comp['terra']}")
        st.write(f"**Sinal:** {comp['sinal']}")
        st.write(f"**Pinos típicos:** {comp['pinos']}")
        st.write(f"**Faixa esperada:** {comp['faixa_normal']}")
        card_close()
    else:
        col_img, col_info = st.columns([1.05, 1.35], gap="large")
        with col_img:
            card_open()
            st.subheader(comp["nome"])
            if image_path.exists():
                st.image(str(image_path), use_container_width=True)
            st.caption(comp["funcao"])
            card_close()
        with col_info:
            m1, m2, m3 = st.columns(3)
            with m1:
                info_card("Sistema", comp["sistema"])
            with m2:
                info_card("Categoria", comp["categoria"])
            with m3:
                info_card("Status simulado", status)
            card_open()
            st.subheader("Alimentação, terra e sinal")
            st.write(f"**Alimentação:** {comp['alimentacao']}")
            st.write(f"**Terra/retorno:** {comp['terra']}")
            st.write(f"**Sinal:** {comp['sinal']}")
            st.write(f"**Pinos típicos:** {comp['pinos']}")
            st.write(f"**Faixa esperada:** {comp['faixa_normal']}")
            card_close()


def section_scope(comp, fault, rpm, load, temp, mobile=False, realtime=False, refresh_ms=350):
    samples = 700 if mobile else 1200
    phase_offset = 0.0
    if realtime:
        tick = st_autorefresh(interval=refresh_ms, key=f"osc_{comp['id']}_{fault}_{mobile}")
        phase_offset = tick * (refresh_ms / 1000.0)
    t, y, y2, y_name, y2_name, title = generate_signal(comp, fault, rpm=rpm, load=load, temp=temp, samples=samples, phase_offset=phase_offset)
    st.markdown("<div class='osc-panel'>", unsafe_allow_html=True)
    st.plotly_chart(
        plot_signal(t, y, y2, y_name, y2_name, title, mobile=mobile),
        use_container_width=True,
        config={"responsive": True, "displayModeBar": not mobile},
    )
    st.markdown("</div>", unsafe_allow_html=True)
    if realtime:
        st.caption(f"Animação ativa: atualização automática a cada {refresh_ms} ms.")
    else:
        st.caption("Representação didática: use manual do fabricante e diagrama elétrico real para diagnóstico em veículo.")


def section_scanner(comp, fault):
    card_open()
    st.subheader("Leitura simulada do scanner")
    dtcs = dtc_for_fault(comp, fault)
    if dtcs:
        df = pd.DataFrame(dtcs)
        df["status"] = "Ativo/simulado"
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.success("Nenhum DTC ativo na condição normal simulada.")
    st.write(f"**Falha selecionada:** {fault}")
    st.write(f"**Descrição:** {FALHAS[fault]['descricao']}")
    st.write(f"**Efeito esperado:** {FALHAS[fault]['efeito']}")
    st.write(f"**Sintomas prováveis:** {comp['sintomas']}")
    card_close()


def section_description(comp):
    card_open()
    st.subheader("Base técnica do componente")
    st.write(comp["funcao"])
    rows = [
        ["Alimentação", comp["alimentacao"]],
        ["Terra/retorno", comp["terra"]],
        ["Sinal", comp["sinal"]],
        ["Pinos típicos", comp["pinos"]],
        ["Faixa normal", comp["faixa_normal"]],
    ]
    st.table(pd.DataFrame(rows, columns=["Item", "Descrição"]))
    card_close()


def section_test(comp, user, fault="Normal"):
    card_open()
    st.subheader("Roteiro de teste")
    if user["role"] == "professor":
        st.markdown("**Gabarito técnico / roteiro sugerido:**")
        for i, step in enumerate(comp.get("diagnostico", []), 1):
            st.write(f"**{i}.** {step}")
        st.info("Professor: selecione a falha, peça ao aluno para identificar alimentação, sinal, DTC e causa provável. As respostas dos alunos ficam salvas no Painel do professor.")
    else:
        st.write("Responda com base no gráfico, alimentação, sintomas e DTCs.")
        causa = st.text_area("Qual a causa provável da falha?", height=90, key=f"causa_{comp['id']}_{fault}")
        teste = st.text_area("Qual teste você faria primeiro?", height=90, key=f"teste_{comp['id']}_{fault}")
        if st.button("Registrar resposta", use_container_width=True):
            if not causa.strip() or not teste.strip():
                st.warning("Preencha causa provável e primeiro teste antes de registrar.")
            else:
                save_student_response(user, comp, fault, causa.strip(), teste.strip())
                st.success("Resposta salva no banco local SQLite do simulador.")
    card_close()


def section_images():
    card_open()
    st.subheader("Banco de imagens")
    refs = list((BASE_DIR / "assets" / "referencias").glob("*.png"))
    if refs:
        cols = st.columns(min(2, len(refs)))
        for i, ref in enumerate(refs):
            with cols[i % len(cols)]:
                st.image(str(ref), caption=ref.name, use_container_width=True)
    st.write("Para usar fotos reais: salve a imagem em `assets/componentes/` com o mesmo nome do `id`, por exemplo `map.png`, e ajuste `data/componentes.json` quando necessário.")
    card_close()


def render_sections(comp, fault, rpm, load, temp, user, mobile=False, realtime=False, refresh_ms=350):
    if mobile:
        selected = st.selectbox(
            "Seção",
            ["Osciloscópio", "Scanner e DTC", "Descrição técnica", "Teste guiado", "Banco de imagens"],
            index=0,
        )
        if selected == "Osciloscópio":
            section_scope(comp, fault, rpm, load, temp, mobile=True, realtime=realtime, refresh_ms=refresh_ms)
        elif selected == "Scanner e DTC":
            section_scanner(comp, fault)
        elif selected == "Descrição técnica":
            section_description(comp)
        elif selected == "Teste guiado":
            section_test(comp, user, fault=fault)
        else:
            section_images()
    else:
        tabs = st.tabs(["Osciloscópio", "Scanner e DTC", "Descrição técnica", "Teste guiado", "Banco de imagens"])
        with tabs[0]:
            section_scope(comp, fault, rpm, load, temp, mobile=False, realtime=realtime, refresh_ms=refresh_ms)
        with tabs[1]:
            section_scanner(comp, fault)
        with tabs[2]:
            section_description(comp)
        with tabs[3]:
            section_test(comp, user, fault=fault)
        with tabs[4]:
            section_images()


def render_vehicle_map(user):
    st.markdown("<div class='big-title'><span class='brand-grad'>Mapa interativo do veículo</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Selecione um módulo no veículo para abrir sua tela técnica no simulador.</div>", unsafe_allow_html=True)
    hero_img = hero_vehicle_path()
    card_open()
    if hero_img.exists():
        st.image(str(hero_img), use_container_width=True)
    st.markdown("**Hotspots funcionais:**")
    modules = [
        ("ECM / ECU", "ecu", "Motor"),
        ("PCM", "pcm", "Trem de força"),
        ("TCM", "tcm", "Transmissão"),
        ("BCM", "bcm", "Carroceria"),
        ("ABS", "abs_module", "Freios"),
        ("SRS", "airbag_module", "Segurança passiva"),
        ("EPS", "eps_module", "Direção elétrica"),
        ("EPB", "epb_module", "Freio estacionamento"),
    ]
    cols = st.columns(4)
    for i, (label, cid, area) in enumerate(modules):
        with cols[i % 4]:
            if st.button(f"{label} | {area}", use_container_width=True, key=f"map_{cid}"):
                st.session_state["forced_component_id"] = cid
                st.success(f"{label} selecionado. Abra a tela Simulador na barra lateral para visualizar sinais, alimentação e DTCs.")
    card_close()


def render_professor_dashboard():
    st.markdown("<div class='big-title'><span class='brand-grad'>Painel do professor</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Acompanhamento das respostas registradas pelos alunos.</div>", unsafe_allow_html=True)
    df = load_student_responses()
    if df.empty:
        card_open()
        st.info("Ainda não há respostas registradas.")
        card_close()
        return
    c1, c2, c3 = st.columns(3)
    with c1:
        info_card("Respostas", str(len(df)))
    with c2:
        info_card("Alunos", str(df["aluno_nome"].nunique()))
    with c3:
        info_card("Turmas", str(df["turma"].replace("", np.nan).nunique()))

    turmas = ["Todas"] + sorted([t for t in df["turma"].dropna().unique().tolist() if str(t).strip()])
    comps = ["Todos"] + sorted(df["componente_nome"].dropna().unique().tolist())
    f1, f2 = st.columns(2)
    with f1:
        turma = st.selectbox("Filtrar por turma", turmas)
    with f2:
        comp_nome = st.selectbox("Filtrar por componente", comps)
    view = df.copy()
    if turma != "Todas":
        view = view[view["turma"] == turma]
    if comp_nome != "Todos":
        view = view[view["componente_nome"] == comp_nome]

    card_open()
    st.dataframe(view, use_container_width=True, hide_index=True)
    csv = view.to_csv(index=False).encode("utf-8-sig")
    st.download_button("Baixar respostas em CSV", data=csv, file_name="respostas_ev_simulator.csv", mime="text/csv", use_container_width=True)
    card_close()


def main_app():
    user = st.session_state["user"]
    config = sidebar_config(user)
    if config is None:
        return
    pagina, comp, fault, rpm, load, temp, mobile, realtime, refresh_ms = config

    if pagina == "Mapa do veículo":
        render_vehicle_map(user)
        return
    if pagina == "Painel do professor":
        render_professor_dashboard()
        return

    render_header(user, mobile=mobile)

    if st.session_state.get("layout_mode") == "Automático":
        st.caption("Modo automático: o Streamlit empilha os blocos no celular. Para uma interface mais leve, selecione Mobile na barra lateral.")

    render_component_summary(comp, fault, mobile=mobile)
    render_sections(comp, fault, rpm, load, temp, user, mobile=mobile, realtime=realtime, refresh_ms=refresh_ms)


if "user" not in st.session_state:
    login_screen()
else:
    main_app()
