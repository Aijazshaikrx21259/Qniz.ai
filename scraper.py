import requests
from bs4 import BeautifulSoup
import json
import time
import random
import os
from datetime import datetime
import pandas as pd

# Liste des whiskys à surveiller
whiskys = [
    {"name": "Ardbeg 10", "aliases": ["Ardbeg 10", "Ardbeg 10 ans", "Ardbeg 10yo"]},
    {"name": "Ardbeg Wee Beastie", "aliases": ["Ardbeg wee beastie", "Ardbeg 5 ans", "Ardbeg 5yo"]},
    {"name": "Ardbeg Uigeadail", "aliases": ["Arbeg Uigeadail", "Ardbeg Uigeadail"]},
    {"name": "Springbank 12 Cask Strength", "aliases": ["Springbank 12 cask strengh", "Springbank 12 CS"]},
    {"name": "Springbank 10", "aliases": ["Springbank 10"]},
    {"name": "Springbank 15", "aliases": ["Springbank 15"]},
    {"name": "Springbank 18", "aliases": ["Springbank 18"]},
    {"name": "Laphroaig 10", "aliases": ["Laphroaig 10"]},
    {"name": "Laphroaig 10 Cask Strength", "aliases": ["Laphroaig 10 cask strengh", "Laphroaig 10 CS"]},
    {"name": "Laphroaig Lore", "aliases": ["Laphroaig Lore"]},
    {"name": "Big Peat 12", "aliases": ["Big Peat 12", "Big Peat 12 ans", "Big Peat 12yo"]},
    {"name": "Big Peat Christmas Edition", "aliases": ["Big Peat Chistmas Edition", "Big Peat Noel"]},
    {"name": "Kilkerran 12", "aliases": ["Kilkerran 12", "Kilkerran 12 ans", "Kilkerran 12yo"]},
    {"name": "Kilkerran 16", "aliases": ["Kilkerran 16", "Kilkerran 16 ans", "Kilkerran 16yo"]},
    {"name": "Kilkerran Heavily Peated Batch 10", "aliases": ["Kilkerran Heavily Peated batch 10"]},
    {"name": "Bunnahabhain 12 Cask Strength", "aliases": ["Bunnahabian 12 cask strengh", "Bunnahabian 12 ans brut de fu", "Bunnahabian 12yo CS"]},
    {"name": "Bunnahabhain 18", "aliases": ["Bunnahabian 18"]},
    {"name": "Bunnahabhain 21", "aliases": ["Bunnahabian 21"]},
    {"name": "Ledaig 10", "aliases": ["Ledaig 10", "Ledaig 10 ans", "Ledaig 10yo"]},
    {"name": "Glen Scotia Victoriana", "aliases": ["Glen Scotia Victoriana"]},
    {"name": "Kilchoman Machir Bay", "aliases": ["Kilchoman Machir Bay"]},
    {"name": "Kilchoman Machir Bay CS", "aliases": ["Kilchoman Machir Bay CS", "Kilchoman Machir Bay cask strengh"]},
    {"name": "Longrow Peated", "aliases": ["Longrow Peated"]},
    {"name": "Bruichladdich The Classic Laddie", "aliases": ["Bruichladdich The Classic Laddie"]},
    {"name": "Port Charlotte 10", "aliases": ["Port Charlotte 10", "Port Charlotte 10 ans", "Port Charlotte 10yo"]},
    {"name": "Lagavulin 16", "aliases": ["Lagavulin 16", "Lagavulin 16 ans", "Lagavulin 16yo"]},
    {"name": "Talisker 10", "aliases": ["Talisker 10", "Talisker 10 ans", "Talisker 10yo"]},
    {"name": "Thor Boyo", "aliases": ["Thor Boyo"]},
    {"name": "Nikka From the Barrel", "aliases": ["Nikka From the Barrel"]},
    {"name": "Hazelburn 10", "aliases": ["Hazelburn 10", "Hazelburn 10 ans", "Hazelburn 10yo"]},
    {"name": "Glenfarclas 105", "aliases": ["Glenfarclas 105"]},
    {"name": "Big Peat Feis Ile", "aliases": ["Big Peat Feis ile"]},
    {"name": "Caol Ila 12", "aliases": ["Caol ila 12", "Caol ila 12 ans", "Caol ila 12yo"]}
]

