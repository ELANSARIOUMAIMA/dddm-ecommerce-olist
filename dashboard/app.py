"""
Dashboard décisionnel — Olist Brazilian E-Commerce
Phase 5 — Data-Driven Decision Making
5 vues : Direction | Marketing | Opérations | Produits | Modèle IA
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ── CONFIG PAGE ─────────────────────────────────────────────
st.set_page_config(
    page_title="Olist Dashboard — DDDM",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CHEMINS ─────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')

# ── CHARGEMENT DES DONNÉES (mise en cache) ───────────────────
@st.cache_data
def load_kpis():
    return pd.read_csv(os.path.join(DATA_DIR, 'dashboard_kpis.csv'))

@st.cache_data
def load_monthly():
    return pd.read_csv(os.path.join(DATA_DIR, 'dashboard_monthly.csv'))

@st.cache_data
def load_rfm_segments():
    return pd.read_csv(os.path.join(DATA_DIR, 'dashboard_rfm_segments.csv'))

@st.cache_data
def load_rfm_profile():
    return pd.read_csv(os.path.join(DATA_DIR, 'dashboard_rfm_profile.csv'))

@st.cache_data
def load_categories():
    return pd.read_csv(os.path.join(DATA_DIR, 'dashboard_categories.csv'))

@st.cache_data
def load_geo():
    return pd.read_csv(os.path.join(DATA_DIR, 'dashboard_geo.csv'))

@st.cache_data
def load_shap():
    return pd.read_csv(os.path.join(DATA_DIR, 'dashboard_shap_importance.csv'))

@st.cache_data
def load_models():
    return pd.read_csv(os.path.join(DATA_DIR, 'dashboard_model_comparison.csv'))

kpis       = load_kpis().iloc[0]
monthly    = load_monthly()
rfm_seg    = load_rfm_segments()
rfm_prof   = load_rfm_profile()
categories = load_categories()
geo        = load_geo()
shap_df    = load_shap()
models_df  = load_models()

# ── PALETTE COULEURS ─────────────────────────────────────────
COLORS = {
    'primary':   '#2563EB',
    'success':   '#16A34A',
    'warning':   '#D97706',
    'danger':    '#DC2626',
    'neutral':   '#6B7280',
    'Champions': '#16A34A',
    'Fidèles':   '#2563EB',
    'À risque':  '#D97706',
    'Inactifs':  '#DC2626',
}
SEG_ORDER = ['Champions', 'Fidèles', 'À risque', 'Inactifs']

# ── SIDEBAR ──────────────────────────────────────────────────
VUE_LABELS = [
    "Direction",
    "Marketing",
    "Operations",
    "Produits",
    "Modele IA",
]

with st.sidebar:
    st.markdown("## Olist Dashboard")
    st.markdown("**Data-Driven Decision Making**")
    st.markdown("---")
    vue_idx = st.radio(
        "Choisir une vue",
        options=list(range(len(VUE_LABELS))),
        format_func=lambda i: [
            "📊 Direction — KPIs Globaux",
            "👥 Marketing — Segments Clients",
            "🚚 Operations — Livraisons",
            "📦 Produits — Categories",
            "🤖 Modele IA — Predictions",
        ][i],
        index=0
    )
    st.markdown("---")
    st.markdown("**Dataset** : Olist 2016-2018")
    st.markdown(f"**Commandes** : {int(kpis['nb_commandes']):,}")
    st.markdown(f"**Clients** : {int(kpis['nb_clients_uniques']):,}")
    st.markdown("---")
    st.caption("Phase 5 — DDDM Project")

# ════════════════════════════════════════════════════════════
# VUE 1 — DIRECTION : KPIs GLOBAUX
# ════════════════════════════════════════════════════════════
if vue_idx == 0:

    st.title("📊 Vue Direction — KPIs Globaux")
    st.markdown("Tableau de bord exécutif — performance globale de la plateforme Olist (2016–2018)")
    st.markdown("---")

    # ── Ligne 1 : 4 métriques principales ───────────────────
    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        label="💰 Chiffre d'Affaires Total",
        value=f"R$ {kpis['ca_total']:,.0f}",
        help="Somme de tous les paiements sur commandes livrées"
    )
    c2.metric(
        label="🛍️ Panier Moyen (AOV)",
        value=f"R$ {kpis['aov']:.2f}",
        delta="Cible : R$ 150",
        delta_color="normal",
        help="Valeur moyenne par commande livrée"
    )
    c3.metric(
        label="⭐ Score Satisfaction Moyen",
        value=f"{kpis['review_score_moyen']:.2f} / 5",
        delta=f"{'✅ Cible atteinte' if kpis['review_score_moyen'] >= 4.0 else '⚠️ Cible : 4.0'}",
        delta_color="normal",
        help="Moyenne des notes laissées par les clients"
    )
    c4.metric(
        label="🔄 Taux de Rétention",
        value=f"{kpis['taux_retention']:.1f}%",
        delta="Cible : 15%",
        delta_color="normal",
        help="Part des clients ayant commandé plus d'une fois"
    )

    st.markdown("&nbsp;")

    # ── Ligne 2 : 4 métriques secondaires ───────────────────
    c5, c6, c7, c8 = st.columns(4)

    c5.metric(
        label="📦 Commandes Livrées",
        value=f"{int(kpis['nb_commandes']):,}",
    )
    c6.metric(
        label="👥 Clients Uniques",
        value=f"{int(kpis['nb_clients_uniques']):,}",
    )
    c7.metric(
        label="🚚 Livraisons dans les Délais",
        value=f"{kpis['taux_livraison_temps']:.1f}%",
        delta=f"{'✅ Cible atteinte' if kpis['taux_livraison_temps'] >= 90 else '⚠️ Cible : 90%'}",
        delta_color="normal",
    )
    c8.metric(
        label="❌ Taux d'Annulation",
        value=f"{kpis['taux_annulation']:.1f}%",
        delta=f"{'✅ OK' if kpis['taux_annulation'] <= 3 else '⚠️ Cible : < 3%'}",
        delta_color="inverse",
    )

    st.markdown("---")

    # ── Graphique : Évolution mensuelle CA + commandes ───────
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("📈 Évolution Mensuelle — CA & Volume Commandes")

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Bar(
                x=monthly['order_month'],
                y=monthly['ca'],
                name="CA (BRL)",
                marker_color=COLORS['primary'],
                opacity=0.75
            ),
            secondary_y=False
        )
        fig.add_trace(
            go.Scatter(
                x=monthly['order_month'],
                y=monthly['nb_commandes'],
                name="Nb Commandes",
                line=dict(color=COLORS['warning'], width=2.5),
                mode='lines+markers',
                marker=dict(size=5)
            ),
            secondary_y=True
        )

        fig.update_layout(
            height=380,
            hovermode='x unified',
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            margin=dict(l=10, r=10, t=30, b=60),
            xaxis=dict(tickangle=-45)
        )
        fig.update_yaxes(title_text="CA (BRL)", secondary_y=False)
        fig.update_yaxes(title_text="Nb Commandes", secondary_y=True)

        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("📋 KPI Tree")
        st.markdown("""
        ```
        CA Total
        ├── AOV (Panier Moyen)
        │   ├── Prix moyen produit
        │   └── Frais de port
        ├── Volume Commandes
        │   ├── Nouveaux clients
        │   └── Clients récurrents
        └── Satisfaction (NPS)
            ├── Délai de livraison
            └── Taux de retard
        ```
        """)
        st.markdown("---")
        st.markdown("**Business Case :**")
        st.info(
            "96% des clients n'achètent qu'une seule fois. "
            "Améliorer la rétention de +5% génère "
            "**+8 à 12% de CA** sur 12 mois."
        )

    # ── Graphique : Score moyen et taux retard par mois ─────
    st.subheader("📉 Satisfaction & Retards — Évolution Mensuelle")

    fig2 = make_subplots(specs=[[{"secondary_y": True}]])

    fig2.add_trace(
        go.Scatter(
            x=monthly['order_month'],
            y=monthly['review_moyen'],
            name="Score Avis Moyen",
            line=dict(color=COLORS['success'], width=2.5),
            mode='lines+markers',
            marker=dict(size=5)
        ),
        secondary_y=False
    )
    fig2.add_trace(
        go.Scatter(
            x=monthly['order_month'],
            y=monthly['taux_retard'],
            name="Taux de Retard (%)",
            line=dict(color=COLORS['danger'], width=2.5, dash='dot'),
            mode='lines+markers',
            marker=dict(size=5)
        ),
        secondary_y=True
    )

    fig2.add_hline(
        y=4.0, line_dash="dash", line_color=COLORS['success'],
        annotation_text="Cible score ≥ 4.0",
        annotation_position="top left",
        secondary_y=False
    )

    fig2.update_layout(
        height=320,
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
        margin=dict(l=10, r=10, t=30, b=60),
        xaxis=dict(tickangle=-45)
    )
    fig2.update_yaxes(title_text="Score Moyen (1–5)", secondary_y=False, range=[3, 5])
    fig2.update_yaxes(title_text="Taux de Retard (%)", secondary_y=True)

    st.plotly_chart(fig2, use_container_width=True)


# ════════════════════════════════════════════════════════════
# VUE 2 — MARKETING : SEGMENTS CLIENTS RFM
# ════════════════════════════════════════════════════════════
elif vue_idx == 1:

    st.title("👥 Vue Marketing — Segmentation Clients RFM")
    st.markdown("Segmentation en 4 catégories basée sur la Récence, Fréquence et Valeur monétaire")
    st.markdown("---")

    # ── Cartes profil par segment ────────────────────────────
    st.subheader("Profil des 4 Segments")
    cols = st.columns(4)

    icons = {'Champions': '🏆', 'Fidèles': '💙', 'À risque': '⚠️', 'Inactifs': '😴'}
    actions = {
        'Champions':  'Récompenser · Programme VIP · Upsell',
        'Fidèles':    'Fidéliser · Cross-sell · NPS',
        'À risque':   'Réactiver · Promo ciblée · Email win-back',
        'Inactifs':   'Campagne réactivation · Dernière chance',
    }

    for col, (_, row) in zip(cols, rfm_prof.iterrows()):
        seg = row['segment']
        with col:
            st.markdown(f"""
            <div style="
                border: 1.5px solid {COLORS[seg]};
                border-radius: 10px;
                padding: 14px;
                text-align: center;
                margin-bottom: 8px;
            ">
                <div style="font-size: 28px">{icons[seg]}</div>
                <div style="font-weight: 600; font-size: 16px; color: {COLORS[seg]}">{seg}</div>
                <div style="font-size: 13px; color: grey; margin: 6px 0">
                    {int(row['nb_clients']):,} clients ({row['pct_clients']:.1f}%)<br>
                    Revenue : {row['pct_revenue']:.1f}% du total<br>
                    Panier moy. : R$ {row['monetary_moy']:.0f}<br>
                    Récence moy. : {row['recency_moy']:.0f}j
                </div>
                <div style="font-size: 11px; color: {COLORS[seg]}; font-style: italic">
                    {actions[seg]}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    col_a, col_b = st.columns(2)

    # ── Donut : répartition clients ──────────────────────────
    with col_a:
        st.subheader("Répartition des Clients par Segment")

        fig_donut = go.Figure(go.Pie(
            labels=rfm_prof['segment'],
            values=rfm_prof['nb_clients'],
            hole=0.55,
            marker_colors=[COLORS[s] for s in rfm_prof['segment']],
            textinfo='label+percent',
            hovertemplate='%{label}<br>%{value:,} clients<br>%{percent}<extra></extra>',
            sort=False
        ))
        fig_donut.update_layout(
            height=380,
            showlegend=False,
            margin=dict(l=10, r=10, t=30, b=10),
            annotations=[dict(
                text=f"{int(rfm_prof['nb_clients'].sum()):,}<br>clients",
                x=0.5, y=0.5, font_size=16, showarrow=False
            )]
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # ── Bar : revenue par segment ────────────────────────────
    with col_b:
        st.subheader("Revenue Total par Segment")

        fig_bar = go.Figure(go.Bar(
            x=rfm_prof['segment'],
            y=rfm_prof['monetary_total'],
            marker_color=[COLORS[s] for s in rfm_prof['segment']],
            text=[f"R$ {v:,.0f}" for v in rfm_prof['monetary_total']],
            textposition='outside',
            hovertemplate='%{x}<br>R$ %{y:,.0f}<extra></extra>'
        ))
        fig_bar.update_layout(
            height=380,
            yaxis_title="Revenue Total (BRL)",
            margin=dict(l=10, r=10, t=30, b=10),
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── Scatter RFM ──────────────────────────────────────────
    st.subheader("Scatter RFM — Récence vs Valeur (échantillon 3 000 clients)")

    rfm_sample = rfm_seg.sample(min(3000, len(rfm_seg)), random_state=42)

    fig_scatter = px.scatter(
        rfm_sample,
        x='recency',
        y='monetary',
        color='segment',
        color_discrete_map=COLORS,
        opacity=0.55,
        size_max=8,
        labels={
            'recency':  'Récence (jours depuis dernier achat)',
            'monetary': 'Valeur totale dépensée (BRL)',
            'segment':  'Segment'
        },
        category_orders={'segment': SEG_ORDER},
        hover_data=['frequency']
    )
    fig_scatter.update_traces(marker=dict(size=5))
    fig_scatter.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=30, b=10)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)


