"""
Dashboard décisionnel — Olist Brazilian E-Commerce
Phase 5 — Data-Driven Decision Making
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ── CONFIG ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Olist Analytics",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS GLOBAL ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

/* Reset & base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #e2e8f0;
}

.stApp {
    background-color: #0f1117;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #161b27 !important;
    border-right: 1px solid #1e2535;
}

[data-testid="stSidebar"] * {
    color: #94a3b8 !important;
}

[data-testid="stSidebar"] .stRadio label {
    color: #94a3b8 !important;
    font-size: 13px !important;
    padding: 6px 0 !important;
}

[data-testid="stSidebar"] .stRadio [data-checked="true"] label {
    color: #f1f5f9 !important;
    font-weight: 500 !important;
}

/* Titres */
h1 {
    font-size: 22px !important;
    font-weight: 600 !important;
    color: #f1f5f9 !important;
    letter-spacing: -0.3px !important;
    margin-bottom: 2px !important;
}

h2 {
    font-size: 15px !important;
    font-weight: 500 !important;
    color: #cbd5e1 !important;
    letter-spacing: 0px !important;
}

h3 {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #94a3b8 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: #161b27;
    border: 1px solid #1e2535;
    border-radius: 10px;
    padding: 18px 20px !important;
}

[data-testid="stMetricLabel"] {
    font-size: 11px !important;
    font-weight: 500 !important;
    color: #64748b !important;
    text-transform: uppercase !important;
    letter-spacing: 0.6px !important;
}

[data-testid="stMetricValue"] {
    font-size: 26px !important;
    font-weight: 600 !important;
    color: #f1f5f9 !important;
    font-family: 'DM Mono', monospace !important;
}

[data-testid="stMetricDelta"] {
    font-size: 11px !important;
}

/* Divider */
hr {
    border: none;
    border-top: 1px solid #1e2535 !important;
    margin: 18px 0 !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background: #161b27 !important;
    border: 1px solid #1e2535 !important;
    border-radius: 10px !important;
}

/* Slider */
[data-testid="stSlider"] * {
    color: #94a3b8 !important;
}

/* Expander */
[data-testid="stExpander"] {
    background: #161b27 !important;
    border: 1px solid #1e2535 !important;
    border-radius: 8px !important;
}

/* Info / success / warning boxes */
[data-testid="stAlert"] {
    border-radius: 8px !important;
    border: 1px solid #1e2535 !important;
    font-size: 13px !important;
}

/* Caption */
.stCaption {
    color: #475569 !important;
    font-size: 11px !important;
}

/* Remove padding top */
.block-container {
    padding-top: 56px !important;
    padding-bottom: 40px !important;
}

/* Tabs */
button[data-baseweb="tab"] {
    font-size: 13px !important;
    color: #64748b !important;
}
</style>
""", unsafe_allow_html=True)

# ── PLOTLY THEME ──────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans', color='#94a3b8', size=12),
    margin=dict(l=8, r=8, t=32, b=8),
    xaxis=dict(
        gridcolor='#1e2535',
        linecolor='#1e2535',
        tickcolor='#1e2535',
        zerolinecolor='#1e2535',
    ),
    yaxis=dict(
        gridcolor='#1e2535',
        linecolor='#1e2535',
        tickcolor='#1e2535',
        zerolinecolor='#1e2535',
    ),
    legend=dict(
        bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8', size=12),
        orientation='h',
        yanchor='bottom',
        y=1.02
    ),
    coloraxis_colorbar=dict(
        tickfont=dict(color='#94a3b8'),
        titlefont=dict(color='#94a3b8')
    )
)

# Palette
C = {
    'blue':    '#3b82f6',
    'green':   '#22c55e',
    'amber':   '#f59e0b',
    'red':     '#ef4444',
    'slate':   '#64748b',
    'indigo':  '#6366f1',
    'teal':    '#14b8a6',
    'Très Fidèles':  '#22c55e',
    'Fidèles':       '#3b82f6',
    'À Réactiver':   '#f59e0b',
    'Perdus':        '#ef4444',
}

# ── CHEMINS ───────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')

# ── CHARGEMENT ────────────────────────────────────────────────
@st.cache_data
def load_all():
    kpis       = pd.read_csv(os.path.join(DATA_DIR, 'dashboard_kpis.csv')).iloc[0]
    monthly    = pd.read_csv(os.path.join(DATA_DIR, 'dashboard_monthly.csv'))
    rfm_seg    = pd.read_csv(os.path.join(DATA_DIR, 'dashboard_rfm_segments.csv'))
    rfm_prof   = pd.read_csv(os.path.join(DATA_DIR, 'dashboard_rfm_profile.csv'))
    categories = pd.read_csv(os.path.join(DATA_DIR, 'dashboard_categories.csv'))
    geo        = pd.read_csv(os.path.join(DATA_DIR, 'dashboard_geo.csv'))
    shap_df    = pd.read_csv(os.path.join(DATA_DIR, 'dashboard_shap_importance.csv'))
    models_df  = pd.read_csv(os.path.join(DATA_DIR, 'dashboard_model_comparison.csv'))
    return kpis, monthly, rfm_seg, rfm_prof, categories, geo, shap_df, models_df

