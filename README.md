# 🛒 DDDM E-Commerce Olist — Phases 3 & 4

> **Module** : Data-Driven Decision Making  
> **Dataset** : [Brazilian E-Commerce (Olist)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)  
> **Branche** : `phase3-phase4-EDA-modeling`

---

## 📁 Structure du Projet

```
dddm-ecommerce-olist/
├── data/
│   ├── raw/                          # CSV bruts Kaggle (non versionnés)
│   │   ├── olist_orders_dataset.csv
│   │   ├── olist_order_items_dataset.csv
│   │   ├── olist_order_payments_dataset.csv
│   │   ├── olist_order_reviews_dataset.csv
│   │   ├── olist_customers_dataset.csv
│   │   ├── olist_products_dataset.csv
│   │   ├── olist_sellers_dataset.csv
│   │   └── product_category_name_translation.csv
│   └── processed/                    # Données transformées
│       └── rfm_clusters.csv          # Table RFM + labels clusters
├── notebooks/
│   ├── phase3_eda.ipynb              # Exploration & Analyse Statistique
│   └── phase4_modeling.ipynb         # Modélisation & Interprétabilité
├── reports/
│   └── figures/                      # Graphiques générés automatiquement
│       ├── phase3_distributions.png
│       ├── phase3_boxplots.png
│       ├── phase3_correlation_heatmap.png
│       ├── phase3_violin_delivery_score.png
│       ├── phase3_monthly_trend.png
│       ├── phase3_heatmap_dow_hour.png
│       ├── phase3_category_analysis.png
│       ├── phase3_elbow_silhouette.png
│       ├── phase3_clusters_rfm.png
│       ├── phase3_scatter_matrix.png
│       ├── phase4_roc_curves.png
│       ├── phase4_precision_recall.png
│       ├── phase4_confusion_matrix.png
│       ├── phase4_feature_importance.png
│       ├── phase4_shap_summary.png
│       ├── phase4_shap_bar.png
│       ├── phase4_shap_force_local.png
│       └── phase4_shap_dependence.png
├── models/
│   └── best_model_*.pkl              
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Cloner le repo et se positionner sur la bonne branche

```bash
git clone https://github.com/TON_USERNAME/dddm-ecommerce-olist.git
cd dddm-ecommerce-olist
git checkout phase3-phase4-EDA-modeling
```

### 2. Créer un environnement virtuel

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

Télécharger manuellement depuis :  
👉 https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Placer tous les fichiers CSV dans `data/raw/`.

---

## 🚀 Lancer les Notebooks

```bash
jupyter notebook
```

Exécuter dans cet ordre :

| Ordre | Notebook | Durée estimée |
|-------|----------|---------------|
| 1 | `notebooks/phase3_eda.ipynb` | ~5 min |
| 2 | `notebooks/phase4_modeling.ipynb` | ~10 min |


---

## 📊 Phase 3 — Exploration & Analyse Statistique (EDA)

### Objectifs
Comprendre les données, détecter les anomalies et segmenter les clients.

### Ce que fait le notebook

**Analyse des distributions**
- Prix, frais de port, délais de livraison, scores d'avis
- Détection et traitement des outliers par méthode IQR (cap au 99e percentile)

**Analyse de corrélation**
- Heatmap de corrélation entre toutes les variables numériques
- Identification des drivers du score d'avis client

**Tests statistiques**

| Test | Variables | Résultat attendu |
|------|-----------|-----------------|
| Mann-Whitney U | Score avis : à temps vs en retard | p < 0.05 ✅ |
| ANOVA | Délai livraison par score (1→5) | p < 0.05 ✅ |
| Chi-² | Retard vs État du client | p < 0.05 ✅ |

**Analyse temporelle**
- Évolution mensuelle du CA et du volume de commandes
- Heatmap commandes par jour de la semaine et heure

**Segmentation RFM + Clustering**
- Construction de la table RFM (Recency, Frequency, Monetary)
- K-Means avec méthode Elbow + Silhouette Score (sample de 2 000 pts)
- DBSCAN pour détection d'anomalies
- Export : `data/processed/rfm_clusters.csv`

### Outputs générés
- 10 figures PNG dans `reports/figures/phase3_*.png`
- `data/processed/rfm_clusters.csv`

---

## 🤖 Phase 4 — Modélisation Prédictive & Interprétabilité

### Objectif
Prédire si une commande recevra un **avis négatif (score ≤ 2)**.

### Problème
> Classification binaire supervisée  
> `target = 1` si `review_score ≤ 2`, sinon `target = 0`  
> Taux de positifs : ~11% (classe déséquilibrée)

### Features utilisées (18 variables)

| Catégorie | Features |
|-----------|----------|
| Commande | `price`, `freight_value`, `freight_ratio`, `revenue` |
| Livraison | `delivery_days`, `delay_days`, `is_late` |
| Temporel | `order_hour`, `order_dow`, `order_month_nb` |
| Géographie | `customer_state_enc` |
| Produit | `category_enc` |
| Paiement | `payment_type_enc`, `payment_installments` |
| RFM Client | `recency`, `frequency`, `monetary`, `cluster` |

### Modèles entraînés

| Modèle | Paramètres clés |
|--------|----------------|
| Logistic Regression | `class_weight='balanced'`, `max_iter=500` |
| Random Forest | `n_estimators=100`, `max_depth=8`, `class_weight='balanced'` |
| XGBoost | `n_estimators=100`, `max_depth=5`, `tree_method='hist'` |

### Évaluation
- Validation croisée `StratifiedKFold` (3 folds)
- Métriques : AUC-ROC, Average Precision, F1-Score, Precision, Recall
- Courbes ROC et Precision-Recall comparatives

### Interprétabilité SHAP
- **Global** : Summary plot + Bar plot (importance moyenne absolue)
- **Local** : Force plot sur une observation individuelle
- **Dependence plot** : Impact de `delay_days` selon `is_late`

### Outputs générés
- 8 figures PNG dans `reports/figures/phase4_*.png`
- `reports/phase4_model_comparison.csv`
- `models/best_model_*.pkl`

---

## 📦 requirements.txt

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
jupyter>=1.0
ipykernel
```


---

## 🌿 Règles Git

```bash
# Travailler uniquement sur cette branche
git checkout phase3-phase4-EDA-modeling

# Committer régulièrement
git add notebooks/ reports/ models/ data/processed/
git commit -m "feat: description du changement"
git push origin phase3-phase4-EDA-modeling


```




