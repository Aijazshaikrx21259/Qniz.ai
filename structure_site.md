# Structure du site web de suivi des prix de whisky

## Vue d'ensemble
Le site web de suivi des prix de whisky est conçu pour permettre aux utilisateurs de suivre l'évolution des prix de différents whiskys sur plusieurs sites marchands au fil du temps. La structure du site est organisée de manière à offrir une navigation intuitive et une visualisation claire des données.

## Pages principales

### 1. Page d'accueil (index.html)
- **Objectif**: Présenter une vue d'ensemble des whiskys suivis et permettre une navigation rapide
- **Contenu**:
  - En-tête avec logo et menu de navigation
  - Section d'introduction expliquant le but du site
  - Grille de cartes pour chaque whisky avec:
    - Image du whisky
    - Nom du whisky
    - Fourchette de prix (min-max)
    - Lien vers la page de détail
  - Barre de recherche pour filtrer les whiskys
  - Pied de page avec informations de copyright

### 2. Page de détail du whisky (whisky_detail.html)
- **Objectif**: Afficher les informations détaillées d'un whisky spécifique
- **Contenu**:
  - Image du whisky
  - Nom et description du whisky
  - Tableau des prix actuels sur différents sites avec:
    - Nom du site
    - Prix
    - Disponibilité (en stock, rupture de stock, non vendu)
    - Lien vers la page produit sur le site marchand
  - Graphique d'évolution des prix dans le temps
  - Options pour filtrer l'affichage par site ou par période

### 3. Page de comparaison (compare.html)
- **Objectif**: Permettre la comparaison des prix entre plusieurs whiskys
- **Contenu**:
  - Sélecteur de whiskys à comparer
  - Sélecteur de sites à inclure dans la comparaison
  - Tableau comparatif des prix
  - Graphique comparatif des prix
  - Options pour filtrer par période

## Composants techniques

### Backend (Flask)
- **app.py**: Application principale Flask
- **Routes**:
  - `/`: Page d'accueil
  - `/whisky/<whisky_name>`: Page de détail d'un whisky
  - `/compare`: Page de comparaison
  - `/api/whiskies`: API pour récupérer la liste des whiskys
  - `/api/whisky/<whisky_name>`: API pour récupérer les détails d'un whisky

### Frontend
- **Templates**:
  - `index.html`: Template de la page d'accueil
  - `whisky_detail.html`: Template de la page de détail
  - `compare.html`: Template de la page de comparaison
- **CSS**:
  - `style.css`: Styles principaux du site
- **JavaScript**:
  - `main.js`: Script pour la page d'accueil
  - `detail.js`: Script pour la page de détail
  - `compare.js`: Script pour la page de comparaison

### Données
- **Format JSON**:
  - Liste des whiskys
  - Prix actuels par site
  - Historique des prix
  - Métadonnées (date de dernière mise à jour)
- **Images**:
  - Images des bouteilles de whisky
  - Image placeholder pour les whiskys sans image

## Fonctionnalités clés
1. Affichage des prix actuels de chaque whisky sur différents sites
2. Suivi de l'évolution des prix dans le temps avec visualisations graphiques
3. Comparaison des prix entre différents whiskys
4. Recherche et filtrage des whiskys
5. Liens directs vers les pages produits sur les sites marchands
6. Indication claire de la disponibilité des produits

## Flux de données
1. Les données sont collectées via le script de scraping (`scraper.py`)
2. Les données sont stockées au format JSON (`data/whisky_prices.json`)
3. L'application Flask charge les données et les expose via des API
4. Le frontend récupère les données via les API et les affiche dans l'interface utilisateur

## Considérations de conception
- **Responsive design**: Le site s'adapte à différentes tailles d'écran
- **Performance**: Chargement asynchrone des données pour une expérience utilisateur fluide
- **Accessibilité**: Contraste suffisant, textes alternatifs pour les images
- **Expérience utilisateur**: Interface intuitive et navigation claire