kpis, monthly, rfm_seg, rfm_prof, categories, geo, shap_df, models_df = load_all()

# ── Traduction catégories produits EN → FR ────────────────────
CAT_FR = {
    'health_beauty':              'Santé & Beauté',
    'bed_bath_table':             'Literie & Bain',
    'sports_leisure':             'Sports & Loisirs',
    'furniture_decor':            'Meubles & Déco',
    'computers_accessories':      'Informatique',
    'housewares':                 'Articles Ménagers',
    'watches_gifts':              'Montres & Cadeaux',
    'telephony':                  'Téléphonie',
    'garden_tools':               'Jardinage',
    'auto':                       'Auto & Moto',
    'toys':                       'Jouets',
    'cool_stuff':                 'Tendances',
    'perfumery':                  'Parfumerie',
    'baby':                       'Puériculture',
    'electronics':                'Électronique',
    'stationery':                 'Papeterie',
    'fashion_bags_accessories':   'Sacs & Accessoires',
    'office_furniture':           'Mobilier Bureau',
    'books_general_interest':     'Livres',
    'food_drink':                 'Alimentation',
    'musical_instruments':        'Instruments Musique',
    'construction_tools_safety':  'Bricolage & Sécurité',
    'pet_shop':                   'Animalerie',
    'art':                        'Art',
    'home_appliances':            'Électroménager',
    'kitchen_dining_laundry_garden_furniture': 'Cuisine & Jardin',
    'luggage_accessories':        'Bagagerie',
    'fashion_male_clothing':      'Mode Homme',
    'fashion_female_clothing':    'Mode Femme',
    'small_appliances':           'Petit Électroménager',
    'consoles_games':             'Consoles & Jeux',
    'audio':                      'Audio',
    'books_technical':            'Livres Techniques',
    'party_supplies':             'Fêtes & Événements',
    'market_place':               'Marketplace',
    'home_comfort':               'Confort Maison',
    'fixed_telephony':            'Téléphonie Fixe',
    'industry_commerce_and_business': 'Commerce & Industrie',
    'drinks':                     'Boissons',
    'fashion_shoes':              'Chaussures',
    'agro_industry_and_commerce': 'Agro-Industrie',
    'tablets_printing_image':     'Tablettes & Photo',
    'la_cuisine':                 'Cuisine',
    'fashion_underwear_beach':    'Lingerie & Plage',
    'fashion_sport':              'Mode Sport',
    'home_comfort_2':             'Confort Maison 2',
    'flowers':                    'Fleurs',
    'christmas_supplies':         'Noël',
    'food':                       'Alimentation',
    'diapers_and_hygiene':        'Hygiène & Couches',
    'dvds_blu_ray':               'DVD & Blu-ray',
    'cine_photo':                 'Cinéma & Photo',
    'other':                      'Autres',
}

def translate_cat(name):
    if not isinstance(name, str):
        return name
    return CAT_FR.get(name.lower(), name.replace('_', ' ').title())

categories['product_category_name_english'] = (
    categories['product_category_name_english'].apply(translate_cat)
)

# ── Renommage des segments dans les dataframes ────────────────
# Les CSV stockent encore les anciens noms produits par le notebook Phase 3
SEG_RENAME = {
    'Champions': 'Très Fidèles',
    'Fidèles':   'Fidèles',
    'À risque':  'À Réactiver',
    'Inactifs':  'Perdus',
}
rfm_prof['segment'] = rfm_prof['segment'].map(SEG_RENAME).fillna(rfm_prof['segment'])
rfm_seg['segment']  = rfm_seg['segment'].map(SEG_RENAME).fillna(rfm_seg['segment'])

SEG_ORDER = ['Très Fidèles', 'Fidèles', 'À Réactiver', 'Perdus']

# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div style='padding:8px 0 20px 0'>"
        "<div style='font-size:18px;font-weight:600;color:#f1f5f9;letter-spacing:-0.3px'>Olist Analytics</div>"
        "<div style='font-size:11px;color:#475569;margin-top:2px'>Brazilian E-Commerce · 2016–2018</div>"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='font-size:10px;font-weight:500;color:#475569;"
        "text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px'>Navigation</div>",
        unsafe_allow_html=True
    )

    vue_idx = st.radio(
        "Navigation",
        options=list(range(5)),
        format_func=lambda i: [
            "Direction — KPIs Globaux",
            "Marketing — Segments Clients",
            "Opérations — Livraisons",
            "Produits — Catégories",
            "Modèle IA — Prédictions",
        ][i],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("<div style='margin-top:24px'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='font-size:11px;color:#334155;line-height:2'>"
        f"Commandes &nbsp;<span style='color:#64748b;font-family:DM Mono,monospace'>{int(kpis['nb_commandes']):,}</span><br>"
        f"Clients &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#64748b;font-family:DM Mono,monospace'>{int(kpis['nb_clients_uniques']):,}</span><br>"
        f"Période &nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#64748b'>2016 – 2018</span>"
        f"</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='position:absolute;bottom:20px;font-size:10px;color:#1e2535'></div>",
        unsafe_allow_html=True
    )


# ── HELPER : card HTML ────────────────────────────────────────
def card(content_html, padding="18px 20px"):
    st.markdown(
        f"<div style='background:#161b27;border:1px solid #1e2535;"
        f"border-radius:10px;padding:{padding};margin-bottom:0'>"
        f"{content_html}</div>",
        unsafe_allow_html=True
    )

def section(title):
    st.markdown(
        f"<div style='font-size:14px;font-weight:600;color:#cbd5e1;"
        f"letter-spacing:-0.2px;margin:32px 0 14px 0;"
        f"padding-bottom:8px;border-bottom:1px solid #1e2535'>{title}</div>",
        unsafe_allow_html=True
    )

def page_header(title, subtitle=""):
    st.markdown(
        f"<div style='margin-bottom:28px'>"
        f"<div style='font-size:22px;font-weight:600;color:#f1f5f9;"
        f"letter-spacing:-0.4px'>{title}</div>"
        f"<div style='font-size:13px;color:#64748b;margin-top:4px'>{subtitle}</div>"
        f"</div>",
        unsafe_allow_html=True
    )

def apply_layout(fig, height=380, extra=None):
    layout = dict(PLOTLY_LAYOUT)
    layout['height'] = height
    if extra:
        layout.update(extra)
    fig.update_layout(**layout)
    return fig


# ════════════════════════════════════════════════════════════
# VUE 0 — DIRECTION
# ════════════════════════════════════════════════════════════
if vue_idx == 0:

    page_header(
        "Performance Globale",
        "Tableau de bord exécutif — KPIs primaires et secondaires"
    )

    # ── KPIs row 1 ──────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Chiffre d'Affaires", f"R$ {kpis['ca_total']:,.0f}")
    with c2:
        st.metric("Panier Moyen (AOV)", f"R$ {kpis['aov']:.2f}",
                  delta="Cible R$ 150")
    with c3:
        score = kpis['review_score_moyen']
        st.metric("Score Satisfaction", f"{score:.2f} / 5",
                  delta="Cible 4.0",
                  delta_color="normal" if score >= 4.0 else "inverse")
    with c4:
        ret = kpis['taux_retention']
        st.metric("Taux de Rétention", f"{ret:.1f}%",
                  delta="Cible 15%",
                  delta_color="normal" if ret >= 15 else "inverse")

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    c5, c6, c7, c8 = st.columns(4)
    with c5:
        st.metric("Commandes Livrées", f"{int(kpis['nb_commandes']):,}")
    with c6:
        st.metric("Clients Uniques", f"{int(kpis['nb_clients_uniques']):,}")
    with c7:
        ontime = kpis['taux_livraison_temps']
        st.metric("Livraisons à Temps", f"{ontime:.1f}%",
                  delta="Cible 90%",
                  delta_color="normal" if ontime >= 90 else "inverse")
    with c8:
        cancel = kpis['taux_annulation']
        st.metric("Taux d'Annulation", f"{cancel:.1f}%",
                  delta="Cible < 3%",
                  delta_color="inverse" if cancel > 3 else "normal")

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    # ── Graphiques principaux ────────────────────────────────
    col_l, col_r = st.columns([3, 2])

    with col_l:
        section("Évolution Mensuelle")
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=monthly['order_month'], y=monthly['ca'],
            name="CA (BRL)",
            marker_color=C['blue'],
            marker_opacity=0.8,
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=monthly['order_month'], y=monthly['nb_commandes'],
            name="Commandes",
            line=dict(color=C['amber'], width=2),
            mode='lines+markers',
            marker=dict(size=4)
        ), secondary_y=True)
        fig.update_xaxes(tickangle=-45, tickfont=dict(size=10))
        fig.update_yaxes(title_text="CA (BRL)", secondary_y=False,
                         title_font=dict(size=11))
        fig.update_yaxes(title_text="Commandes", secondary_y=True,
                         title_font=dict(size=11))
        apply_layout(fig, height=340,
                     extra={'hovermode': 'x unified',
                            'margin': dict(l=8, r=8, t=16, b=60)})
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        section("Contexte & Enjeux")
        card(
            "<div style='font-size:12px;color:#64748b;line-height:1.9'>"
            "<span style='font-family:DM Mono,monospace;color:#3b82f6;font-size:13px'>96%</span>"
            " des clients n'achetent qu'une seule fois<br>"
            "<span style='font-family:DM Mono,monospace;color:#f59e0b;font-size:13px'>10%</span>"
            " des commandes sont livrees en retard<br>"
            "<span style='font-family:DM Mono,monospace;color:#22c55e;font-size:13px'>+8–12%</span>"
            " de CA projete sur 12 mois si retention +5%"
            "</div>",
            padding="20px 22px"
        )

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        section("Arbre des KPIs")
        card(
            "<div style='font-size:11px;color:#64748b;"
            "font-family:DM Mono,monospace;line-height:2.1'>"
            "<span style='color:#94a3b8'>CA Total</span><br>"
            "&nbsp;&nbsp;├── <span style='color:#3b82f6'>Panier Moyen (AOV) (AOV)</span><br>"
            "&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;├── Prix produit<br>"
            "&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;└── Frais de port<br>"
            "&nbsp;&nbsp;├── <span style='color:#3b82f6'>Volume Commandes</span><br>"
            "&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;├── Nouveaux clients<br>"
            "&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;└── Clients recurrents<br>"
            "&nbsp;&nbsp;└── <span style='color:#3b82f6'>Satisfaction</span><br>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── Delai livraison<br>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── Taux de retard"
            "</div>",
            padding="18px 20px"
        )

    # ── Satisfaction mensuelle ───────────────────────────────
    section("Satisfaction & Retards — Évolution Mensuelle")
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(go.Scatter(
        x=monthly['order_month'], y=monthly['review_moyen'],
        name="Score Moyen",
        line=dict(color=C['green'], width=2),
        mode='lines+markers', marker=dict(size=4)
    ), secondary_y=False)
    fig2.add_trace(go.Scatter(
        x=monthly['order_month'], y=monthly['taux_retard'],
        name="Taux Retard (%)",
        line=dict(color=C['red'], width=2, dash='dot'),
        mode='lines+markers', marker=dict(size=4)
    ), secondary_y=True)
    fig2.add_hline(
        y=4.0, line_dash="dash",
        line_color="#22c55e", opacity=0.4,
        annotation_text="Cible 4.0",
        annotation_font=dict(color="#22c55e", size=10),
        secondary_y=False
    )
    fig2.update_xaxes(tickangle=-45, tickfont=dict(size=10))
    fig2.update_yaxes(title_text="Score (1-5)", secondary_y=False,
                      range=[3, 5.2], title_font=dict(size=11))
    fig2.update_yaxes(title_text="Retard (%)", secondary_y=True,
                      title_font=dict(size=11))
    apply_layout(fig2, height=300,
                 extra={'hovermode': 'x unified',
                        'margin': dict(l=8, r=8, t=16, b=60)})
    st.plotly_chart(fig2, use_container_width=True)