# Liste des sites web à surveiller
sites = [
    {"name": "Jardin Vouvrillon", "url": "https://www.jardinvouvrillon.fr", "search_url": "https://www.jardinvouvrillon.fr/recherche?controller=search&s={}"},
    {"name": "Whisky.fr", "url": "https://www.whisky.fr", "search_url": "https://www.whisky.fr/catalogsearch/result/?q={}"},
    {"name": "Drankdozijn", "url": "https://drankdozijn.fr", "search_url": "https://drankdozijn.fr/rechercher?q={}"},
    {"name": "Whiskysite", "url": "https://www.whiskysite.nl/en/", "search_url": "https://www.whiskysite.nl/en/search?q={}"},
    {"name": "Prestige Whisky", "url": "https://www.prestigewhisky.fr/", "search_url": "https://www.prestigewhisky.fr/recherche?controller=search&s={}"},
    {"name": "Maltmate", "url": "https://www.maltmate.de/", "search_url": "https://www.maltmate.de/search?sSearch={}"},
    {"name": "Clos des Millesimes", "url": "https://www.closdesmillesimes.com/", "search_url": "https://www.closdesmillesimes.com/recherche?controller=search&s={}"},
    {"name": "Dugas Club Expert", "url": "https://dugasclubexpert.fr/", "search_url": "https://dugasclubexpert.fr/recherche?controller=search&s={}"}
]

# Configuration des headers pour simuler un navigateur
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://www.google.com/'
}

