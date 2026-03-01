# Gestion de Stock — Application Desktop Python

Application de bureau complète de gestion d'inventaire développée en Python 3.10+
avec **PyQt6** (interface graphique), **SQLAlchemy** (ORM) et **SQLite** (base de données).

---

## Table des matières

1. [Aperçu](#aperçu)
2. [Fonctionnalités](#fonctionnalités)
3. [Architecture du projet](#architecture-du-projet)
4. [Prérequis système](#prérequis-système)
5. [Installation pas à pas](#installation-pas-à-pas)
   - [Windows](#windows)
   - [macOS](#macos)
   - [Linux (Ubuntu / Debian)](#linux-ubuntu--debian)
6. [Lancement de l'application](#lancement-de-lapplication)
7. [Utilisation](#utilisation)
8. [Structure de la base de données](#structure-de-la-base-de-données)
9. [Développement](#développement)
10. [Dépannage](#dépannage)

---

## Aperçu

L'application permet de gérer l'inventaire de produits d'une entreprise via une
interface graphique intuitive. Les données sont persistées localement dans un
fichier SQLite (`data/inventory.db`), ce qui ne nécessite aucun serveur de base
de données externe.

---

## Fonctionnalités

| Fonctionnalité | Description |
|---|---|
| Affichage des produits | Tableau complet avec tri par colonne |
| Ajout de produit | Formulaire modal avec validation |
| Modification de produit | Pré-remplissage automatique du formulaire |
| Suppression de produit | Avec demande de confirmation |
| Recherche | Recherche en temps réel par nom ou référence |
| Alerte stock faible | Mise en évidence visuelle + filtre dédié |
| Catégories | Affectation de produits à des catégories |

---

## Architecture du projet

```
inventory_desktop_app/
│
├── data/                        # Fichier SQLite (créé automatiquement)
│   └── inventory.db
│
├── src/
│   ├── __init__.py
│   ├── models/                  # Couche M — Modèles SQLAlchemy
│   │   ├── __init__.py
│   │   ├── database.py          # Engine, Session, Base, init_db()
│   │   └── product.py           # Modèles ORM : Category, Product
│   │
│   ├── controllers/             # Couche C — Logique métier CRUD
│   │   ├── __init__.py
│   │   └── inventory_controller.py
│   │
│   └── views/                   # Couche V — Interface PyQt6
│       ├── __init__.py
│       ├── main_window.py       # Fenêtre principale + tableau
│       └── product_form.py      # Formulaire ajout / modification
│
├── main.py                      # Point d'entrée
├── requirements.txt             # Dépendances Python
└── README.md                    # Ce fichier
```

L'architecture suit le patron **MVC** :

- **Modèles** (`src/models/`) — définissent le schéma de données via SQLAlchemy ORM.
- **Contrôleur** (`src/controllers/`) — contient toute la logique métier ; chaque méthode
  ouvre et ferme sa propre session SQLAlchemy pour éviter les verrous SQLite.
- **Vues** (`src/views/`) — interface PyQt6 ; ne contiennent aucune logique métier.

---

## Prérequis système

| Logiciel | Version minimale | Remarque |
|---|---|---|
| Python | 3.10 | 3.11 ou 3.12 recommandé |
| pip | 22.0 | Inclus avec Python |
| Git | Toute version récente | Pour cloner le dépôt |

> **Note :** PyQt6 nécessite des bibliothèques graphiques système.
> Voir la section [Linux](#linux-ubuntu--debian) pour les détails.

---

## Installation pas à pas

### Windows

#### 1. Installer Python

1. Télécharger Python 3.12 depuis [python.org](https://www.python.org/downloads/windows/).
2. Pendant l'installation, **cocher** « Add Python to PATH ».
3. Vérifier l'installation :

```powershell
python --version
pip --version
```

#### 2. Cloner le dépôt

```powershell
git clone <URL_DU_DEPOT>
cd inventory_desktop_app
```

#### 3. Créer et activer un environnement virtuel

```powershell
python -m venv .venv
.venv\Scripts\activate
```

> Votre invite de commandes affichera `(.venv)` quand l'environnement est actif.

#### 4. Installer les dépendances

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. Lancer l'application

```powershell
python main.py
```

---

### macOS

#### 1. Installer Python via Homebrew (recommandé)

```bash
# Installer Homebrew si ce n'est pas déjà fait
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Installer Python
brew install python@3.12
```

Ou télécharger directement depuis [python.org](https://www.python.org/downloads/macos/).

Vérifier :

```bash
python3 --version
pip3 --version
```

#### 2. Cloner le dépôt

```bash
git clone <URL_DU_DEPOT>
cd inventory_desktop_app
```

#### 3. Créer et activer un environnement virtuel

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 4. Installer les dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. Lancer l'application

```bash
python main.py
```

> **macOS Ventura / Sonoma :** Si une fenêtre noire s'affiche, relancez avec
> `OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES python main.py`.

---

### Linux (Ubuntu / Debian)

#### 1. Installer Python et les dépendances système

```bash
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-dev python3-pip git

# Bibliothèques graphiques requises par PyQt6
sudo apt install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libdbus-1-3 \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    libxkbcommon-x11-0 \
    libfontconfig1
```

> Sur **Fedora / RHEL** :
> ```bash
> sudo dnf install python3.12 python3.12-devel mesa-libGL glib2 dbus
> ```

#### 2. Cloner le dépôt

```bash
git clone <URL_DU_DEPOT>
cd inventory_desktop_app
```

#### 3. Créer et activer un environnement virtuel

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

#### 4. Installer les dépendances Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. Lancer l'application

```bash
python main.py
```

> **Serveur sans affichage (headless) :** Installez un serveur X virtuel :
> ```bash
> sudo apt install -y xvfb
> xvfb-run python main.py
> ```

---

## Lancement de l'application

```bash
# Activer l'environnement virtuel (si ce n'est pas déjà fait)
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

# Lancer
python main.py
```

Au premier lancement, le fichier `data/inventory.db` est créé automatiquement
et les tables sont initialisées.

---

## Utilisation

### Interface principale

| Zone | Rôle |
|---|---|
| Barre d'outils | Boutons Ajouter / Modifier / Supprimer / Actualiser / Filtre stock faible |
| Barre de recherche | Filtrage en temps réel par nom ou référence |
| Tableau | Liste des produits ; cliquer sur un en-tête pour trier |
| Barre de statut | Nombre de produits affichés + alertes stock faible |

### Raccourcis clavier

| Raccourci | Action |
|---|---|
| `Ctrl+N` | Ajouter un produit |
| `Ctrl+E` | Modifier le produit sélectionné |
| `Del` | Supprimer le produit sélectionné |
| `F5` | Actualiser la liste |
| Double-clic | Ouvrir le formulaire de modification |

### Alertes stock faible

Un produit est considéré en **stock faible** lorsque sa quantité est **inférieure ou
égale à son seuil d'alerte**. Ces lignes apparaissent en orange dans le tableau.
Le bouton **⚠ Stock faible** filtre la liste pour n'afficher que ces produits.

---

## Structure de la base de données

### Table `categories`

| Colonne | Type | Description |
|---|---|---|
| `id` | INTEGER | Clé primaire auto-incrémentée |
| `nom` | VARCHAR(100) | Nom unique de la catégorie |

### Table `products`

| Colonne | Type | Description |
|---|---|---|
| `id` | INTEGER | Clé primaire auto-incrémentée |
| `nom` | VARCHAR(200) | Nom du produit |
| `reference` | VARCHAR(100) | Référence unique |
| `quantite` | INTEGER | Quantité en stock |
| `prix` | FLOAT | Prix unitaire en euros |
| `seuil_alerte` | INTEGER | Seuil déclenchant l'alerte stock faible |
| `category_id` | INTEGER | Clé étrangère vers `categories.id` (nullable) |
| `created_at` | DATETIME | Date de création (automatique) |
| `updated_at` | DATETIME | Date de dernière modification (automatique) |

---

## Développement

### Ajouter des dépendances

```bash
pip install <package>
pip freeze > requirements.txt
```

### Étendre les modèles

1. Modifier `src/models/product.py` pour ajouter des colonnes.
2. Supprimer `data/inventory.db` pour une base vierge **OU** utiliser
   [Alembic](https://alembic.sqlalchemy.org/) pour des migrations sans perte de données.

### Étendre le contrôleur

Toutes les nouvelles méthodes CRUD doivent utiliser le pattern :

```python
with self._session() as session:
    # opérations...
```

Cela garantit que la session est toujours fermée, même en cas d'exception.

### Ajouter une nouvelle vue

1. Créer un fichier dans `src/views/`.
2. L'importer et l'instancier depuis `main_window.py` ou `main.py`.

---

## Dépannage

| Problème | Cause probable | Solution |
|---|---|---|
| `ModuleNotFoundError: PyQt6` | Dépendances non installées | `pip install -r requirements.txt` dans le bon environnement virtuel |
| `qt.qpa.plugin: Could not load the Qt platform plugin "xcb"` | Bibliothèques système manquantes | Voir section [Linux](#linux-ubuntu--debian), étape 1 |
| `OperationalError: database is locked` | Session SQLite non fermée | Toujours utiliser `with self._session() as session:` |
| Fenêtre noire sur macOS | Problème fork safety | `OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES python main.py` |
| `python: command not found` | Python non dans le PATH | Utiliser `python3` au lieu de `python`, ou réinstaller Python en cochant "Add to PATH" |

---

*Projet généré avec Python 3.12 · PyQt6 · SQLAlchemy 2.x · SQLite*
