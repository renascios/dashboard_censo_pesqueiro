# -*- coding: utf-8 -*-
# app.py — Censo Pesqueiro (OCA) — 

from pathlib import Path
import base64
import unicodedata

import streamlit as st
import pandas as pd
import plotly.express as px

import folium
from streamlit_folium import st_folium
from PIL import Image

# ============================================================================
# CONFIG INICIAL
# ============================================================================
oca_logo = Image.open("oca_site.png")
st.set_page_config(page_title="Censo Pesqueiro — OCA", page_icon=oca_logo, layout="wide")
#st.set_page_config(page_title="Censo Pesqueiro — OCA", page_icon="🌊", layout="wide")

THEME = {
    "primary": "#2E73B8",
    "brand":   "#2E2A74",
    "text":    "#0F172A",
    "muted":   "#64748B",
    "bg":      "#FFFFFF",
    "bg_soft": "#F3F6FA",
    "radius":  "14px",
}

# ============================================================================
# CSS GLOBAL
# ============================================================================
st.markdown(f"""
<style>         
.block-container {{
  padding-top: 0.8rem;
  padding-bottom: 2rem;
}}

/* Header: logo sem corte, com espaço e sem clipping */
.app-header {{
  width: 100%;              /*background: {THEME["brand"]};/*
  background: transparent;  /* tira a barra azul */
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 35px 0;            /* mais espaço vertical */
  padding-bottom: 10px; /* reduz espaço da base */
  margin: 0 0 12px 0;
  overflow: visible;          /* garante que nada seja cortado */
  position: relative;
  z-index: 1;
}}
.app-header img {{
  display: block;
  height: auto;
  max-height: 100px;           /* pode aumentar se quiser maior */
  width: auto;
  max-width: 100%;
}}

/* KPIs */
.kpi-card {{
  border-radius: {THEME["radius"]};
  padding: 14px 16px;
  border: 1px solid rgba(0,0,0,0.06);
  background: {THEME["bg"]};
  box-shadow: 0 1px 8px rgba(0,0,0,0.04);
}}
.kpi-value {{ font-size: 1.6rem; font-weight: 700; color: {THEME["brand"]}; }}
.kpi-label {{ color: {THEME["muted"]}; font-size: 0.9rem; }}

.section-card {{
  border-radius: {THEME["radius"]};
  padding: 16px 18px;
  border: 1px solid rgba(0,0,0,0.06);
  background: {THEME["bg"]};
}}
</style>
""", unsafe_allow_html=True)

# ============================================================================
st.markdown(f"""
<style>
/* ============================
   Ajuste apenas das caixas select/multiselect
   ============================ */
div[data-baseweb="select"] > div {{
  background-color: #E3F2FD !important;
  border: 1px solid #2E73B8 !important;
  border-radius: 8px !important;
}}
div[data-baseweb="select"] span {{
  color: none !important;
  font-weight: 600 !important;
}}
div[data-baseweb="select"]:focus-within {{
  box-shadow: 0 0 0 2px #2E73B8 !important;
}}
ul[role="listbox"] li[aria-selected="true"],
ul[role="listbox"] li[data-selected="true"],
ul[role="listbox"] li[data-highlighted="true"],
ul[role="listbox"] li:hover {{
  background-color: #BBDEFB !important;
  color: #0F172A !important;
  font-weight: 600 !important;
}}
/* Chips do multiselect (meses selecionados) */
div[data-baseweb="tag"] {{
  background-color: #2E2A74 !important; /* azul mais escuro */
  color: white !important;             /* texto branco */
  border-radius: 6px !important;
  border: 1px solid #2E73B8 !important;
}}
</style>
""", unsafe_allow_html=True)