# ════════════════════════════════════════════════════════════
# VUE 3 — OPÉRATIONS : LIVRAISONS
# ════════════════════════════════════════════════════════════
elif vue_idx == 2:

    st.title("🚚 Vue Opérations — Performance des Livraisons")
    st.markdown("Analyse des délais, retards et satisfaction par région géographique")
    st.markdown("---")

    # ── KPIs opérationnels ───────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🚚 Livraisons à temps",
              f"{kpis['taux_livraison_temps']:.1f}%",
              delta="Cible ≥ 90%",
              delta_color="normal")
    c2.metric("⏱️ Délai médian livraison",
              f"{kpis['delai_moyen_jours']:.0f} jours")
    c3.metric("⭐ Score moyen (avis)",
              f"{kpis['review_score_moyen']:.2f} / 5")
    c4.metric("📦 Commandes analysées",
              f"{int(kpis['nb_commandes']):,}")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    # ── Carte bulle : retard par état ────────────────────────
    with col_left:
        st.subheader("🗺️ Taux de Retard par État (Brésil)")

        geo_clean = geo.dropna(subset=['lat', 'lon'])

        fig_map = px.scatter_geo(
            geo_clean,
            lat='lat',
            lon='lon',
            size='nb_commandes',
            color='taux_retard',
            hover_name='customer_state',
            hover_data={
                'nb_commandes': True,
                'taux_retard': ':.1f',
                'delai_moyen': ':.1f',
                'review_moyen': ':.2f',
                'lat': False,
                'lon': False
            },
            color_continuous_scale='RdYlGn_r',
            size_max=40,
            scope='south america',
            labels={
                'taux_retard':   'Taux retard (%)',
                'nb_commandes':  'Nb commandes',
                'delai_moyen':   'Délai moyen (j)',
                'review_moyen':  'Score moyen'
            },
            title=""
        )
        fig_map.update_layout(
            height=420,
            margin=dict(l=0, r=0, t=10, b=0),
            coloraxis_colorbar=dict(title="Retard (%)")
        )
        st.plotly_chart(fig_map, use_container_width=True)

    # ── Bar horizontal : top états par retard ───────────────
    with col_right:
        st.subheader("📊 Top 10 États — Taux de Retard")

        top_retard = geo.sort_values('taux_retard', ascending=True).tail(10)
        colors_bar = [
            COLORS['danger'] if v > 20 else
            COLORS['warning'] if v > 10 else
            COLORS['success']
            for v in top_retard['taux_retard']
        ]

        fig_states = go.Figure(go.Bar(
            x=top_retard['taux_retard'],
            y=top_retard['customer_state'],
            orientation='h',
            marker_color=colors_bar,
            text=[f"{v:.1f}%" for v in top_retard['taux_retard']],
            textposition='outside',
            hovertemplate='%{y}<br>Retard : %{x:.1f}%<extra></extra>'
        ))
        fig_states.update_layout(
            height=420,
            xaxis_title="Taux de retard (%)",
            margin=dict(l=10, r=60, t=10, b=10),
            showlegend=False
        )
        st.plotly_chart(fig_states, use_container_width=True)

    # ── Scatter : délai vs score par état ───────────────────
    st.subheader("📉 Délai Moyen vs Score Satisfaction — par État")

    fig_del = px.scatter(
        geo,
        x='delai_moyen',
        y='review_moyen',
        size='nb_commandes',
        color='taux_retard',
        hover_name='customer_state',
        color_continuous_scale='RdYlGn_r',
        size_max=35,
        labels={
            'delai_moyen':  'Délai moyen (jours)',
            'review_moyen': 'Score avis moyen',
            'taux_retard':  'Taux retard (%)',
            'nb_commandes': 'Nb commandes'
        },
        text='customer_state'
    )
    fig_del.update_traces(textposition='top center', textfont_size=10)
    fig_del.add_hline(y=4.0, line_dash='dash', line_color=COLORS['success'],
                      annotation_text="Cible score = 4.0")
    fig_del.update_layout(
        height=450,
        margin=dict(l=10, r=10, t=30, b=10)
    )
    st.plotly_chart(fig_del, use_container_width=True)


