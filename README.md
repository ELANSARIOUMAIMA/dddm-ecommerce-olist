# 🛒 Projet Data-Driven Decision Making — E-Commerce Olist

> **Module** : Data-Driven Decision Making  
> **Dataset** : [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)  
> **Date limite** : 07 Juin 2026  
> **Équipe** : 3 membres

---

## 📌 Contexte & Objectif

Ce projet applique l'intégralité du pipeline décisionnel basé sur la donnée sur un cas réel d'e-commerce brésilien. La plateforme **Olist** connecte des petits vendeurs à de grands canaux de vente en ligne. Le dataset couvre **~100 000 commandes réelles** sur la période 2016–2018.

**Question décisionnelle centrale :**
> Comment identifier les segments clients les plus rentables et optimiser les décisions marketing et logistiques pour maximiser le chiffre d'affaires de la plateforme ?

---

## 👥 Répartition des Tâches

| Membre | Phases | Description |
|--------|--------|-------------|
| Membre 1 | Phase 1 & 2 | Définition du problème, KPIs, Collecte & Audit des données |
| Membre 2 | Phase 3 & 4 | EDA, Analyse statistique, Modélisation prédictive |
| Membre 3 | Phase 5 & 6 | Dashboard, A/B Testing, Présentation exécutive |

---

## 📁 Structure du Projet

```
dddm-ecommerce-olist/
│
├── data/
│   └── raw/                        # Données brutes (non versionnées - voir ci-dessous)
│       ├── olist_orders_dataset.csv
│       ├── olist_customers_dataset.csv
│       ├── olist_order_items_dataset.csv
│       ├── olist_order_payments_dataset.csv
│       ├── olist_order_reviews_dataset.csv
│       ├── olist_products_dataset.csv
│       ├── olist_sellers_dataset.csv
│       ├── olist_geolocation_dataset.csv
│       └── product_category_name_translation.csv
│
├── notebooks/
│   ├── phase1_problem_definition.ipynb   # KPIs, Business Case, KPI Tree
│   ├── phase2_data_audit.ipynb           # Audit, Data Dictionary, Gaps
│   ├── phase3_eda.ipynb                  # Exploration statistique
│   └── phase4_modeling.ipynb             # Modèles prédictifs
│
├── reports/
│   └── DDDM_Phase1_Phase2.docx           # Rapport détaillé Phases 1 & 2
│
├── dashboard/                            # Dashboard interactif (Phase 5)
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Lancement

### 1. Cloner le repo

```bash
git clone https://github.com/TON_USERNAME/dddm-ecommerce-olist.git
cd dddm-ecommerce-olist
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Télécharger le dataset

Les fichiers CSV ne sont pas versionnés (trop volumineux). Télécharge le dataset manuellement :

1. Va sur : https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
2. Clique sur **Download**
3. Extrais le contenu dans `data/raw/`

### 4. Lancer les notebooks

```bash
jupyter notebook
```

Ouvre les notebooks dans l'ordre : `phase1` → `phase2` → `phase3` → `phase4`

---

## 📊 Dataset — Brazilian E-Commerce (Olist)

| Fichier | Contenu | Lignes |
|---------|---------|--------|
| olist_orders_dataset.csv | Commandes, statuts, dates | ~99 441 |
| olist_customers_dataset.csv | Clients, localisation | ~99 441 |
| olist_order_items_dataset.csv | Articles, prix, livraison | ~112 650 |
| olist_order_payments_dataset.csv | Paiements, montants | ~103 886 |
| olist_order_reviews_dataset.csv | Avis clients (1-5 étoiles) | ~99 224 |
| olist_products_dataset.csv | Produits, catégories | ~32 951 |
| olist_sellers_dataset.csv | Vendeurs, localisation | ~3 095 |
| olist_geolocation_dataset.csv | Coordonnées GPS par CEP | ~1 000 163 |
| product_category_name_translation.csv | Traduction catégories PT→EN | ~71 |

> **Volume total** : > 50 000 lignes ✅ | **Sources combinées** : 2+ ✅

---

## 🎯 KPIs Principaux

| KPI | Type | Cible |
|-----|------|-------|
| Chiffre d'Affaires Total | Primaire | Suivi mensuel |
| Valeur Moyenne Commande (AOV) | Primaire | > R$ 150 |
| Taux de Rétention Client | Primaire | > 15% |
| Score Satisfaction (NPS proxy) | Primaire | > 4.0 / 5 |
| Taux Livraison dans les Délais | Secondaire | > 90% |
| Taux d'Annulation Commandes | Secondaire | < 3% |

---

## 🌿 Branches Git

| Branche | Rôle |
|---------|------|
| `main` | Version finale stable — ne pas modifier directement |
| `dev` | Branche d'intégration — merge des phases terminées |
| `phase1-phase2-data-audit` | Phases 1 & 2 (Membre 1) |
| `phase3-eda` | Phase 3 & 4 (Membre 2) |
| `phase5-dashboard` | Phase 5 & 6 (Membre 3) |

---

## 📦 Livrables Finaux

- [x] Notebook Jupyter complet et reproductible
- [x] `requirements.txt`
- [ ] Dashboard interactif (Phase 5)
- [x] Rapport Word — Phases 1 & 2
- [ ] Data Story — 15 slides (Phase 6)
- [ ] A/B Test Plan — 2 pages (Phase 6)
- [x] Dépôt Git public

---

## 🛠️ Stack Technique

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Pandas](https://img.shields.io/badge/Pandas-2.1-green)
![Scikit--learn](https://img.shields.io/badge/Scikit--learn-1.3-orange)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-yellow)
![Plotly](https://img.shields.io/badge/Plotly-5.15-purple)
