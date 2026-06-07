# Olist Analytics : Data-Driven Decision Making

> Projet académique : Module Data-Driven Decision Making  
> Dataset : [Brazilian E-Commerce (Olist)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) · 99 441 commandes · 2016–2018

---

## Présentation du Projet

Ce projet applique l'intégralité du pipeline décisionnel basé sur la donnée, depuis la définition des KPIs jusqu'au déploiement d'un dashboard décisionnel en ligne. Il prend appui sur les données réelles de la plateforme Olist, la plus grande marketplace brésilienne, pour répondre à la question centrale :

> **Comment identifier les segments clients les plus rentables et optimiser les décisions marketing et logistiques pour maximiser le chiffre d'affaires de la plateforme ?**

---

## Dashboard en ligne

**URL** : [https://dddm-ecommerce-olist-bdfn7pnhvqeexiu6r9ufke.streamlit.app/](https://dddm-ecommerce-olist-bdfn7pnhvqeexiu6r9ufke.streamlit.app/)

Le dashboard est accessible sans installation. Il comprend 5 vues interactives :

| Vue | Profil cible | Contenu |
|-----|-------------|---------|
| Direction — KPIs Globaux | Direction générale | CA total, AOV, satisfaction, rétention, tendances mensuelles |
| Marketing — Segments Clients | Équipe marketing | Segmentation RFM 4 catégories, scatter récence/valeur |
| Opérations — Livraisons | Équipe logistique | Carte retards par état, délai vs satisfaction |
| Produits — Catégories | Chef de produit | Revenue, score, taux retard par catégorie |
| Modèle IA — Prédictions | Data & Direction | SHAP, comparaison modèles, recommandations |

---

## Structure du Projet

```
dddm-ecommerce-olist/
│
├── data/
│   ├── raw/                          # CSV bruts Kaggle (non versionnés)
│   │   ├── olist_orders_dataset.csv
│   │   ├── olist_customers_dataset.csv
│   │   ├── olist_order_items_dataset.csv
│   │   ├── olist_order_payments_dataset.csv
│   │   ├── olist_order_reviews_dataset.csv
│   │   ├── olist_products_dataset.csv
│   │   ├── olist_sellers_dataset.csv
│   │   ├── olist_geolocation_dataset.csv
│   │   └── product_category_name_translation.csv
│   │
│   └── processed/                    # Données transformées (versionnées)
│       ├── rfm_clusters.csv          # Table RFM + clusters K-Means
│       ├── dashboard_kpis.csv        # KPIs globaux agrégés
│       ├── dashboard_monthly.csv     # Tendances mensuelles
│       ├── dashboard_rfm_segments.csv
│       ├── dashboard_rfm_profile.csv
│       ├── dashboard_categories.csv
│       ├── dashboard_geo.csv
│       ├── dashboard_shap_importance.csv
│       └── dashboard_model_comparison.csv
│
├── notebooks/
│   ├── phase1_problem_definition.ipynb   # KPIs + Business Case
│   ├── phase2_data_audit.ipynb           # Audit + Data Dictionary
│   ├── phase3_eda.ipynb                  # EDA + Segmentation RFM
│   ├── phase4_modeling.ipynb             # Modélisation + SHAP
│   └── phase5_data_prep.ipynb           # Agrégats dashboard
│
├── dashboard/
│   ├── app.py                        # Application Streamlit (5 vues)
│   └── requirements.txt              # Dépendances dashboard
│
├── reports/
│   ├── figures/                      # Graphiques générés (PNG)
│   │   ├── phase3_*.png
│   │   └── phase4_*.png
│   └── phase4_model_comparison.csv   # Tableau comparatif modèles
│
├── models/
│   └── best_model_random_forest.pkl  # Modèle entraîné sauvegardé
│
├── requirements.txt                  # Dépendances globales
└── README.md
```

---

## Installation locale

### Prérequis

- Python 3.10+
- Compte Kaggle (pour télécharger les données)
- Git

### 1. Cloner le repository

```bash
git clone https://github.com/ELANSARIOUMAIMA/dddm-ecommerce-olist.git
cd dddm-ecommerce-olist
```

### 2. Créer l'environnement virtuel

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Télécharger les données Kaggle

**Option A : Via l'API Kaggle**

```bash
pip install kaggle
# Placer kaggle.json dans ~/.kaggle/ (voir https://www.kaggle.com/docs/api)
kaggle datasets download -d olistbr/brazilian-ecommerce -p data/raw/ --unzip
```

**Option B : Téléchargement manuel**

Télécharger depuis [kaggle.com/datasets/olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) et placer les 9 fichiers CSV dans `data/raw/`.

### 5. Lancer les notebooks

```bash
jupyter notebook
```

Exécuter dans cet ordre :

| Ordre | Notebook | Durée | Rôle |
|-------|----------|-------|------|
| 1 | `phase1_problem_definition.ipynb` | ~1 min | KPIs, Business Case |
| 2 | `phase2_data_audit.ipynb` | ~2 min | Audit, Data Dictionary |
| 3 | `phase3_eda.ipynb` | ~5 min | EDA, clustering RFM |
| 4 | `phase4_modeling.ipynb` | ~10 min | Modélisation, SHAP |
| 5 | `phase5_data_prep.ipynb` | ~3 min | Agrégats dashboard |

### 6. Lancer le dashboard

```bash
streamlit run dashboard/app.py
```

Ouvre automatiquement sur [http://localhost:8501](http://localhost:8501).

---

## Phases du Projet

### Phase 1 : Définition du Problème & KPIs

Cadrage métier et définition des métriques de succès avant tout contact avec les données.

**KPIs primaires**

| KPI | Formule | Cible |
|-----|---------|-------|
| CA Total | Σ payment_value | Suivi mensuel |
| AOV (Panier Moyen) | CA / Nb commandes | > R$ 150 |
| Taux de Rétention | Clients récurrents / Total | > 15% |
| Score Satisfaction | Moyenne review_score | > 4.0 / 5 |

**KPIs secondaires** : taux de livraison dans les délais (cible > 90%), taux d'annulation (cible < 3%).

**Business Case** : 96% des clients n'achètent qu'une seule fois. Améliorer la rétention de +5% génère +8 à 12% de CA sur 12 mois.

---

### Phase 2 : Collecte & Audit des Données

Audit complet des 9 fichiers CSV Olist (99 441+ lignes).

| Dimension | Score | Détail |
|-----------|-------|--------|
| Complétude | 9/10 | < 3% de valeurs manquantes sur colonnes critiques |
| Cohérence | 8/10 | Quelques incohérences de dates corrigées |
| Fraîcheur | 7/10 | Données 2016–2018, suffisant pour le projet |
| Granularité | 9/10 | Timestamps précis, codes postaux, IDs uniques |
| Volume | 10/10 | ~100 000 commandes >> seuil minimum 50 000 |
| **Global** | **8.8/10** | Dataset propre et prêt pour l'analyse |

**Imputations réalisées** : `order_approved_at` manquant → délai médian (1.4h) ; catégorie produit manquante → mode ; géolocalisation doublons → médiane lat/lng.

---

### Phase 3 : Exploration & Analyse Statistique (EDA)

Analyse exploratoire complète avec tests statistiques et segmentation client.

**Tests statistiques**

| Test | Variables | Résultat |
|------|-----------|----------|
| Mann-Whitney U | Score avis : à temps vs en retard | p ≈ 0 — différence significative |
| ANOVA | Délai livraison par score (1→5) | F = 2961, p ≈ 0 |
| Chi-² | Retard vs État du client | χ² = 1218, p ≈ 0 |

**Segmentation RFM**

Construction de la table RFM (96 096 clients uniques) et clustering K-Means. K=2 retenu (silhouette = 0.74). Détection d'anomalies par DBSCAN : 4.7% de clients atypiques identifiés.

**Résultat clé** : corrélation entre `is_late` et `review_score` = -0.32. Les livraisons en retard ont une médiane de score à 1.0 vs 5.0 pour les livraisons à temps.

---

### Phase 4 : Modélisation Prédictive & Interprétabilité

**Problème** : classification binaire — prédire si une commande recevra un avis négatif (score ≤ 2).

**18 features** : livraison, temporel, géographie, produit, paiement, RFM client.

**Résultats**

| Modèle | AUC-ROC | Avg Precision | CV AUC |
|--------|---------|---------------|--------|
| Logistic Regression | 0.7071 | 0.3972 | 0.7126 ± 0.005 |
| Random Forest | **0.7298** | 0.4296 | 0.7186 ± 0.006 |
| XGBoost | 0.7252 | **0.4333** | 0.7142 ± 0.004 |

**Meilleur modèle** : Random Forest (AUC-ROC = 0.7298)

**Top features SHAP**

1. `delay_days` : retard de livraison en jours (facteur #1)
2. `delivery_days` : durée totale de livraison
3. `freight_ratio` : ratio frais de port / prix produit
4. `monetary` : valeur client RFM

---

### Phase 5 : Dashboard Décisionnel Interactif

Dashboard Streamlit déployé en ligne avec 5 vues distinctes par profil utilisateur.

**Stack technique** : Python · Streamlit · Plotly · Pandas

**Données** : agrégats précalculés versionnés dans `data/processed/` (pas de chargement des CSV bruts au runtime).

---

### Phase 6 : A/B Testing & Mesure d'Impact

Voir le document `reports/ab_test_plan.pdf` pour le protocole expérimental complet.

**3 recommandations actionnables**

1. **Réduire les retards de livraison** : SLAs vendeurs, alertes J+1 → impact estimé +0.4 point de score moyen
2. **Réactiver les clients perdus** : campagne win-back sur 3 028 clients à risque → +2 à 3% de rétention
3. **Optimiser les frais de port** : plafonner freight_ratio à 25% → +5% de conversion

---

## Dépendances

```
pandas>=1.5
numpy>=1.23
matplotlib>=3.6
seaborn>=0.12
scipy>=1.10
scikit-learn>=1.2
xgboost>=1.7
shap>=0.42
joblib>=1.2
streamlit>=1.32
plotly>=5.18
jupyter>=1.0
ipykernel
```