# ════════════════════════════════════════════════════════════
# VUE 4 — PRODUITS : CATÉGORIES
# ════════════════════════════════════════════════════════════
elif vue_idx == 3:

    st.title("📦 Vue Produits — Analyse par Catégories")
    st.markdown("Performance commerciale et satisfaction client par catégorie de produit (Top 20)")
    st.markdown("---")

    # ── Filtre interactif ────────────────────────────────────
    nb_cat = st.slider("Nombre de catégories à afficher", 5, 20, 15)
    cat_display = categories.head(nb_cat).copy()

    col_a, col_b = st.columns(2)

    # ── Bar : revenue par catégorie ──────────────────────────
    with col_a:
        st.subheader("💰 Revenue par Catégorie")

        cat_sorted = cat_display.sort_values('revenue', ascending=True)
        fig_rev = go.Figure(go.Bar(
            x=cat_sorted['revenue'],
            y=cat_sorted['product_category_name_english'],
            orientation='h',
            marker_color=COLORS['primary'],
            text=[f"R$ {v:,.0f}" for v in cat_sorted['revenue']],
            textposition='outside',
            hovertemplate='%{y}<br>Revenue : R$ %{x:,.0f}<extra></extra>'
        ))
        fig_rev.update_layout(
            height=500,
            xaxis_title="Revenue (BRL)",
            margin=dict(l=10, r=80, t=10, b=10),
            showlegend=False
        )
        st.plotly_chart(fig_rev, use_container_width=True)

    # ── Bar : score moyen par catégorie ─────────────────────
    with col_b:
        st.subheader("⭐ Score Satisfaction Moyen")

        cat_score = cat_display.sort_values('review_moyen', ascending=True)
        bar_colors = [
            COLORS['success'] if v >= 4.0 else
            COLORS['warning'] if v >= 3.5 else
            COLORS['danger']
            for v in cat_score['review_moyen']
        ]

        fig_score = go.Figure(go.Bar(
            x=cat_score['review_moyen'],
            y=cat_score['product_category_name_english'],
            orientation='h',
            marker_color=bar_colors,
            text=[f"{v:.2f}" for v in cat_score['review_moyen']],
            textposition='outside',
            hovertemplate='%{y}<br>Score : %{x:.2f}<extra></extra>'
        ))
        fig_score.add_vline(
            x=4.0, line_dash='dash', line_color=COLORS['success'],
            annotation_text="Cible = 4.0", annotation_position="top"
        )
        fig_score.update_layout(
            height=500,
            xaxis_title="Score Moyen (1–5)",
            xaxis_range=[0, 5.5],
            margin=dict(l=10, r=60, t=10, b=10),
            showlegend=False
        )
        st.plotly_chart(fig_score, use_container_width=True)

    # ── Bubble : revenue vs retard vs score ─────────────────
    st.subheader("🔵 Matrice Revenue × Retard × Satisfaction — par Catégorie")
    st.caption("Taille des bulles = nombre de commandes | Couleur = score moyen")

    fig_bubble = px.scatter(
        cat_display,
        x='taux_retard',
        y='review_moyen',
        size='nb_commandes',
        color='review_moyen',
        color_continuous_scale='RdYlGn',
        size_max=45,
        text='product_category_name_english',
        labels={
            'taux_retard':  'Taux de Retard (%)',
            'review_moyen': 'Score Satisfaction Moyen',
            'nb_commandes': 'Nb Commandes',
            'review_moyen': 'Score'
        },
        hover_data={
            'revenue': ':,.0f',
            'nb_commandes': True,
            'taux_retard': ':.1f',
        }
    )
    fig_bubble.update_traces(textposition='top center', textfont_size=9)
    fig_bubble.add_hline(y=4.0, line_dash='dash', line_color=COLORS['success'],
                         annotation_text="Cible satisfaction")
    fig_bubble.update_layout(
        height=500,
        coloraxis_colorbar=dict(title="Score"),
        margin=dict(l=10, r=10, t=30, b=10)
    )
    st.plotly_chart(fig_bubble, use_container_width=True)