# Fonction pour extraire les prix d'un site web
def extract_prices_from_site(site, whisky):
    result = {
        "price": "Non disponible",
        "available": None,
        "url": None
    }
    
    try:
        # Construction de l'URL de recherche
        search_term = whisky["name"].replace(" ", "+")
        search_url = site["search_url"].format(search_term)
        
        # Envoi de la requête
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Logique d'extraction spécifique à chaque site
            # Note: Ceci est une implémentation simplifiée qui devrait être adaptée pour chaque site
            
            # Recherche générique de prix
            price_elements = soup.select('.price, .product-price, .price-box, [class*="price"]')
            product_links = soup.select('a[href*="{}"]'.format(whisky["name"].lower().replace(" ", "-")))
            
            # Vérification de la disponibilité
            availability_elements = soup.select('.availability, .stock, [class*="stock"], [class*="availability"]')
            
            if price_elements and product_links:
                # Extraction du prix (simplifié)
                price_text = price_elements[0].get_text().strip()
                price = ''.join(filter(lambda x: x.isdigit() or x == ',' or x == '.', price_text))
                
                # Formatage du prix
                if price:
                    try:
                        price_float = float(price.replace(',', '.'))
                        result["price"] = f"{price_float:.2f} €"
                    except ValueError:
                        result["price"] = price_text
                
                # Extraction de l'URL du produit
                result["url"] = product_links[0]['href']
                if not result["url"].startswith('http'):
                    result["url"] = site["url"] + result["url"]
                
                # Vérification de la disponibilité
                if availability_elements:
                    availability_text = availability_elements[0].get_text().lower().strip()
                    result["available"] = not any(term in availability_text for term in ['out of stock', 'épuisé', 'rupture', 'indisponible'])
                else:
                    result["available"] = True  # Par défaut, on suppose disponible si le prix est affiché
            
            # Si aucun résultat n'est trouvé, on essaie avec les alias
            if result["price"] == "Non disponible" and whisky["aliases"]:
                for alias in whisky["aliases"]:
                    search_term = alias.replace(" ", "+")
                    search_url = site["search_url"].format(search_term)
                    
                    response = requests.get(search_url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        price_elements = soup.select('.price, .product-price, .price-box, [class*="price"]')
                        product_links = soup.select('a[href*="{}"]'.format(alias.lower().replace(" ", "-")))
                        
                        if price_elements and product_links:
                            price_text = price_elements[0].get_text().strip()
                            price = ''.join(filter(lambda x: x.isdigit() or x == ',' or x == '.', price_text))
                            
                            if price:
                                try:
                                    price_float = float(price.replace(',', '.'))
                                    result["price"] = f"{price_float:.2f} €"
                                except ValueError:
                                    result["price"] = price_text
                            
                            result["url"] = product_links[0]['href']
                            if not result["url"].startswith('http'):
                                result["url"] = site["url"] + result["url"]
                            
                            result["available"] = True
                            break
    
    except Exception as e:
        print(f"Erreur lors de l'extraction des prix pour {whisky['name']} sur {site['name']}: {str(e)}")
    
    return result

# Fonction principale pour collecter les prix de tous les whiskys sur tous les sites
def collect_all_prices():
    all_data = {
        "whiskies": [],
        "last_updated": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    
    for whisky in whiskys:
        whisky_data = {
            "name": whisky["name"],
            "prices": {},
            "image": f"/static/images/{whisky['name'].lower().replace(' ', '_')}.jpg",
            "history": {}  # Pour stocker l'historique des prix
        }
        
        for site in sites:
            print(f"Collecte des prix pour {whisky['name']} sur {site['name']}...")
            
            # Ajout d'un délai aléatoire pour éviter de surcharger les serveurs
            time.sleep(random.uniform(1, 3))
            
            # Extraction des prix
            price_data = extract_prices_from_site(site, whisky)
            
            # Stockage des données
            whisky_data["prices"][site["name"]] = price_data
        
        all_data["whiskies"].append(whisky_data)
    
    # Sauvegarde des données dans un fichier JSON
    with open('data/whisky_prices.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
    
    print(f"Collecte terminée. Données sauvegardées dans data/whisky_prices.json")
    
    return all_data

# Fonction pour générer un fichier CSV des prix
def generate_price_csv(data):
    rows = []
    
    for whisky in data["whiskies"]:
        row = {"Whisky": whisky["name"]}
        
        for site_name, price_data in whisky["prices"].items():
            price = price_data["price"]
            available = "En stock" if price_data["available"] else "Out of stock" if price_data["available"] is False else "Non vendu"
            row[f"{site_name} - Prix"] = price
            row[f"{site_name} - Disponibilité"] = available
        
        rows.append(row)
    
    df = pd.DataFrame(rows)
    df.to_csv('data/whisky_prices.csv', index=False, encoding='utf-8')
    
    print(f"Fichier CSV généré: data/whisky_prices.csv")

# Fonction pour créer des données de test (à utiliser pendant le développement)
def create_test_data():
    all_data = {
        "whiskies": [],
        "last_updated": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    
    for whisky in whiskys:
        whisky_data = {
            "name": whisky["name"],
            "prices": {},
            "image": f"/static/images/{whisky['name'].lower().replace(' ', '_')}.jpg",
            "history": {}
        }
        
        for site in sites:
            # Génération de données aléatoires pour les tests
            price = round(random.uniform(40, 200), 2)
            available = random.choice([True, False, None])
            
            price_data = {
                "price": f"{price:.2f} €" if available is not None else "Non disponible",
                "available": available,
                "url": f"{site['url']}/product/{whisky['name'].lower().replace(' ', '-')}" if available is not None else None
            }
            
            whisky_data["prices"][site["name"]] = price_data
        
        # Ajout de données historiques fictives
        dates = ["01/01/2025", "01/02/2025", "01/03/2025", "01/04/2025"]
        whisky_data["history"] = {
            site["name"]: {
                date: f"{round(random.uniform(40, 200), 2):.2f} €" for date in dates
            } for site in sites
        }
        
        all_data["whiskies"].append(whisky_data)
    
    # Sauvegarde des données dans un fichier JSON
    os.makedirs('data', exist_ok=True)
    with open('data/whisky_prices.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
    
    print(f"Données de test générées et sauvegardées dans data/whisky_prices.json")
    
    return all_data

if __name__ == "__main__":
    # Pour le développement, utiliser des données de test
    # En production, utiliser la collecte réelle
    print("Génération de données de test pour le développement...")
    data = create_test_data()
    
    # Génération du fichier CSV
    generate_price_csv(data)
    
    print("Script terminé avec succès.")