# ════════════════════════════════════════════════════════════
# VUE 1 — MARKETING
# ════════════════════════════════════════════════════════════
elif vue_idx == 1:

    page_header(
        "Segmentation Clients",
        "Analyse RFM — Récence, Fréquence, Valeur Monétaire"
    )

    # ── Cartes segments ─────────────────────────────────────
    section("Profil des 4 Segments")
    cols = st.columns(4)

    actions = {
        'Très Fidèles': 'Programme VIP · Récompenses · Parrainage',
        'Fidèles':      'Cross-sell · Enquête satisfaction · Accès anticipé',
        'À Réactiver':  'Email win-back · Promotion -15% · Urgence',
        'Perdus':       'Campagne réactivation · Offre dernière chance',
    }
    descriptions = {
        'Très Fidèles': 'Acheteurs récents, fréquents et à haute valeur.',
        'Fidèles':      'Plusieurs achats, bonne valeur, engagement correct.',
        'À Réactiver':  'Bons clients devenus inactifs depuis trop longtemps.',
        'Perdus':       'Un seul achat, faible valeur, peu de potentiel.',
    }

    for col, (_, row) in zip(cols, rfm_prof.iterrows()):
        seg = row['segment']
        color = C[seg]
        with col:
            st.markdown(
                f"<div style='background:#161b27;border:1px solid #1e2535;"
                f"border-top:2px solid {color};border-radius:10px;"
                f"padding:18px 16px;height:100%'>"
                f"<div style='font-size:13px;font-weight:600;color:{color};"
                f"margin-bottom:6px'>{seg}</div>"
                f"<div style='font-size:11px;color:#475569;margin-bottom:12px'>"
                f"{descriptions[seg]}</div>"
                f"<div style='font-family:DM Mono,monospace;font-size:12px;"
                f"color:#94a3b8;line-height:2'>"
                f"<span style='color:#475569'>Clients</span>&nbsp;&nbsp;"
                f"{int(row['nb_clients']):,}"
                f"&nbsp;<span style='color:#334155'>({row['pct_clients']:.1f}%)</span><br>"
                f"<span style='color:#475569'>Revenue</span>&nbsp;"
                f"{row['pct_revenue']:.1f}% total<br>"
                f"<span style='color:#475569'>Panier</span>&nbsp;&nbsp;&nbsp;"
                f"R$ {row['monetary_moy']:.0f}<br>"
                f"<span style='color:#475569'>Recence</span>&nbsp;"
                f"{row['recency_moy']:.0f}j"
                f"</div>"
                f"<div style='margin-top:12px;padding-top:10px;"
                f"border-top:1px solid #1e2535;font-size:10px;"
                f"color:#334155'>{actions[seg]}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    # ── Donut ────────────────────────────────────────────────
    with col_a:
        section("Répartition des Clients par Segment")
        fig_d = go.Figure(go.Pie(
            labels=rfm_prof['segment'],
            values=rfm_prof['nb_clients'],
            hole=0.62,
            marker_colors=[C[s] for s in rfm_prof['segment']],
            textinfo='percent',
            textfont=dict(size=12, color='#0f1117'),
            hovertemplate='%{label}<br>%{value:,} clients<br>%{percent}<extra></extra>',
            sort=False
        ))
        total = int(rfm_prof['nb_clients'].sum())
        fig_d.add_annotation(
            text=f"<b>{total:,}</b><br><span style='font-size:10px'>clients</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color='#f1f5f9')
        )
        apply_layout(fig_d, height=340,
                     extra={'showlegend': True,
                            'margin': dict(l=8, r=8, t=16, b=8)})
        st.plotly_chart(fig_d, use_container_width=True)

    # ── Revenue ──────────────────────────────────────────────
    with col_b:
        section("Chiffre d'Affaires par Segment")
        fig_b = go.Figure(go.Bar(
            x=rfm_prof['segment'],
            y=rfm_prof['monetary_total'],
            marker_color=[C[s] for s in rfm_prof['segment']],
            marker_opacity=0.85,
            text=[f"R$ {v:,.0f}" for v in rfm_prof['monetary_total']],
            textposition='outside',
            textfont=dict(size=11, color='#94a3b8'),
            hovertemplate='%{x}<br>R$ %{y:,.0f}<extra></extra>'
        ))
        apply_layout(fig_b, height=340,
                     extra={'showlegend': False,
                            'yaxis': dict(
                                title="Chiffre d'affaires (BRL)",
                                gridcolor='#1e2535',
                                title_font=dict(size=11)
                            ),
                            'margin': dict(l=8, r=8, t=16, b=8)})
        st.plotly_chart(fig_b, use_container_width=True)

    # ── Scatter RFM ──────────────────────────────────────────
    section("Distribution RFM — Récence vs Valeur (échantillon 3 000 clients)")
    rfm_sample = rfm_seg.sample(min(3000, len(rfm_seg)), random_state=42)
    fig_s = px.scatter(
        rfm_sample, x='recency', y='monetary',
        color='segment',
        color_discrete_map=C,
        opacity=0.5,
        labels={
            'recency':  'Récence (jours depuis dernier achat)',
            'monetary': 'Valeur totale dépensée (BRL)',
            'segment':  'Segment client'
        },
        category_orders={'segment': SEG_ORDER},
        hover_data=['frequency']
    )
    fig_s.update_traces(marker=dict(size=5))
    apply_layout(fig_s, height=400,
                 extra={'margin': dict(l=8, r=8, t=16, b=8)})
    st.plotly_chart(fig_s, use_container_width=True)


# ════════════════════════════════════════════════════════════
# VUE 2 — OPERATIONS
# ════════════════════════════════════════════════════════════
elif vue_idx == 2:

    page_header(
        "Performance Logistique",
        "Analyse des délais et retards de livraison par région"
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        ontime = kpis['taux_livraison_temps']
        st.metric("Livraisons à Temps", f"{ontime:.1f}%",
                  delta="Cible 90%",
                  delta_color="normal" if ontime >= 90 else "inverse")
    with c2:
        st.metric("Délai Médian", f"{kpis['delai_moyen_jours']:.0f} jours")
    with c3:
        st.metric("Score Satisfaction", f"{kpis['review_score_moyen']:.2f} / 5")
    with c4:
        st.metric("Commandes Analysées", f"{int(kpis['nb_commandes']):,}")

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)

    with col_l:
        section("Taux de Retard par État (Brésil)")
        geo_clean = geo.dropna(subset=['lat', 'lon'])
        fig_map = px.scatter_geo(
            geo_clean, lat='lat', lon='lon',
            size='nb_commandes',
            color='taux_retard',
            hover_name='customer_state',
            hover_data={
                'nb_commandes': True,
                'taux_retard': ':.1f',
                'delai_moyen': ':.1f',
                'review_moyen': ':.2f',
                'lat': False, 'lon': False
            },
            color_continuous_scale=[
                [0, '#22c55e'], [0.5, '#f59e0b'], [1, '#ef4444']
            ],
            size_max=38,
            scope='south america',
            labels={
                'taux_retard':  'Taux de retard (%)',
                'nb_commandes': 'Nb commandes',
                'delai_moyen':  'Délai moyen (j)',
                'review_moyen': 'Score satisfaction'
            }
        )
        fig_map.update_layout(
            **{k: v for k, v in PLOTLY_LAYOUT.items()
               if k not in ['xaxis', 'yaxis', 'margin']},
            height=420,
            margin=dict(l=0, r=0, t=16, b=0),
            geo=dict(
                bgcolor='rgba(0,0,0,0)',
                landcolor='#161b27',
                oceancolor='#0f1117',
                lakecolor='#0f1117',
                coastlinecolor='#1e2535',
                countrycolor='#1e2535',
            )
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with col_r:
        section("Top 10 États — Taux de Retard")
        top_retard = geo.sort_values('taux_retard', ascending=True).tail(10)
        bar_colors = [
            C['red'] if v > 20 else
            C['amber'] if v > 10 else
            C['green']
            for v in top_retard['taux_retard']
        ]
        fig_r = go.Figure(go.Bar(
            x=top_retard['taux_retard'],
            y=top_retard['customer_state'],
            orientation='h',
            marker_color=bar_colors,
            marker_opacity=0.85,
            text=[f"{v:.1f}%" for v in top_retard['taux_retard']],
            textposition='outside',
            textfont=dict(size=11, color='#94a3b8'),
            hovertemplate='%{y} — %{x:.1f}%<extra></extra>'
        ))
        apply_layout(fig_r, height=420,
                     extra={
                         'showlegend': False,
                         'xaxis': dict(
                             title='Taux de retard (%)',
                             gridcolor='#1e2535',
                             title_font=dict(size=11)
                         ),
                         'margin': dict(l=8, r=50, t=16, b=8)
                     })
        st.plotly_chart(fig_r, use_container_width=True)

    section("Délai Moyen vs Score Satisfaction — par État")
    fig_del = px.scatter(
        geo, x='delai_moyen', y='review_moyen',
        size='nb_commandes',
        color='taux_retard',
        hover_name='customer_state',
        color_continuous_scale=[
            [0, '#22c55e'], [0.5, '#f59e0b'], [1, '#ef4444']
        ],
        size_max=35,
        text='customer_state',
        labels={
            'delai_moyen':  'Délai moyen (jours)',
            'review_moyen': 'Score satisfaction',
            'taux_retard':  'Taux de retard (%)',
            'nb_commandes': 'Nb commandes'
        }
    )
    fig_del.update_traces(
        textposition='top center',
        textfont=dict(size=9, color='#64748b')
    )
    fig_del.add_hline(
        y=4.0, line_dash='dash',
        line_color='#22c55e', opacity=0.4,
        annotation_text="Cible score 4.0",
        annotation_font=dict(size=10, color='#22c55e')
    )
    apply_layout(fig_del, height=440,
                 extra={'margin': dict(l=8, r=8, t=16, b=8)})
    st.plotly_chart(fig_del, use_container_width=True)


# ════════════════════════════════════════════════════════════
# VUE 3 — PRODUITS
# ════════════════════════════════════════════════════════════
elif vue_idx == 3:

    page_header(
        "Analyse par Catégorie",
        "Performance par catégorie — Chiffre d'affaires, Satisfaction, Délais"
    )

    nb_cat = st.slider("Nombre de categories", 5, 20, 15,
                       label_visibility="collapsed")
    st.markdown(
        f"<div style='font-size:11px;color:#475569;margin:-8px 0 20px 0'>"
        f"Affichage des {nb_cat} premières catégories par chiffre d'affaires</div>",
        unsafe_allow_html=True
    )

    cat_display = categories.head(nb_cat).copy()

    col_a, col_b = st.columns(2)

    with col_a:
        section("Chiffre d'Affaires par Catégorie")
        cat_r = cat_display.sort_values('revenue', ascending=True)
        fig_rv = go.Figure(go.Bar(
            x=cat_r['revenue'],
            y=cat_r['product_category_name_english'],
            orientation='h',
            marker_color=C['blue'],
            marker_opacity=0.8,
            text=[f"R$ {v:,.0f}" for v in cat_r['revenue']],
            textposition='outside',
            textfont=dict(size=10, color='#94a3b8'),
            hovertemplate='%{y}<br>R$ %{x:,.0f}<extra></extra>'
        ))
        apply_layout(fig_rv, height=520,
                     extra={
                         'showlegend': False,
                         'xaxis': dict(
                             title="Chiffre d'affaires (BRL)",
                             gridcolor='#1e2535',
                             title_font=dict(size=11)
                         ),
                         'margin': dict(l=8, r=80, t=16, b=8)
                     })
        st.plotly_chart(fig_rv, use_container_width=True)

    with col_b:
        section("Score de Satisfaction Moyen")
        cat_s = cat_display.sort_values('review_moyen', ascending=True)
        bar_c = [
            C['green'] if v >= 4.0 else
            C['amber'] if v >= 3.5 else
            C['red']
            for v in cat_s['review_moyen']
        ]
        fig_sc = go.Figure(go.Bar(
            x=cat_s['review_moyen'],
            y=cat_s['product_category_name_english'],
            orientation='h',
            marker_color=bar_c,
            marker_opacity=0.85,
            text=[f"{v:.2f}" for v in cat_s['review_moyen']],
            textposition='outside',
            textfont=dict(size=10, color='#94a3b8'),
            hovertemplate='%{y}<br>Score : %{x:.2f}<extra></extra>'
        ))
        fig_sc.add_vline(
            x=4.0, line_dash='dash',
            line_color='#22c55e', opacity=0.4,
            annotation_text="Cible 4.0",
            annotation_font=dict(size=10, color='#22c55e'),
            annotation_position="top"
        )
        apply_layout(fig_sc, height=520,
                     extra={
                         'showlegend': False,
                         'xaxis': dict(
                             title='Score satisfaction (1-5)',
                             range=[0, 5.8],
                             gridcolor='#1e2535',
                             title_font=dict(size=11)
                         ),
                         'margin': dict(l=8, r=60, t=16, b=8)
                     })
        st.plotly_chart(fig_sc, use_container_width=True)

    section("Matrice CA × Retard × Satisfaction")
    fig_bub = px.scatter(
        cat_display,
        x='taux_retard', y='review_moyen',
        size='nb_commandes',
        color='review_moyen',
        color_continuous_scale=[
            [0, '#ef4444'], [0.5, '#f59e0b'], [1, '#22c55e']
        ],
        size_max=45,
        text='product_category_name_english',
        labels={
            'taux_retard':  'Taux de retard (%)',
            'review_moyen': 'Score satisfaction',
            'nb_commandes': 'Nb commandes'
        },
        hover_data={'revenue': ':,.0f', 'nb_commandes': True}
    )
    fig_bub.update_traces(
        textposition='top center',
        textfont=dict(size=9, color='#64748b')
    )
    fig_bub.add_hline(
        y=4.0, line_dash='dash',
        line_color='#22c55e', opacity=0.4,
        annotation_text="Cible satisfaction",
        annotation_font=dict(size=10, color='#22c55e')
    )
    apply_layout(fig_bub, height=480,
                 extra={'margin': dict(l=8, r=8, t=16, b=8)})
    st.plotly_chart(fig_bub, use_container_width=True)


# ════════════════════════════════════════════════════════════
# VUE 4 — MODELE IA
# ════════════════════════════════════════════════════════════
elif vue_idx == 4:

    page_header(
        "Modèle Prédictif",
        "Classification binaire — prédiction des avis négatifs (score ≤ 2)"
    )

    # ── Tableau modeles ──────────────────────────────────────
    section("Comparaison des 3 Modèles Entraînés")
    col_t, col_m = st.columns([3, 1])

    with col_t:
        if 'Modèle' not in models_df.columns and 'model' in models_df.columns:
            models_df.rename(columns={'model': 'Modele'}, inplace=True)
        elif 'Modèle' in models_df.columns:
            models_df.rename(columns={'Modèle': 'Modele'}, inplace=True)

        best_idx = models_df['AUC-ROC'].idxmax()

        def highlight_best(row):
            style = 'background-color:#1a2e1a;color:#22c55e;font-weight:500'
            default = ''
            return [style if row.name == best_idx else default] * len(row)

        st.dataframe(
            models_df.style
                .apply(highlight_best, axis=1)
                .format({
                    'AUC-ROC':       '{:.4f}',
                    'Avg Precision': '{:.4f}',
                    'CV AUC (mean)': '{:.4f}',
                    'CV AUC (std)':  '{:.4f}',
                }),
            use_container_width=True,
            height=155
        )

    with col_m:
        best_name = models_df.loc[best_idx, 'Modele'] \
            if 'Modele' in models_df.columns else 'Random Forest'
        best_auc  = models_df.loc[best_idx, 'AUC-ROC']
        st.metric("Meilleur Modèle", best_name)
        st.metric("AUC-ROC", f"{best_auc:.4f}")
        st.metric("Taux d'avis négatifs", "12.7%")

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    col_s, col_i = st.columns(2)

    # ── SHAP ─────────────────────────────────────────────────
    with col_s:
        section("Importance des Variables — SHAP (Top 10)")
        shap_top = shap_df.head(10).sort_values('importance', ascending=True)
        bar_shap = [
            C['red']   if i >= 7 else
            C['amber'] if i >= 4 else
            C['slate']
            for i in range(len(shap_top))
        ]
        fig_sh = go.Figure(go.Bar(
            x=shap_top['importance'],
            y=shap_top['label'],
            orientation='h',
            marker_color=bar_shap,
            marker_opacity=0.85,
            text=[f"{v:.3f}" for v in shap_top['importance']],
            textposition='outside',
            textfont=dict(size=10, color='#94a3b8'),
            hovertemplate='%{y}<br>SHAP : %{x:.4f}<extra></extra>'
        ))
        apply_layout(fig_sh, height=400,
                     extra={
                         'showlegend': False,
                         'xaxis': dict(
                             title='Importance SHAP (valeur absolue moyenne)',
                             gridcolor='#1e2535',
                             title_font=dict(size=11)
                         ),
                         'margin': dict(l=8, r=60, t=16, b=8)
                     })
        st.plotly_chart(fig_sh, use_container_width=True)

    # ── Insights ─────────────────────────────────────────────
    with col_i:
        section("Interprétation Métier")
        insights = [
            ("Retard livraison", "delay_days", C['red'],
             "Facteur #1. Chaque jour de retard augmente "
             "significativement la probabilite d'un avis negatif."),
            ("Duree totale livraison", "delivery_days", C['red'],
             "Meme sans retard, une livraison longue "
             "degrade la satisfaction client."),
            ("Ratio frais de port", "freight_ratio", C['amber'],
             "Quand les frais depassent 30% du prix produit, "
             "le client est systematiquement decu."),
            ("Valeur client RFM", "monetary", C['amber'],
             "Les clients a forte valeur ont des attentes "
             "plus elevees et sont plus critiques."),
            ("Recence client", "recency", C['slate'],
             "Les clients inactifs depuis longtemps "
             "sont plus critiques a leur retour."),
        ]
        for label, feature, color, desc in insights:
            with st.expander(label):
                st.markdown(
                    f"<div style='font-size:12px;color:#64748b;line-height:1.7'>"
                    f"<span style='font-family:DM Mono,monospace;color:{color};"
                    f"font-size:11px'>{feature}</span><br>{desc}</div>",
                    unsafe_allow_html=True
                )

    # ── Recommandations ──────────────────────────────────────
    section("Recommandations Actionnables — Priorisées")
    r1, r2, r3 = st.columns(3)

    reco_data = [
        (r1, C['red'],   "Priorite 1",
         "Reduire les retards de livraison",
         [
             "Identifier les vendeurs avec retard > 20%",
             "Mettre en place des SLAs contractuels",
             "Alerte automatique a J+1 de retard",
             "Impact estime : +0.4 point de score",
         ]),
        (r2, C['amber'], "Priorite 2",
         "Réactiver les clients perdus",
         [
             "Campagne email win-back sur 3 028 clients",
             "Promo -15% sur categorie preferee",
             "Delai : sous 30 jours",
             "Impact estime : +2 a 3% retention",
         ]),
        (r3, C['blue'],  "Priorite 3",
         "Optimiser les frais de port",
         [
             "Plafonner freight_ratio a 25%",
             "Negocier tarifs logistiques",
             "Afficher delai estime avant validation",
             "Impact estime : +5% conversion",
         ]),
    ]

    for col, color, priority, title, items in reco_data:
        with col:
            items_html = "".join(
                f"<div style='display:flex;gap:6px;margin-bottom:5px'>"
                f"<span style='color:{color};margin-top:1px'>—</span>"
                f"<span>{item}</span></div>"
                for item in items
            )
            st.markdown(
                f"<div style='background:#161b27;border:1px solid #1e2535;"
                f"border-top:2px solid {color};border-radius:10px;padding:18px 16px'>"
                f"<div style='font-size:10px;color:{color};font-weight:500;"
                f"text-transform:uppercase;letter-spacing:0.8px;"
                f"margin-bottom:6px'>{priority}</div>"
                f"<div style='font-size:13px;font-weight:600;color:#f1f5f9;"
                f"margin-bottom:12px'>{title}</div>"
                f"<div style='font-size:12px;color:#64748b;line-height:1.6'>"
                f"{items_html}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

    # ── AUC bar ──────────────────────────────────────────────
    section("AUC-ROC — Comparaison des Modèles")
    model_names = models_df['Modele'].tolist() \
        if 'Modele' in models_df.columns \
        else ['Logistic Regression', 'Random Forest', 'XGBoost']
    auc_values = models_df['AUC-ROC'].tolist()
    auc_colors = [
        C['green'] if v == max(auc_values) else C['slate']
        for v in auc_values
    ]
    fig_auc = go.Figure(go.Bar(
        x=model_names, y=auc_values,
        marker_color=auc_colors,
        marker_opacity=0.85,
        text=[f"{v:.4f}" for v in auc_values],
        textposition='outside',
        textfont=dict(size=11, color='#94a3b8'),
        hovertemplate='%{x}<br>AUC-ROC : %{y:.4f}<extra></extra>'
    ))
    fig_auc.add_hline(
        y=0.5, line_dash='dash',
        line_color=C['red'], opacity=0.4,
        annotation_text="Aleatoire (0.5)",
        annotation_font=dict(size=10, color=C['red'])
    )
    apply_layout(fig_auc, height=300,
                 extra={
                     'showlegend': False,
                     'yaxis': dict(
                         title='AUC-ROC',
                         range=[0.4, 0.8],
                         gridcolor='#1e2535',
                         title_font=dict(size=11)
                     ),
                     'margin': dict(l=8, r=8, t=16, b=8)
                 })
    st.plotly_chart(fig_auc, use_container_width=True)