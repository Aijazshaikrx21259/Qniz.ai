// main.js - Script pour la page d'accueil

document.addEventListener('DOMContentLoaded', function() {
    // Récupération des données des whiskys
    fetchWhiskyData();
    
    // Configuration de la recherche
    setupSearch();
});

// Fonction pour récupérer les données des whiskys
function fetchWhiskyData() {
    fetch('/api/whiskies')
        .then(response => response.json())
        .then(data => {
            displayWhiskyGrid(data.whiskies);
            updateLastUpdated(data.last_updated);
        })
        .catch(error => {
            console.error('Erreur lors de la récupération des données:', error);
            document.getElementById('whisky-grid').innerHTML = 
                '<p class="error">Erreur lors du chargement des données. Veuillez réessayer plus tard.</p>';
        });
}

// Fonction pour afficher la grille de whiskys
function displayWhiskyGrid(whiskies) {
    const grid = document.getElementById('whisky-grid');
    
    if (!whiskies || whiskies.length === 0) {
        grid.innerHTML = '<p>Aucune donnée de whisky disponible pour le moment.</p>';
        return;
    }
    
    let html = '';
    
    whiskies.forEach(whisky => {
        // Calcul du prix minimum et maximum
        let prices = [];
        if (whisky.prices) {
            Object.values(whisky.prices).forEach(sitePrice => {
                if (sitePrice && sitePrice.price && sitePrice.price !== "Non disponible") {
                    prices.push(parseFloat(sitePrice.price.replace('€', '').trim()));
                }
            });
        }
        
        const minPrice = prices.length > 0 ? Math.min(...prices) : null;
        const maxPrice = prices.length > 0 ? Math.max(...prices) : null;
        
        let priceRange = 'Prix non disponible';
        if (minPrice !== null && maxPrice !== null) {
            if (minPrice === maxPrice) {
                priceRange = `${minPrice.toFixed(2)} €`;
            } else {
                priceRange = `${minPrice.toFixed(2)} € - ${maxPrice.toFixed(2)} €`;
            }
        }
        
        // Création de la carte pour chaque whisky
        html += `
            <div class="whisky-card" data-name="${whisky.name.toLowerCase()}">
                <img src="${whisky.image || '/static/images/placeholder.jpg'}" alt="${whisky.name}">
                <div class="whisky-card-content">
                    <h3>${whisky.name}</h3>
                    <p class="price-range">${priceRange}</p>
                    <a href="/whisky/${encodeURIComponent(whisky.name)}" class="view-btn">Voir les détails</a>
                </div>
            </div>
        `;
    });
    
    grid.innerHTML = html;
}

// Fonction pour mettre à jour la date de dernière mise à jour
function updateLastUpdated(lastUpdated) {
    const introSection = document.querySelector('.intro');
    if (lastUpdated) {
        const dateElement = document.createElement('p');
        dateElement.classList.add('last-updated');
        dateElement.textContent = `Dernière mise à jour: ${lastUpdated}`;
        introSection.appendChild(dateElement);
    }
}

// Fonction pour configurer la recherche
function setupSearch() {
    const searchInput = document.getElementById('search-input');
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase().trim();
        const cards = document.querySelectorAll('.whisky-card');
        
        cards.forEach(card => {
            const name = card.dataset.name;
            if (name.includes(searchTerm)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}