# ════════════════════════════════════════════════════════════
# VUE 5 — MODÈLE IA : PRÉDICTIONS & INTERPRÉTABILITÉ
# ════════════════════════════════════════════════════════════
elif vue_idx == 4:

    st.title("🤖 Vue Modèle IA — Prédictions & Interprétabilité")
    st.markdown("Modèle de classification : **prédire si une commande recevra un avis négatif (score ≤ 2)**")
    st.markdown("---")

    # ── Tableau comparatif modèles ───────────────────────────
    st.subheader("📊 Comparaison des 3 Modèles Entraînés")

    col_m1, col_m2 = st.columns([2, 1])

    with col_m1:
        models_display = models_df.copy()
        # Renommer si colonne s'appelle 'Modèle' ou 'model'
        if 'Modèle' not in models_display.columns and 'model' in models_display.columns:
            models_display = models_display.rename(columns={'model': 'Modèle'})

        best_idx = models_display['AUC-ROC'].idxmax()

        def highlight_best(row):
            return [
                'background-color: #d1fae5; font-weight: bold'
                if row.name == best_idx else ''
            ] * len(row)

        st.dataframe(
            models_display.style
                .apply(highlight_best, axis=1)
                .format({
                    'AUC-ROC':       '{:.4f}',
                    'Avg Precision': '{:.4f}',
                    'CV AUC (mean)': '{:.4f}',
                    'CV AUC (std)':  '{:.4f}',
                }),
            use_container_width=True,
            height=160
        )

    with col_m2:
        best_model_name = models_display.loc[best_idx, 'Modèle'] \
            if 'Modèle' in models_display.columns else 'Random Forest'
        best_auc = models_display.loc[best_idx, 'AUC-ROC']

        st.success(f"**Meilleur modèle** : {best_model_name}")
        st.metric("AUC-ROC", f"{best_auc:.4f}")
        st.metric("Taux d'avis négatifs", "12.7%",
                  help="Part des commandes avec score ≤ 2 dans le dataset")
        st.caption("Validation : StratifiedKFold (3 folds)")

    st.markdown("---")

    # ── SHAP Feature Importance ──────────────────────────────
    col_s1, col_s2 = st.columns(2)

    with col_s1:
        st.subheader("🔍 Importance des Features — SHAP (Top 10)")

        shap_top = shap_df.head(10).sort_values('importance', ascending=True)
        bar_shap_colors = [
            COLORS['danger']  if i >= 7 else
            COLORS['warning'] if i >= 4 else
            COLORS['neutral']
            for i in range(len(shap_top))
        ]

        fig_shap = go.Figure(go.Bar(
            x=shap_top['importance'],
            y=shap_top['label'],
            orientation='h',
            marker_color=bar_shap_colors,
            text=[f"{v:.3f}" for v in shap_top['importance']],
            textposition='outside',
            hovertemplate='%{y}<br>Importance SHAP : %{x:.4f}<extra></extra>'
        ))
        fig_shap.update_layout(
            height=420,
            xaxis_title="Importance SHAP moyenne absolue",
            margin=dict(l=10, r=60, t=10, b=10),
            showlegend=False
        )
        st.plotly_chart(fig_shap, use_container_width=True)

    with col_s2:
        st.subheader("💡 Interprétation Métier")

        st.markdown("#### Principaux drivers des avis négatifs")

        insights = [
            ("🔴", "Retard livraison", "delay_days",
             "Le facteur #1. Chaque jour de retard augmente significativement la probabilité d'un avis négatif."),
            ("🔴", "Durée totale livraison", "delivery_days",
             "Même sans retard, une livraison longue dégrade la satisfaction."),
            ("🟠", "Ratio frais de port", "freight_ratio",
             "Quand les frais de port dépassent ~30% du prix produit, le client est déçu."),
            ("🟡", "Valeur client RFM", "monetary",
             "Les clients à forte valeur ont des attentes plus élevées."),
            ("🟡", "Récence client", "recency",
             "Les clients inactifs depuis longtemps sont plus critiques au retour."),
        ]

        for icon, label, feature, desc in insights:
            with st.expander(f"{icon} {label}"):
                st.markdown(f"**Feature** : `{feature}`")
                st.markdown(desc)

    # ── Recommandations actionnables ─────────────────────────
    st.markdown("---")
    st.subheader("🎯 3 Recommandations Actionnables — Priorisées")

    r1, r2, r3 = st.columns(3)

    with r1:
        st.error("#### 🥇 Priorité 1")
        st.markdown("**Réduire les retards de livraison**")
        st.markdown("""
        - Identifier les vendeurs avec taux de retard > 20%
        - Mettre en place des SLAs contractuels
        - Alerte automatique à J+1 de retard
        - **Impact estimé** : +0.4 point de score moyen
        """)

    with r2:
        st.warning("#### 🥈 Priorité 2")
        st.markdown("**Réactiver les clients À Risque**")
        st.markdown("""
        - Campagne email win-back sur les 3 028 clients fidèles inactifs
        - Promo ciblée -15% sur leur catégorie préférée
        - Délai : dans les 30 prochains jours
        - **Impact estimé** : +2 à 3% de taux de rétention
        """)

    with r3:
        st.info("#### 🥉 Priorité 3")
        st.markdown("**Optimiser les frais de port**")
        st.markdown("""
        - Plafonner le freight_ratio à 25% du prix produit
        - Négocier des tarifs logistiques pour les catégories à fort retard
        - Afficher le délai estimé avant validation commande
        - **Impact estimé** : +5% de conversion
        """)

    # ── AUC-ROC bar chart ────────────────────────────────────
    st.markdown("---")
    st.subheader("📈 AUC-ROC — Comparaison Visuelle")

    model_names = models_display['Modèle'].tolist() \
        if 'Modèle' in models_display.columns \
        else ['Logistic Regression', 'Random Forest', 'XGBoost']

    auc_values = models_display['AUC-ROC'].tolist()
    auc_colors = [
        COLORS['success'] if v == max(auc_values) else COLORS['neutral']
        for v in auc_values
    ]

    fig_auc = go.Figure(go.Bar(
        x=model_names,
        y=auc_values,
        marker_color=auc_colors,
        text=[f"{v:.4f}" for v in auc_values],
        textposition='outside',
        hovertemplate='%{x}<br>AUC-ROC : %{y:.4f}<extra></extra>'
    ))
    fig_auc.add_hline(
        y=0.5, line_dash='dash', line_color=COLORS['danger'],
        annotation_text="Aléatoire (0.5)", annotation_position="top left"
    )
    fig_auc.update_layout(
        height=320,
        yaxis=dict(title="AUC-ROC", range=[0.4, 0.8]),
        margin=dict(l=10, r=10, t=30, b=10),
        showlegend=False
    )
    st.plotly_chart(fig_auc, use_container_width=True)