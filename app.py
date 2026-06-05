import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ==========================================
# CONFIGURACIÓN DE PÁGINA
# ==========================================

st.set_page_config(
    page_title="Academia Premilitar — Sistema de Rendimiento",
    page_icon="🎖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# ESTILOS GLOBALES
# ==========================================

st.markdown("""
<style>
    /* ---- Fuentes ---- */
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600&family=Source+Sans+3:wght@300;400;600&display=swap');

    /* ---- Variables ---- */
    :root {
        --gold:    #C9A84C;
        --gold-lt: #E8D49A;
        --navy:    #0D1B2A;
        --navy-2:  #162233;
        --navy-3:  #1E3148;
        --slate:   #2C4464;
        --text:    #E8EEF4;
        --muted:   #8CA3BA;
        --border:  rgba(201,168,76,0.25);
        --success: #3BA55D;
        --warn:    #E2B640;
        --danger:  #C94040;
    }

    /* ---- Fondo general ---- */
    .stApp {
        background: var(--navy) !important;
        color: var(--text) !important;
    }

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] {
        background: var(--navy-2) !important;
        border-right: 1px solid var(--border) !important;
    }
    section[data-testid="stSidebar"] * {
        color: var(--text) !important;
    }

    /* ---- Tipografía ---- */
    h1, h2, h3 {
        font-family: 'Oswald', sans-serif !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        color: var(--gold) !important;
    }
    p, label, div, span {
        font-family: 'Source Sans 3', sans-serif !important;
    }

    /* ---- Inputs ---- */
    input, textarea, select {
        background: var(--navy-3) !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: 4px !important;
    }
    input:focus, textarea:focus {
        border-color: var(--gold) !important;
        box-shadow: 0 0 0 2px rgba(201,168,76,0.2) !important;
    }

    /* ---- Botones ---- */
    .stButton > button {
        background: linear-gradient(135deg, #C9A84C, #A8863A) !important;
        color: var(--navy) !important;
        font-family: 'Oswald', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.6rem 2rem !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(201,168,76,0.35) !important;
    }

    /* ---- Métricas ---- */
    [data-testid="metric-container"] {
        background: var(--navy-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        padding: 1rem 1.2rem !important;
    }
    [data-testid="stMetricLabel"] p {
        color: var(--muted) !important;
        font-size: 12px !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }
    [data-testid="stMetricValue"] {
        color: var(--gold) !important;
        font-family: 'Oswald', sans-serif !important;
        font-size: 2rem !important;
    }
    [data-testid="stMetricDelta"] {
        color: var(--muted) !important;
        font-size: 13px !important;
    }

    /* ---- Alertas ---- */
    .stAlert {
        border-radius: 6px !important;
        border-left: 4px solid !important;
    }
    .stSuccess { border-left-color: var(--success) !important; background: rgba(59,165,93,0.1) !important; }
    .stWarning { border-left-color: var(--warn) !important; background: rgba(226,182,64,0.1) !important; }
    .stError   { border-left-color: var(--danger) !important; background: rgba(201,64,64,0.1) !important; }
    .stInfo    { border-left-color: var(--gold) !important; background: rgba(201,168,76,0.07) !important; }

    /* ---- Divisores ---- */
    hr {
        border-color: var(--border) !important;
        margin: 1.5rem 0 !important;
    }

    /* ---- Dataframe ---- */
    .stDataFrame {
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
    }

    /* ---- Radio sidebar ---- */
    .stRadio label { font-size: 15px !important; }

    /* ---- Progress bar ---- */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--gold), var(--gold-lt)) !important;
    }

    /* ---- Número input ---- */
    [data-baseweb="input"] { background: var(--navy-3) !important; }

    /* ---- Quitar padding extra ---- */
    .block-container { padding-top: 2rem !important; }

    /* ---- Badge personalizado ---- */
    .badge-alto   { background:#1a4a2e; color:#5edd8a; border:1px solid #3BA55D; border-radius:20px; padding:4px 14px; font-family:'Oswald',sans-serif; font-size:15px; letter-spacing:1px; }
    .badge-medio  { background:#4a3a0a; color:#f5cc60; border:1px solid #E2B640; border-radius:20px; padding:4px 14px; font-family:'Oswald',sans-serif; font-size:15px; letter-spacing:1px; }
    .badge-bajo   { background:#4a1010; color:#f07070; border:1px solid #C94040; border-radius:20px; padding:4px 14px; font-family:'Oswald',sans-serif; font-size:15px; letter-spacing:1px; }

    /* ---- Card info estudiante ---- */
    .card-field {
        background: var(--navy-3);
        border: 1px solid var(--border);
        border-radius: 6px;
        padding: 0.6rem 1rem;
        margin-bottom: 8px;
        font-size: 15px;
    }
    .card-label {
        color: var(--muted);
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 2px;
    }
    .card-value {
        color: var(--text);
        font-size: 16px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# CARGAR DATOS
# ==========================================

@st.cache_data
def cargar_datos():
    return pd.read_excel("rendimiento_academico.xlsx")

@st.cache_resource
def cargar_modelo():
    modelo = joblib.load("modelo_rendimiento.pkl")
    scaler = joblib.load("scaler.pkl")
    return modelo, scaler

datos = cargar_datos()
modelo, scaler = cargar_modelo()

FEATURES = [
    "faltas_disciplinarias", "practica_oral", "horas_estudio",
    "asistencia", "simulacros", "tardanzas",
    "cumplimiento_tareas", "participacion", "examen_fisico"
]


# ==========================================
# HELPERS
# ==========================================

def badge_rendimiento(nivel):
    """Devuelve HTML con badge de color según nivel."""
    mapa = {
        "Alto":  ("badge-alto",  "▲ ALTO"),
        "Medio": ("badge-medio", "● MEDIO"),
        "Bajo":  ("badge-bajo",  "▼ BAJO"),
    }
    cls, txt = mapa.get(nivel, ("badge-medio", nivel))
    return f'<span class="{cls}">{txt}</span>'


def campo_info(label, valor):
    return f"""
    <div class="card-field">
        <div class="card-label">{label}</div>
        <div class="card-value">{valor}</div>
    </div>
    """


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1.2rem 0 1.5rem;">
        <div style="font-size:2.5rem;">🎖️</div>
        <div style="font-family:'Oswald',sans-serif; font-size:1.1rem;
                    color:#C9A84C; letter-spacing:2px; text-transform:uppercase;
                    line-height:1.3; margin-top:8px;">
            Academia<br>Premilitar
        </div>
        <div style="color:#8CA3BA; font-size:12px; letter-spacing:1px; margin-top:6px;">
            Sistema de Predicción IA
        </div>
    </div>
    <hr style="border-color:rgba(201,168,76,0.25); margin:0 0 1rem;">
    """, unsafe_allow_html=True)

    menu = st.radio(
        "Navegación",
        ["Inicio", "Buscar Estudiante", "Nuevo Estudiante", "Dashboard"],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="color:#8CA3BA; font-size:11px; letter-spacing:1px; text-align:center;">
        Modelo: Regresión Logística<br>
        <span style="color:#C9A84C;">●</span> Sistema activo
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# INICIO
# ==========================================

if menu == "Inicio":

    st.markdown("## Sistema Inteligente de Rendimiento Académico")
    st.markdown("""
    <p style="color:#8CA3BA; font-size:15px; max-width:600px;">
    Plataforma de predicción basada en Inteligencia Artificial para el seguimiento
    y clasificación del desempeño académico de los cadetes.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    total = len(datos)
    alto  = len(datos[datos["rendimiento"] == "Alto"])
    medio = len(datos[datos["rendimiento"] == "Medio"])
    bajo  = len(datos[datos["rendimiento"] == "Bajo"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Cadetes",       total)
    c2.metric("Rendimiento Alto",    alto,  f"{alto/total*100:.1f}%")
    c3.metric("Rendimiento Medio",   medio, f"{medio/total*100:.1f}%")
    c4.metric("Rendimiento Bajo",    bajo,  f"{bajo/total*100:.1f}%")

    st.markdown("---")

    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.markdown("#### Distribución General")
        fig, ax = plt.subplots(figsize=(7, 3))
        fig.patch.set_facecolor("#0D1B2A")
        ax.set_facecolor("#162233")

        cats   = ["Alto", "Medio", "Bajo"]
        values = [alto, medio, bajo]
        colors = ["#3BA55D", "#E2B640", "#C94040"]
        bars   = ax.bar(cats, values, color=colors, width=0.5, edgecolor="none")

        for bar, val in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5,
                str(val),
                ha="center", va="bottom",
                color="#C9A84C", fontsize=13, fontweight="bold"
            )

        ax.set_xticks([0, 1, 2])
        ax.set_xticklabels(cats, color="#8CA3BA", fontsize=12)
        ax.set_ylabel("Cadetes", color="#8CA3BA", fontsize=11)
        ax.tick_params(axis="y", colors="#8CA3BA")
        ax.spines[:].set_color("#2C4464")
        ax.set_ylim(0, max(values) * 1.25)
        ax.yaxis.set_minor_locator(plt.AutoLocator())

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with col_b:
        st.markdown("#### Proporción")
        fig2, ax2 = plt.subplots(figsize=(3.5, 3.5))
        fig2.patch.set_facecolor("#0D1B2A")
        ax2.set_facecolor("#0D1B2A")

        wedges, texts, autotexts = ax2.pie(
            values,
            labels=cats,
            colors=["#3BA55D", "#E2B640", "#C94040"],
            autopct="%1.0f%%",
            startangle=90,
            wedgeprops=dict(width=0.55, edgecolor="#0D1B2A", linewidth=2)
        )
        for t in texts:      t.set_color("#8CA3BA")
        for t in autotexts:  t.set_color("#0D1B2A"); t.set_fontweight("bold")

        st.pyplot(fig2, use_container_width=True)
        plt.close(fig2)

    st.markdown("---")
    st.info("💡 Usa el menú lateral para buscar un cadete, registrar uno nuevo o explorar el dashboard completo.")


# ==========================================
# BUSCAR ESTUDIANTE
# ==========================================

elif menu == "Buscar Estudiante":

    st.markdown("## Buscar Cadete")
    st.markdown('<p style="color:#8CA3BA;">Ingrese el código del cadete para consultar su perfil y predicción de rendimiento.</p>', unsafe_allow_html=True)
    st.markdown("---")

    col_inp, col_btn = st.columns([3, 1])
    with col_inp:
        codigo = st.text_input("Código del cadete", placeholder="Ej: A0001", label_visibility="collapsed")
    with col_btn:
        buscar = st.button("🔍 Buscar")

    if buscar:
        estudiante = datos[datos["codigo"] == codigo]

        if estudiante.empty:
            st.error("⚠️ No se encontró ningún cadete con ese código.")

        else:
            est = estudiante.iloc[0]

            st.markdown("---")
            st.markdown(f"### {est['nombre']}")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(campo_info("Código",           est["codigo"]),           unsafe_allow_html=True)
                st.markdown(campo_info("Asistencia",       f"{est['asistencia']}%"), unsafe_allow_html=True)
                st.markdown(campo_info("Horas de Estudio", est["horas_estudio"]),    unsafe_allow_html=True)

            with col2:
                st.markdown(campo_info("Participación",    est["participacion"]),    unsafe_allow_html=True)
                st.markdown(campo_info("Práctica Oral",    est["practica_oral"]),    unsafe_allow_html=True)
                st.markdown(campo_info("Examen Físico",    est["examen_fisico"]),    unsafe_allow_html=True)

            with col3:
                st.markdown(campo_info("Simulacros",          est["simulacros"]),           unsafe_allow_html=True)
                st.markdown(campo_info("Cumplimiento Tareas", f"{est['cumplimiento_tareas']}%"), unsafe_allow_html=True)
                st.markdown(campo_info("Tardanzas",           est["tardanzas"]),            unsafe_allow_html=True)

            # Predicción
            X_pred = pd.DataFrame({f: [est[f]] for f in FEATURES})
            X_pred = scaler.transform(X_pred)
            resultado       = modelo.predict(X_pred)[0]
            probabilidades  = modelo.predict_proba(X_pred)[0]

            st.markdown("---")
            st.markdown("#### Predicción de Rendimiento")

            col_res, col_proba = st.columns([1, 2])

            with col_res:
                st.markdown(f"""
                <div style="background:#162233; border:1px solid rgba(201,168,76,0.3);
                            border-radius:10px; padding:1.5rem; text-align:center; margin-top:8px;">
                    <div style="color:#8CA3BA; font-size:11px; letter-spacing:2px; text-transform:uppercase; margin-bottom:12px;">
                        Clasificación IA
                    </div>
                    {badge_rendimiento(resultado)}
                </div>
                """, unsafe_allow_html=True)

            with col_proba:
                st.markdown('<div style="padding-top:8px;">', unsafe_allow_html=True)
                for clase, prob in zip(modelo.classes_, probabilidades):
                    color = {"Alto": "#3BA55D", "Medio": "#E2B640", "Bajo": "#C94040"}.get(clase, "#C9A84C")
                    st.markdown(f"""
                    <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
                        <div style="width:55px; color:{color}; font-size:13px; font-weight:600;">{clase}</div>
                        <div style="flex:1; background:#1E3148; border-radius:4px; height:10px; overflow:hidden;">
                            <div style="width:{prob*100:.1f}%; background:{color}; height:100%; border-radius:4px; transition:width 0.5s;"></div>
                        </div>
                        <div style="width:45px; color:#8CA3BA; font-size:13px; text-align:right;">{prob*100:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# NUEVO ESTUDIANTE
# ==========================================

elif menu == "Nuevo Estudiante":

    st.markdown("## Registro y Predicción — Nuevo Cadete")
    st.markdown('<p style="color:#8CA3BA;">Complete los datos del cadete. El sistema generará un código automático y guardará el registro en la base de datos.</p>', unsafe_allow_html=True)
    st.markdown("---")

    # ---- Código automático ----
    def generar_codigo(df):
        try:
            codigos = df["codigo"].astype(str)
            nums = []
            for c in codigos:
                if c.startswith("A") and c[1:].isdigit():
                    nums.append(int(c[1:]))
            siguiente = max(nums) + 1 if nums else 1
        except Exception:
            siguiente = len(df) + 1
        return f"A{siguiente}"

    codigo_nuevo = generar_codigo(datos)

    st.markdown(f"""
    <div style="background:#162233; border:1px solid rgba(201,168,76,0.4);
                border-radius:8px; padding:0.8rem 1.2rem; display:inline-block; margin-bottom:1rem;">
        <span style="color:#8CA3BA; font-size:11px; letter-spacing:2px; text-transform:uppercase;">
            Código asignado —
        </span>
        <span style="color:#C9A84C; font-family:'Oswald',sans-serif; font-size:1.3rem;
                     letter-spacing:3px; margin-left:8px;">
            {codigo_nuevo}
        </span>
    </div>
    """, unsafe_allow_html=True)

    nombre = st.text_input("Nombre completo del cadete")

    st.markdown("#### Indicadores Académicos y Disciplinarios")
    c1, c2 = st.columns(2)

    with c1:
        faltas        = st.number_input("Faltas disciplinarias",   min_value=0,   max_value=10,  value=0)
        practica      = st.number_input("Práctica oral (0–20)",    min_value=0,   max_value=20,  value=10)
        horas         = st.number_input("Horas de estudio",        min_value=1,   max_value=10,  value=4)
        asistencia    = st.number_input("Asistencia (%)",          min_value=0,   max_value=100, value=80)
        simulacros    = st.number_input("Simulacros aprobados",    min_value=0,   max_value=10,  value=5)

    with c2:
        tardanzas     = st.number_input("Tardanzas",               min_value=0,   max_value=20,  value=2)
        tareas        = st.number_input("Cumplimiento tareas (%)", min_value=0,   max_value=100, value=75)
        participacion = st.number_input("Participación (1–10)",    min_value=1,   max_value=10,  value=5)
        examen        = st.number_input("Examen físico (0–20)",    min_value=0,   max_value=20,  value=12)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡ Registrar y Predecir"):

        if not nombre.strip():
            st.warning("⚠️ Ingresa el nombre del cadete antes de continuar.")
            st.stop()

        # ---- Predicción ----
        nuevo_df = pd.DataFrame({
            "faltas_disciplinarias": [faltas],
            "practica_oral":         [practica],
            "horas_estudio":         [horas],
            "asistencia":            [asistencia],
            "simulacros":            [simulacros],
            "tardanzas":             [tardanzas],
            "cumplimiento_tareas":   [tareas],
            "participacion":         [participacion],
            "examen_fisico":         [examen],
        })

        nuevo_sc       = scaler.transform(nuevo_df)
        resultado      = modelo.predict(nuevo_sc)[0]
        probabilidades = modelo.predict_proba(nuevo_sc)[0]

        # ---- Guardar en Excel ----
        fila_nueva = {
            "codigo":                 codigo_nuevo,
            "nombre":                 nombre.strip(),
            "faltas_disciplinarias":  faltas,
            "practica_oral":          practica,
            "horas_estudio":          horas,
            "asistencia":             asistencia,
            "simulacros":             simulacros,
            "tardanzas":              tardanzas,
            "cumplimiento_tareas":    tareas,
            "participacion":          participacion,
            "examen_fisico":          examen,
            "rendimiento":            resultado,
        }

        try:
            df_actualizado = pd.concat(
                [datos, pd.DataFrame([fila_nueva])],
                ignore_index=True
            )
            df_actualizado.to_excel("rendimiento_academico.xlsx", index=False)
            # Limpiar caché para que "Buscar Estudiante" vea el nuevo registro
            st.cache_data.clear()
            guardado_ok = True
        except Exception as e:
            guardado_ok = False
            error_msg   = str(e)

        # ---- Resultado visual ----
        st.markdown("---")

        if guardado_ok:
            st.success(f"✅ Cadete registrado correctamente con el código **{codigo_nuevo}**")
        else:
            st.error(f"⚠️ No se pudo guardar en Excel: {error_msg}")

        st.markdown("#### Resultado de Predicción")

        col_badge, col_proba = st.columns([1, 2])

        with col_badge:
            st.markdown(f"""
            <div style="background:#162233; border:1px solid rgba(201,168,76,0.3);
                        border-radius:10px; padding:1.8rem 1.2rem; text-align:center;">
                <div style="color:#8CA3BA; font-size:11px; letter-spacing:2px;
                            text-transform:uppercase; margin-bottom:4px;">
                    {nombre.strip()}
                </div>
                <div style="color:#C9A84C; font-family:'Oswald',sans-serif;
                            font-size:13px; letter-spacing:2px; margin-bottom:10px;">
                    {codigo_nuevo}
                </div>
                <div style="margin:8px 0;">
                    {badge_rendimiento(resultado)}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_proba:
            st.markdown("**Distribución de probabilidades:**")
            for clase, prob in zip(modelo.classes_, probabilidades):
                color = {"Alto": "#3BA55D", "Medio": "#E2B640", "Bajo": "#C94040"}.get(clase, "#C9A84C")
                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
                    <div style="width:55px; color:{color}; font-size:13px; font-weight:600;">{clase}</div>
                    <div style="flex:1; background:#1E3148; border-radius:4px; height:10px; overflow:hidden;">
                        <div style="width:{prob*100:.1f}%; background:{color}; height:100%; border-radius:4px;"></div>
                    </div>
                    <div style="width:45px; color:#8CA3BA; font-size:13px; text-align:right;">{prob*100:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)

        # ---- Observaciones ----
        st.markdown("---")
        st.markdown("#### Observaciones")

        recomendaciones = []
        if faltas >= 3:
            recomendaciones.append("⚠️ Alto número de faltas disciplinarias — se recomienda seguimiento.")
        if asistencia < 75:
            recomendaciones.append("⚠️ Asistencia por debajo del 75% — riesgo de rezago.")
        if horas <= 2:
            recomendaciones.append("📚 Aumentar horas de estudio diarias.")
        if examen < 10:
            recomendaciones.append("🏃 Reforzar preparación física.")
        if not recomendaciones:
            recomendaciones.append("✅ El cadete muestra un perfil académico saludable.")

        for obs in recomendaciones:
            st.markdown(f"- {obs}")


# ==========================================
# DASHBOARD
# ==========================================

elif menu == "Dashboard":

    st.markdown("## Dashboard General")
    st.markdown('<p style="color:#8CA3BA;">Análisis estadístico del cuerpo de cadetes registrados.</p>', unsafe_allow_html=True)
    st.markdown("---")

    total = len(datos)
    alto  = len(datos[datos["rendimiento"] == "Alto"])
    medio = len(datos[datos["rendimiento"] == "Medio"])
    bajo  = len(datos[datos["rendimiento"] == "Bajo"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Cadetes",     total)
    c2.metric("Alto Rendimiento",  alto,  f"{alto/total*100:.1f}%")
    c3.metric("Medio Rendimiento", medio, f"{medio/total*100:.1f}%")
    c4.metric("Bajo Rendimiento",  bajo,  f"{bajo/total*100:.1f}%")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    # ---- Gráfica de barras ----
    with col_left:
        st.markdown("#### Distribución por Nivel")
        fig, ax = plt.subplots(figsize=(5, 3.5))
        fig.patch.set_facecolor("#0D1B2A")
        ax.set_facecolor("#162233")

        cats   = ["Alto", "Medio", "Bajo"]
        values = [alto, medio, bajo]
        colors = ["#3BA55D", "#E2B640", "#C94040"]

        bars = ax.barh(cats, values, color=colors, height=0.5, edgecolor="none")
        for bar, val in zip(bars, values):
            ax.text(
                bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                str(val), va="center", color="#C9A84C", fontsize=12, fontweight="bold"
            )

        ax.set_xlabel("Número de cadetes", color="#8CA3BA", fontsize=10)
        ax.tick_params(colors="#8CA3BA")
        ax.spines[:].set_color("#2C4464")
        ax.set_xlim(0, max(values) * 1.3)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    # ---- Promedios por variable ----
    with col_right:
        st.markdown("#### Promedio por Variable")
        vars_plot  = ["asistencia", "practica_oral", "examen_fisico",
                      "participacion", "horas_estudio", "cumplimiento_tareas"]
        etiquetas  = ["Asistencia", "P. Oral", "Examen Fís.", "Participac.", "H. Estudio", "C. Tareas"]

        promedios = [datos[v].mean() for v in vars_plot]

        fig2, ax2 = plt.subplots(figsize=(5, 3.5))
        fig2.patch.set_facecolor("#0D1B2A")
        ax2.set_facecolor("#162233")

        bar2 = ax2.bar(etiquetas, promedios, color="#C9A84C", width=0.5, edgecolor="none")
        ax2.set_ylabel("Promedio", color="#8CA3BA", fontsize=10)
        ax2.tick_params(axis="x", colors="#8CA3BA", labelsize=9, rotation=15)
        ax2.tick_params(axis="y", colors="#8CA3BA")
        ax2.spines[:].set_color("#2C4464")
        ax2.set_ylim(0, max(promedios) * 1.2)

        st.pyplot(fig2, use_container_width=True)
        plt.close(fig2)

    st.markdown("---")

    # ---- Tabla de cadetes ----
    st.markdown("#### Base de Datos de Cadetes")

    def color_rendimiento(val):
        mapa = {"Alto": "color: #3BA55D; font-weight:600",
                "Medio": "color: #E2B640; font-weight:600",
                "Bajo": "color: #C94040; font-weight:600"}
        return mapa.get(val, "")

    df_show = datos.head(50).copy()
    st.dataframe(df_show, use_container_width=True)