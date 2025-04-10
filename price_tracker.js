// price_tracker.js - Script pour le suivi temporel des prix

// Fonction pour sauvegarder les données actuelles comme point historique
function saveCurrentPricesAsHistoryPoint() {
    // Chargement des données actuelles
    fetch('data/whisky_prices.json')
        .then(response => response.json())
        .then(data => {
            // Création d'un point d'historique avec la date actuelle
            const currentDate = new Date().toLocaleDateString('fr-FR');
            
            // Pour chaque whisky, ajouter les prix actuels à l'historique
            data.whiskies.forEach(whisky => {
                if (!whisky.history) {
                    whisky.history = {};
                }
                
                // Pour chaque site, ajouter le prix actuel à l'historique
                Object.entries(whisky.prices).forEach(([site, priceData]) => {
                    if (!whisky.history[site]) {
                        whisky.history[site] = {};
                    }
                    
                    // Sauvegarder le prix actuel dans l'historique
                    if (priceData.price && priceData.price !== "Non disponible") {
                        whisky.history[site][currentDate] = priceData.price;
                    }
                });
            });
            
            // Mise à jour de la date de dernière mise à jour
            data.last_updated = new Date().toLocaleString('fr-FR');
            
            // Sauvegarde des données mises à jour
            return saveDataToLocalStorage(data);
        })
        .then(() => {
            console.log('Historique des prix mis à jour avec succès');
            alert('Historique des prix mis à jour avec succès');
        })
        .catch(error => {
            console.error('Erreur lors de la mise à jour de l\'historique des prix:', error);
            alert('Erreur lors de la mise à jour de l\'historique des prix');
        });
}

// Fonction pour sauvegarder les données dans le localStorage
function saveDataToLocalStorage(data) {
    return new Promise((resolve, reject) => {
        try {
            localStorage.setItem('whisky_prices_data', JSON.stringify(data));
            resolve();
        } catch (error) {
            reject(error);
        }
    });
}

// Fonction pour charger les données depuis le localStorage
function loadDataFromLocalStorage() {
    return new Promise((resolve, reject) => {
        try {
            const data = localStorage.getItem('whisky_prices_data');
            if (data) {
                resolve(JSON.parse(data));
            } else {
                // Si pas de données dans le localStorage, charger depuis le fichier JSON
                fetch('data/whisky_prices.json')
                    .then(response => response.json())
                    .then(data => {
                        // Sauvegarder dans le localStorage pour utilisation future
                        localStorage.setItem('whisky_prices_data', JSON.stringify(data));
                        resolve(data);
                    })
                    .catch(reject);
            }
        } catch (error) {
            reject(error);
        }
    });
}

// Fonction pour exporter l'historique des prix
function exportPriceHistory() {
    loadDataFromLocalStorage()
        .then(data => {
            // Conversion des données en format CSV
            let csvContent = "data:text/csv;charset=utf-8,";
            
            // En-tête du CSV
            csvContent += "Whisky,Site,Date,Prix\n";
            
            // Ajout des données d'historique
            data.whiskies.forEach(whisky => {
                if (whisky.history) {
                    Object.entries(whisky.history).forEach(([site, dates]) => {
                        Object.entries(dates).forEach(([date, price]) => {
                            csvContent += `"${whisky.name}","${site}","${date}","${price}"\n`;
                        });
                    });
                }
            });
            
            // Création d'un lien de téléchargement
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "historique_prix_whisky.csv");
            document.body.appendChild(link);
            
            // Téléchargement du fichier
            link.click();
            
            // Nettoyage
            document.body.removeChild(link);
        })
        .catch(error => {
            console.error('Erreur lors de l\'exportation de l\'historique des prix:', error);
            alert('Erreur lors de l\'exportation de l\'historique des prix');
        });
}

