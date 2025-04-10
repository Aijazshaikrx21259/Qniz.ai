# Guide de déploiement et d'utilisation du site de suivi des prix de whisky

## Introduction

Ce document explique comment déployer et utiliser le site web de suivi des prix de whisky que nous avons développé. Le site permet de suivre l'évolution des prix de différents whiskys sur plusieurs sites marchands au fil du temps.

## Structure du projet

Le projet est organisé comme suit :

```
whisky_tracker/
├── index.html              # Page d'accueil
├── whisky_detail.html      # Page de détail pour chaque whisky
├── compare.html            # Page de comparaison des prix
├── static/                 # Ressources statiques
│   ├── css/                # Feuilles de style
│   │   └── style.css       # Style principal
│   ├── js/                 # Scripts JavaScript
│   │   ├── main.js         # Script principal
│   │   ├── detail.js       # Script pour la page de détail
│   │   ├── compare.js      # Script pour la page de comparaison
│   │   └── price_tracker.js # Script pour le suivi temporel des prix
│   └── images/             # Images des whiskys
├── data/                   # Données des prix
│   └── whisky_prices.json  # Données des prix des whiskys
├── scraper.py              # Script pour collecter les prix
└── image_collector.py      # Script pour collecter les images
```

## Déploiement sur HuggingFace Spaces

Pour déployer le site sur HuggingFace Spaces (https://huggingface.co/spaces/enzostvs/deepsite), suivez ces étapes :

1. Téléchargez l'ensemble du projet depuis ce sandbox
2. Connectez-vous à votre compte HuggingFace
3. Accédez à https://huggingface.co/spaces/enzostvs/deepsite
4. Cliquez sur "Files" puis utilisez l'option "Upload files" pour téléverser tous les fichiers du projet
5. Assurez-vous que le fichier index.html est à la racine du dépôt

## Utilisation du site

### Page d'accueil

La page d'accueil présente une grille de tous les whiskys avec leurs fourchettes de prix. Vous pouvez :
- Rechercher un whisky spécifique avec la barre de recherche
- Cliquer sur un whisky pour voir ses détails
- Utiliser les boutons en haut pour gérer l'historique des prix

### Page de détail

La page de détail d'un whisky affiche :
- Une image du whisky
- Un tableau des prix actuels sur différents sites
- Un graphique de l'évolution des prix dans le temps
- Un bouton pour enregistrer le prix actuel dans l'historique

### Page de comparaison

La page de comparaison permet de :
- Sélectionner plusieurs whiskys à comparer
- Filtrer par site marchand
- Comparer les prix à différentes dates
- Visualiser l'évolution des prix dans le temps

## Fonctionnalités de suivi temporel

Le site offre plusieurs fonctionnalités pour suivre l'évolution des prix dans le temps :

1. **Enregistrer les prix actuels** : Sauvegarde les prix actuels comme point historique
2. **Exporter l'historique** : Télécharge l'historique des prix au format CSV
3. **Importer un historique** : Permet d'importer un fichier CSV d'historique de prix
4. **Générer des données de démonstration** : Crée des données historiques fictives pour la démonstration

## Maintenance et amélioration

Pour mettre à jour les prix, exécutez le script `scraper.py` :

```
python3 scraper.py
```

Pour ajouter de nouveaux whiskys ou sites marchands, modifiez le fichier `scraper.py` et ajoutez les nouvelles sources.

## Améliorations futures possibles

- Ajouter plus de sites web à surveiller
- Implémenter un système de notifications pour les changements de prix
- Ajouter des filtres par région ou type de whisky
- Intégrer des avis et notes pour chaque whisky
- Automatiser la collecte des prix avec une tâche planifiée
