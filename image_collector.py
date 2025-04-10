import os
import requests
import json
from PIL import Image
from io import BytesIO
import time
import random
from bs4 import BeautifulSoup

# Configuration des headers pour simuler un navigateur
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://www.google.com/'
}

# Fonction pour rechercher des images de whisky
def search_whisky_images(whisky_name):
    search_term = f"{whisky_name} whisky bottle"
    search_url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}&tbm=isch"
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Recherche des balises d'images
            img_tags = soup.find_all('img')
            
            # Extraction des URLs d'images (après la première qui est généralement le logo Google)
            img_urls = []
            for img in img_tags[1:6]:  # Prendre quelques images pour avoir des options
                if img.has_attr('src') and 'http' in img['src']:
                    img_urls.append(img['src'])
                elif img.has_attr('data-src') and 'http' in img['data-src']:
                    img_urls.append(img['data-src'])
            
            return img_urls
        else:
            print(f"Erreur lors de la recherche d'images pour {whisky_name}: {response.status_code}")
            return []
    except Exception as e:
        print(f"Exception lors de la recherche d'images pour {whisky_name}: {str(e)}")
        return []

# Fonction pour télécharger et optimiser une image
def download_and_optimize_image(img_url, whisky_name, save_path):
    try:
        response = requests.get(img_url, headers=headers, timeout=10)
        if response.status_code == 200:
            # Ouvrir l'image avec PIL
            img = Image.open(BytesIO(response.content))
            
            # Redimensionner l'image si nécessaire
            max_size = (500, 500)
            img.thumbnail(max_size, Image.LANCZOS)
            
            # Convertir en RGB si nécessaire (pour les images avec transparence)
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
                img = background
            
            # Sauvegarder l'image optimisée
            img.save(save_path, 'JPEG', quality=85, optimize=True)
            print(f"Image sauvegardée pour {whisky_name}: {save_path}")
            return True
        else:
            print(f"Erreur lors du téléchargement de l'image pour {whisky_name}: {response.status_code}")
            return False
    except Exception as e:
        print(f"Exception lors du téléchargement de l'image pour {whisky_name}: {str(e)}")
        return False

# Fonction principale pour collecter les images de tous les whiskys
def collect_all_whisky_images():
    # Charger les données des whiskys
    try:
        with open('data/whisky_prices.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Fichier de données non trouvé. Veuillez d'abord exécuter le script de collecte des prix.")
        return
    
    # Créer le dossier d'images s'il n'existe pas
    os.makedirs('static/images', exist_ok=True)
    
    # Pour chaque whisky, rechercher et télécharger une image
    for whisky in data["whiskies"]:
        whisky_name = whisky["name"]
        file_name = whisky_name.lower().replace(' ', '_') + '.jpg'
        save_path = os.path.join('static/images', file_name)
        
        print(f"Recherche d'images pour {whisky_name}...")
        
        # Vérifier si l'image existe déjà
        if os.path.exists(save_path):
            print(f"Image déjà existante pour {whisky_name}: {save_path}")
            continue
        
        # Rechercher des images
        img_urls = search_whisky_images(whisky_name)
        
        if img_urls:
            # Essayer de télécharger la première image, puis les suivantes si échec
            success = False
            for img_url in img_urls:
                time.sleep(random.uniform(1, 2))  # Délai pour éviter de surcharger les serveurs
                success = download_and_optimize_image(img_url, whisky_name, save_path)
                if success:
                    # Mettre à jour le chemin de l'image dans les données
                    whisky["image"] = f"/static/images/{file_name}"
                    break
            
            if not success:
                print(f"Impossible de télécharger une image pour {whisky_name}, utilisation de l'image placeholder")
                whisky["image"] = "/static/images/placeholder.jpg"
        else:
            print(f"Aucune image trouvée pour {whisky_name}, utilisation de l'image placeholder")
            whisky["image"] = "/static/images/placeholder.jpg"
        
        # Ajouter un délai entre les recherches pour éviter d'être bloqué
        time.sleep(random.uniform(2, 4))
    
    # Sauvegarder les données mises à jour
    with open('data/whisky_prices.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("Collecte d'images terminée.")

# Fonction pour générer des images de test (à utiliser pendant le développement)
def create_test_images():
    # Charger les données des whiskys
    try:
        with open('data/whisky_prices.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Fichier de données non trouvé. Veuillez d'abord exécuter le script de collecte des prix.")
        return
    
    # Créer le dossier d'images s'il n'existe pas
    os.makedirs('static/images', exist_ok=True)
    
    # Utiliser l'image placeholder pour tous les whiskys (pour le développement)
    for whisky in data["whiskies"]:
        whisky_name = whisky["name"]
        file_name = whisky_name.lower().replace(' ', '_') + '.jpg'
        save_path = os.path.join('static/images', file_name)
        
        # Copier l'image placeholder
        try:
            img = Image.open('static/images/placeholder.jpg')
            img.save(save_path)
            print(f"Image de test créée pour {whisky_name}: {save_path}")
            
            # Mettre à jour le chemin de l'image dans les données
            whisky["image"] = f"/static/images/{file_name}"
        except Exception as e:
            print(f"Erreur lors de la création de l'image de test pour {whisky_name}: {str(e)}")
            whisky["image"] = "/static/images/placeholder.jpg"
    
    # Sauvegarder les données mises à jour
    with open('data/whisky_prices.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("Création d'images de test terminée.")

if __name__ == "__main__":
    # Pour le développement, utiliser des images de test
    # En production, utiliser la collecte réelle d'images
    print("Création d'images de test pour le développement...")
    create_test_images()
    
    print("Script terminé avec succès.")