// Fonction pour importer un historique de prix
function importPriceHistory(fileInput) {
    const file = fileInput.files[0];
    if (!file) {
        alert('Veuillez sélectionner un fichier CSV');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        const content = e.target.result;
        const lines = content.split('\n');
        
        // Ignorer l'en-tête
        const dataLines = lines.slice(1);
        
        // Chargement des données actuelles
        loadDataFromLocalStorage()
            .then(data => {
                // Traitement de chaque ligne du CSV
                dataLines.forEach(line => {
                    if (!line.trim()) return; // Ignorer les lignes vides
                    
                    const [whiskyName, site, date, price] = line.split(',').map(item => item.replace(/"/g, '').trim());
                    
                    // Recherche du whisky correspondant
                    const whisky = data.whiskies.find(w => w.name === whiskyName);
                    if (whisky) {
                        if (!whisky.history) {
                            whisky.history = {};
                        }
                        if (!whisky.history[site]) {
                            whisky.history[site] = {};
                        }
                        
                        // Ajout du point d'historique
                        whisky.history[site][date] = price;
                    }
                });
                
                // Sauvegarde des données mises à jour
                return saveDataToLocalStorage(data);
            })
            .then(() => {
                console.log('Historique des prix importé avec succès');
                alert('Historique des prix importé avec succès');
                
                // Recharger la page pour afficher les nouvelles données
                window.location.reload();
            })
            .catch(error => {
                console.error('Erreur lors de l\'importation de l\'historique des prix:', error);
                alert('Erreur lors de l\'importation de l\'historique des prix');
            });
    };
    
    reader.readAsText(file);
}

// Fonction pour générer des données historiques fictives (pour la démonstration)
function generateDemoHistoricalData() {
    // Chargement des données actuelles
    fetch('data/whisky_prices.json')
        .then(response => response.json())
        .then(data => {
            // Dates pour l'historique (6 derniers mois)
            const dates = [];
            const today = new Date();
            for (let i = 6; i >= 0; i--) {
                const date = new Date(today);
                date.setMonth(today.getMonth() - i);
                dates.push(date.toLocaleDateString('fr-FR'));
            }
            
            // Pour chaque whisky, générer un historique fictif
            data.whiskies.forEach(whisky => {
                whisky.history = {};
                
                // Pour chaque site, générer un historique de prix
                Object.entries(whisky.prices).forEach(([site, priceData]) => {
                    whisky.history[site] = {};
                    
                    // Prix de base (actuel ou aléatoire)
                    let basePrice = 0;
                    if (priceData.price && priceData.price !== "Non disponible") {
                        basePrice = parseFloat(priceData.price.replace('€', '').trim());
                    } else {
                        basePrice = Math.random() * 100 + 50; // Prix aléatoire entre 50 et 150 €
                    }
                    
                    // Génération de l'historique avec des variations aléatoires
                    dates.forEach(date => {
                        // Variation aléatoire entre -10% et +10%
                        const variation = (Math.random() * 0.2 - 0.1);
                        const historicalPrice = basePrice * (1 + variation);
                        whisky.history[site][date] = `${historicalPrice.toFixed(2)} €`;
                    });
                });
            });
            
            // Mise à jour de la date de dernière mise à jour
            data.last_updated = new Date().toLocaleString('fr-FR');
            
            // Sauvegarde des données mises à jour
            const dataStr = JSON.stringify(data, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            const dataUrl = URL.createObjectURL(dataBlob);
            
            // Création d'un lien de téléchargement
            const link = document.createElement("a");
            link.href = dataUrl;
            link.download = "whisky_prices_with_history.json";
            document.body.appendChild(link);
            
            // Téléchargement du fichier
            link.click();
            
            // Nettoyage
            document.body.removeChild(link);
            URL.revokeObjectURL(dataUrl);
            
            alert('Données historiques fictives générées avec succès. Veuillez remplacer le fichier data/whisky_prices.json par le fichier téléchargé pour voir l\'historique des prix.');
        })
        .catch(error => {
            console.error('Erreur lors de la génération des données historiques:', error);
            alert('Erreur lors de la génération des données historiques');
        });
}