# ============================================================================
st.markdown("""
<style>
/* remove apenas o ícone/botão de download da toolbar do dataframe */
button[title="Download as CSV"],
div[title="Download as CSV"] {
  display: none !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* remove a toolbar do st.dataframe (download, busca e fullscreen) */
div[data-testid="stElementToolbar"] {
  display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPERS
# ============================================================================
def fmt_int(x):
    try:
        return f"{int(x):,}".replace(",", ".")
    except Exception:
        return "-"

def fmt_float(x, nd=2):
    try:
        s = f"{float(x):,.{nd}f}"
    except Exception:
        return "-"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")

def fmt_kg(x, nd=2):
    s = fmt_float(x, nd)
    return s + " kg" if s != "-" else s

def kpi(label: str, value: str):
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-value">{value}</div>
      <div class="kpi-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

def section(title: str):
    st.markdown(f"### {title}")

def _norm(s: str) -> str:
    """normaliza string: remove acentos, troca hífen por espaço, tira espaços duplicados, lower"""
    s = str(s or "").strip()
    s = ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))
    s = s.replace("-", " ")
    while "  " in s:
        s = s.replace("  ", " ")
    return s.lower()

# ============================================================================
# HEADER (logo)
# ============================================================================
def render_header(logo_path="oca_logo2.png"):
    p = Path(logo_path)
    if p.exists():
        b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
        st.markdown(
            f'<div class="app-header"><img src="data:image/png;base64,{b64}" alt="logo OCA"/></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="app-header"><h3 style="color:white;margin:0;">Observatório da Costa Amazônica</h3></div>',
            unsafe_allow_html=True
        )

render_header()

st.markdown("## Censo Pesqueiro — Zona Costeira Amazônica")
st.caption("Visão geral • Análises por RESEX • Série temporal")

# ============================================================================
# DADOS
# ============================================================================
DATA_PATH = "Base_Coleta_OCA_ATUALIZADA_02.07.2025.xlsx"

@st.cache_data(show_spinner=True)
def carregar_dados(caminho: str) -> pd.DataFrame:
    p = Path(caminho)
    if not p.exists():
        return pd.DataFrame()
    df = pd.read_excel(p)

    # Tipos e limpeza
    df["Total (kg)"] = pd.to_numeric(df.get("Total (kg)"), errors="coerce")
    if "Qtidades" in df.columns:
        df["Qtidades"] = pd.to_numeric(df.get("Qtidades"), errors="coerce")

    # Colunas-chave
    df["Resex"] = df.get("Resex", "").astype(str).str.strip()
    df["Mês"]   = df.get("Mês", "").astype(str).str.strip().str.capitalize()
    df = df.dropna(subset=["Nome Popular", "Total (kg)", "Resex", "Mês"])

    # Municipio normalizado (corrige contagem)
    if "Municipio" in df.columns:
        df["Municipio"] = (
            df["Municipio"].astype(str).str.strip()
            .replace({"": pd.NA, "-": pd.NA, "nan": pd.NA, "None": pd.NA, "NULL": pd.NA})
        )
        MUNIC_ALIASES = {
            "Sao Luis": "São Luís",
            "São Luis": "São Luís",
            "Belem": "Belém",
            "Belem/PA": "Belém",
        }
        df["Municipio"] = df["Municipio"].map(lambda x: MUNIC_ALIASES.get(x, x))

    # Datas (mensal)
    mes_map = {
        "Janeiro":1, "Fevereiro":2, "Março":3, "Marco":3, "Abril":4, "Maio":5, "Junho":6,
        "Julho":7, "Agosto":8, "Setembro":9, "Outubro":10, "Novembro":11, "Dezembro":12
    }
    df["Mes_Num"] = (df["Mês"].map(mes_map)
                        .fillna(pd.to_numeric(df["Mês"], errors="coerce")))
    df["Ano"] = pd.to_numeric(df.get("Ano"), errors="coerce")
    df = df.dropna(subset=["Ano", "Mes_Num"])
    df["Mes_Num"] = df["Mes_Num"].astype(int)
    df["Ano"] = df["Ano"].astype(int)
    df["Data_Mensal"] = pd.to_datetime({"year": df["Ano"], "month": df["Mes_Num"], "day": 1})

    # Normalização de RESEX
    df["Resex_norm"]  = df["Resex"].map(_norm)
    # Label "bonito" preferindo o primeiro visto
    df["Resex_label"] = df.groupby("Resex_norm")["Resex"].transform("first")

    return df

df = carregar_dados(DATA_PATH)
if df.empty:
    st.error(f"Arquivo de dados não encontrado ou vazio: `{DATA_PATH}`")
    st.stop()

# ============================================================================
# KPIs GERAIS (ANTES DOS FILTROS)
# ============================================================================
col_k1, col_k2, col_k3, col_k4 = st.columns(4)
with col_k1: kpi("Peso Total (kg)", fmt_kg(df["Total (kg)"].sum()))
with col_k2: kpi("Espécies", fmt_int(df["Nome Popular"].nunique()))
with col_k3:
    n_mun = df["Municipio"].dropna().nunique() if "Municipio" in df.columns else 0
    kpi("Municípios", fmt_int(n_mun))
with col_k4: kpi("RESEXs", fmt_int(df["Resex"].nunique() if "Resex" in df.columns else 0))

st.divider()

# ============================================================================
# TOP 10 GERAL (Gráfico + Tabela) — sem download
# ============================================================================
section("Top 10 Geral")

top10_geral = (df.groupby("Nome Popular")["Total (kg)"]
                 .sum().sort_values(ascending=False).head(10).reset_index())

# margem esquerda dinâmica p/ não cortar labels
max_lab_len = top10_geral["Nome Popular"].astype(str).str.len().max() if not top10_geral.empty else 12
left_margin = max(100, min(16 + int(max_lab_len * 7.2), 260))

left, right = st.columns([1.2, 1])

with left:
    fig1 = px.bar(
        top10_geral, x="Total (kg)", y="Nome Popular",
        orientation="h", template="none",
        color_discrete_sequence=[THEME["brand"]],
        height=400
    )
    if not top10_geral.empty:
        min_val = top10_geral["Total (kg)"].min()
        textpos = ["inside" if v > 1.5 * min_val else "outside" for v in top10_geral["Total (kg)"]]
        fig1.update_traces(text=top10_geral["Nome Popular"], textposition=textpos, textfont=dict(size=12))
    fig1.update_yaxes(automargin=True, title=None)
    fig1.update_xaxes(automargin=True, title="Peso (kg)")
    fig1.update_layout(margin=dict(l=left_margin, r=10, t=10, b=30))
    st.plotly_chart(fig1, use_container_width=True)

with right:
    t = top10_geral.copy()
    t.insert(0, "Nº", range(1, len(t) + 1))
    t["Total (kg)"] = t["Total (kg)"].apply(fmt_kg)
    st.dataframe(t.set_index("Nº"), use_container_width=True, height=400)

# ============================================================================
# FILTROS GLOBAIS
# ============================================================================
resex_lista = sorted(df["Resex_label"].dropna().unique().tolist())
meses_lista = sorted(df["Mês"].dropna().unique().tolist())

col_f1, col_f2, col_f3 = st.columns([1.4, 1.6, 2])
with col_f1:
    default_idx = resex_lista.index("Soure") if "Soure" in resex_lista else 0
    resex_global = st.selectbox("RESEX", resex_lista, index=default_idx)
with col_f2:
    meses_default = ["Maio"] if "Maio" in meses_lista else meses_lista[:1]
    meses_global = st.multiselect("Meses", meses_lista, default=meses_default)
with col_f3:
    n_regs = len(df[(df["Resex_label"] == resex_global) & (df["Mês"].isin(meses_global))])
    st.write("")
    st.write(f"**Registros filtrados:** {fmt_int(n_regs)}")

# ============================================================================
# MAPA RESEXs — leve, sem números, Baia do Tubarão garantida
# ============================================================================
section("Mapa das RESEXs")

# Coordenadas oficiais
coords_resex = {
    "Soure": (-0.567944, -48.477072),
    "Mocapajuba": (-0.774368, -48.044237),
    "Arapiranga Tromaí": (-1.203442, -45.895965),
    "Itapetininga": (-2.354133, -44.696923),
    "Baia do Tubarão": (-2.448243, -43.753105),
}

# --- mapa central ---
lat_centro = sum(lat for lat, _ in coords_resex.values()) / len(coords_resex)
lon_centro = sum(lon for _, lon in coords_resex.values()) / len(coords_resex)

# --- TIPOS DE MAPA (basemap) ---
TILESETS = {
    "OpenStreetMap": "OpenStreetMap",           # OSM padrão
    "Esri Satélite": "Esri.WorldImagery",
}
# seletor no UI
basemap_label = st.selectbox("Tipo de mapa (basemap)", list(TILESETS.keys()), index=1)
tiles_selected = TILESETS[basemap_label]

# cria o mapa com o tiles escolhido
m = folium.Map(location=[lat_centro, lon_centro], zoom_start=6, tiles=tiles_selected)

for resex, (lat, lon) in coords_resex.items():
    folium.Marker(
        [lat, lon],
        popup=f"<b>RESEX:</b> {resex}",
        icon=folium.Icon(color="blue", icon="leaf", prefix="fa")
    ).add_to(m)

st_folium(m, height=380, use_container_width=True)

# ============================================================================
# ANÁLISE POR RESEX E MÊS — BARRAS EM DUAS COLUNAS
# ============================================================================
section("Análise por RESEX e Mês")

df_filtrado = df[(df["Resex_label"] == resex_global) & (df["Mês"].isin(meses_global))]

if df_filtrado.empty:
    st.warning(f"Sem dados para **{resex_global}** em {', '.join(meses_global)}.")
else:
    top10_filt = (df_filtrado.groupby("Nome Popular")["Total (kg)"]
                  .sum().sort_values(ascending=False).head(10).reset_index())
    total_sel = top10_filt["Total (kg)"].sum()

    if total_sel == 0:
        st.info("Os valores somados são zero para o filtro escolhido.")
    else:
        top10_filt["% do total"] = 100 * top10_filt["Total (kg)"] / total_sel

        max_lab_len2 = top10_filt["Nome Popular"].astype(str).str.len().max()
        left_margin2 = max(100, min(16 + int(max_lab_len2 * 7.2), 260))

        # Cria duas colunas para gráfico e tabela
        g1, g2 = st.columns([1.2, 1])

        with g1:
            fig = px.bar(
                top10_filt, x="Total (kg)", y="Nome Popular",
                orientation="h",
                title=f"Top 10 — {resex_global} ({', '.join(meses_global)})",
                template="none",
                color_discrete_sequence=[THEME["brand"]],
                text=top10_filt["% do total"].map(lambda v: f"{v:.1f}%")
            )
            min_val = top10_filt["Total (kg)"].min()
            textpos = ["inside" if v > 1.5 * min_val else "outside" for v in top10_filt["Total (kg)"]]
            fig.update_traces(textposition=textpos,
                              hovertemplate="<b>%{y}</b><br>Peso: %{x:.2f} kg<br>Participação: %{text}")
            fig.update_yaxes(automargin=True, title=None)
            fig.update_xaxes(automargin=True, title="Peso (kg)")
            fig.update_layout(height=420, margin=dict(l=left_margin2, r=10, t=40, b=30))
            st.plotly_chart(fig, use_container_width=True)

        with g2:
            tt = top10_filt.copy()
            tt.insert(0, "Nº", range(1, len(tt) + 1))
            tt["Total (kg)"] = tt["Total (kg)"].map(fmt_kg)
            tt["% do total"] = tt["% do total"].map(lambda v: f"{v:.1f}%")
            st.dataframe(tt.set_index("Nº"), use_container_width=True, height=420)

# ============================================================================
# SÉRIE TEMPORAL — labels em português + fonte ajustada
# ============================================================================
section("Evolução Temporal — Top N da RESEX selecionada")

# Nomes customizáveis dos eixos
nome_eixo_x = "Mês / Ano"
nome_eixo_y = "Peso Total (kg)"

# Tradução de meses para português
mapa_meses_pt = {
    "Jan": "Jan", "Feb": "Fev", "Mar": "Mar", "Apr": "Abr", "May": "Mai", "Jun": "Jun",
    "Jul": "Jul", "Aug": "Ago", "Sep": "Set", "Oct": "Out", "Nov": "Nov", "Dec": "Dez"
}

top_n = st.slider("Top N espécies", 3, 15, 5,
                  help="Ranking por soma de peso na RESEX selecionada.")

df_reserva = df[df["Resex_label"] == resex_global]
if df_reserva.empty:
    st.info("Sem dados para a RESEX selecionada.")
else:
    top_especies = df_reserva.groupby("Nome Popular")["Total (kg)"].sum().nlargest(top_n).index
    df_time = (df_reserva[df_reserva["Nome Popular"].isin(top_especies)]
               .groupby(["Data_Mensal", "Nome Popular"], as_index=False)["Total (kg)"].sum())

    # Gera gráfico
    fig_time = px.line(
        df_time,
        x="Data_Mensal",
        y="Total (kg)",
        color="Nome Popular",
        markers=True,
        labels={"Data_Mensal": nome_eixo_x, "Total (kg)": nome_eixo_y, "Nome Popular": "Espécie"}
    )

    # Ajuste do layout: meses em português, fonte uniforme, legenda embaixo
    fig_time.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y",
        automargin=True,
        tickfont=dict(family="Arial", size=12, color="#0F172A"),
        ticklabelmode="period"
    )
    # Substitui os meses para português
    fig_time.for_each_xaxis(lambda axis: axis.update(
        ticktext=[mapa_meses_pt.get(t[:3], t) for t in axis.ticktext] if axis.ticktext else None
    ))

    fig_time.update_yaxes(
        automargin=True,
        title_font=dict(family="Arial", size=14, color="#0F172A"),
        tickfont=dict(family="Arial", size=12, color="#0F172A")
    )
    fig_time.update_layout(
        xaxis_title_font=dict(family="Arial", size=14, color="#0F172A"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.35,
                    xanchor="center", x=0.5, title=None,
                    font=dict(family="Arial", size=12, color="#0F172A")),
        hovermode="x unified",
        margin=dict(l=20, r=20, t=20, b=90),
        height=440,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF"
    )

    st.plotly_chart(fig_time, use_container_width=True)

# ============================================================================
# Rodapé
# ============================================================================
st.write("")
st.caption("© Observatório da Costa Amazônica — Oca Social")
