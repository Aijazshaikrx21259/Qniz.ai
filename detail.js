// detail.js - Script pour la page de détail d'un whisky

document.addEventListener('DOMContentLoaded', function() {
    // Récupération du nom du whisky depuis l'URL
    const whiskyName = document.querySelector('.whisky-detail h2').textContent;
    
    // Récupération des données du whisky
    fetchWhiskyData(whiskyName);
});

// Fonction pour récupérer les données d'un whisky spécifique
function fetchWhiskyData(whiskyName) {
    fetch(`/api/whisky/${encodeURIComponent(whiskyName)}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error);
            } else {
                displayWhiskyInfo(data);
                displayPriceTable(data);
                displayPriceHistory(data);
            }
        })
        .catch(error => {
            console.error('Erreur lors de la récupération des données:', error);
            showError('Erreur lors du chargement des données. Veuillez réessayer plus tard.');
        });
}

// Fonction pour afficher les informations du whisky
function displayWhiskyInfo(whisky) {
    const infoDiv = document.getElementById('whisky-info');
    const loadingDiv = infoDiv.querySelector('.loading');
    
    if (loadingDiv) {
        loadingDiv.remove();
    }
    
    // Affichage de l'image
    const imageDiv = document.querySelector('.whisky-image');
    imageDiv.innerHTML = `<img src="${whisky.image || '/static/images/placeholder.jpg'}" alt="${whisky.name}">`;
    
    // Ajout d'informations supplémentaires si disponibles
    if (whisky.description) {
        const descriptionP = document.createElement('p');
        descriptionP.classList.add('whisky-description');
        descriptionP.textContent = whisky.description;
        infoDiv.appendChild(descriptionP);
    }
}

// Fonction pour afficher le tableau des prix
function displayPriceTable(whisky) {
    const tableBody = document.querySelector('#current-prices tbody');
    tableBody.innerHTML = '';
    
    if (!whisky.prices || Object.keys(whisky.prices).length === 0) {
        tableBody.innerHTML = '<tr><td colspan="4">Aucune donnée de prix disponible</td></tr>';
        return;
    }
    
    for (const [site, data] of Object.entries(whisky.prices)) {
        const row = document.createElement('tr');
        
        // Nom du site
        const siteCell = document.createElement('td');
        siteCell.textContent = site;
        row.appendChild(siteCell);
        
        // Prix
        const priceCell = document.createElement('td');
        priceCell.textContent = data.price || 'Non disponible';
        row.appendChild(priceCell);
        
        // Disponibilité
        const availabilityCell = document.createElement('td');
        if (data.available === false) {
            availabilityCell.textContent = 'Out of stock';
            availabilityCell.classList.add('out-of-stock');
        } else if (data.available === true) {
            availabilityCell.textContent = 'En stock';
            availabilityCell.classList.add('in-stock');
        } else if (data.price === 'Non disponible') {
            availabilityCell.textContent = 'Non vendu';
        } else {
            availabilityCell.textContent = 'Statut inconnu';
        }
        row.appendChild(availabilityCell);
        
        // Lien
        const linkCell = document.createElement('td');
        if (data.url) {
            const link = document.createElement('a');
            link.href = data.url;
            link.textContent = 'Voir sur le site';
            link.target = '_blank';
            linkCell.appendChild(link);
        } else {
            linkCell.textContent = 'Lien non disponible';
        }
        row.appendChild(linkCell);
        
        tableBody.appendChild(row);
    }
}

// Fonction pour afficher l'historique des prix
function displayPriceHistory(whisky) {
    const chartDiv = document.getElementById('price-chart');
    
    if (!whisky.history || Object.keys(whisky.history).length === 0) {
        chartDiv.innerHTML = '<p>Aucune donnée historique disponible pour le moment.</p>';
        return;
    }
    
    // Note: Dans une implémentation réelle, nous utiliserions une bibliothèque comme Chart.js
    // pour créer un graphique d'évolution des prix
    chartDiv.innerHTML = '<p>Les données historiques seront affichées ici sous forme de graphique.</p>';
}

// Fonction pour afficher une erreur
function showError(message) {
    const infoDiv = document.getElementById('whisky-info');
    infoDiv.innerHTML = `<h2>Erreur</h2><p class="error">${message}</p>`;
}
