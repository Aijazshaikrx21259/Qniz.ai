// compare.js - Script pour la page de comparaison des prix de whisky

document.addEventListener('DOMContentLoaded', function() {
    // Récupération des données de tous les whiskys
    fetchAllWhiskyData();
});

// Fonction pour récupérer les données de tous les whiskys
function fetchAllWhiskyData() {
    fetch('/api/whiskies')
        .then(response => response.json())
        .then(data => {
            if (data.whiskies && data.whiskies.length > 0) {
                populateWhiskySelector(data.whiskies);
                populateSiteSelector(data.whiskies);
                setupEventListeners();
            } else {
                showError('Aucune donnée de whisky disponible pour le moment.');
            }
        })
        .catch(error => {
            console.error('Erreur lors de la récupération des données:', error);
            showError('Erreur lors du chargement des données. Veuillez réessayer plus tard.');
        });
}

// Fonction pour remplir le sélecteur de whiskys
function populateWhiskySelector(whiskies) {
    const select = document.getElementById('whisky-select');
    select.innerHTML = '';
    
    whiskies.forEach(whisky => {
        const option = document.createElement('option');
        option.value = whisky.name;
        option.textContent = whisky.name;
        select.appendChild(option);
    });
}

// Fonction pour remplir le sélecteur de sites
function populateSiteSelector(whiskies) {
    const select = document.getElementById('site-select');
    select.innerHTML = '';
    
    // Récupération de tous les sites uniques
    const sites = new Set();
    whiskies.forEach(whisky => {
        if (whisky.prices) {
            Object.keys(whisky.prices).forEach(site => sites.add(site));
        }
    });
    
    // Ajout des options pour chaque site
    sites.forEach(site => {
        const option = document.createElement('option');
        option.value = site;
        option.textContent = site;
        option.selected = true; // Par défaut, tous les sites sont sélectionnés
        select.appendChild(option);
    });
}

// Fonction pour configurer les écouteurs d'événements
function setupEventListeners() {
    const addButton = document.getElementById('add-whisky-btn');
    const whiskySelect = document.getElementById('whisky-select');
    const siteSelect = document.getElementById('site-select');
    
    // Événement pour ajouter des whiskys à la comparaison
    addButton.addEventListener('click', function() {
        const selectedWhiskys = Array.from(whiskySelect.selectedOptions).map(option => option.value);
        if (selectedWhiskys.length > 0) {
            updateComparisonTable(selectedWhiskys);
        } else {
            alert('Veuillez sélectionner au moins un whisky à comparer.');
        }
    });
    
    // Événement pour filtrer les sites
    siteSelect.addEventListener('change', function() {
        const selectedWhiskys = getSelectedWhiskysFromTable();
        if (selectedWhiskys.length > 0) {
            updateComparisonTable(selectedWhiskys);
        }
    });
}

// Fonction pour obtenir les whiskys actuellement sélectionnés dans le tableau
function getSelectedWhiskysFromTable() {
    const rows = document.querySelectorAll('#compare-table tbody tr');
    const whiskys = [];
    
    rows.forEach(row => {
        const whiskyName = row.querySelector('td:first-child').textContent;
        whiskys.push(whiskyName);
    });
    
    return whiskys;
}

// Fonction pour mettre à jour le tableau de comparaison
function updateComparisonTable(selectedWhiskys) {
    // Récupération des sites sélectionnés
    const siteSelect = document.getElementById('site-select');
    const selectedSites = Array.from(siteSelect.selectedOptions).map(option => option.value);
    
    if (selectedSites.length === 0) {
        alert('Veuillez sélectionner au moins un site pour la comparaison.');
        return;
    }
    
    // Récupération des données pour chaque whisky sélectionné
    Promise.all(selectedWhiskys.map(whisky => 
        fetch(`/api/whisky/${encodeURIComponent(whisky)}`).then(res => res.json())
    ))
    .then(whiskies => {
        displayComparisonTable(whiskies, selectedSites);
        displayComparisonChart(whiskies, selectedSites);
    })
    .catch(error => {
        console.error('Erreur lors de la récupération des données détaillées:', error);
        showError('Erreur lors du chargement des données détaillées. Veuillez réessayer plus tard.');
    });
}

// Fonction pour afficher le tableau de comparaison
function displayComparisonTable(whiskies, selectedSites) {
    const table = document.getElementById('compare-table');
    
    // Création de l'en-tête du tableau
    let headerHtml = '<tr><th>Whisky</th>';
    selectedSites.forEach(site => {
        headerHtml += `<th>${site}</th>`;
    });
    headerHtml += '</tr>';
    
    // Création des lignes du tableau
    let bodyHtml = '';
    whiskies.forEach(whisky => {
        bodyHtml += `<tr><td>${whisky.name}</td>`;
        
        selectedSites.forEach(site => {
            const priceData = whisky.prices && whisky.prices[site];
            let cellContent = 'N/A';
            
            if (priceData) {
                if (priceData.available === false) {
                    cellContent = 'Out of stock';
                } else if (priceData.price) {
                    cellContent = priceData.price;
                } else {
                    cellContent = 'Non vendu';
                }
            }
            
            bodyHtml += `<td>${cellContent}</td>`;
        });
        
        bodyHtml += '</tr>';
    });
    
    // Mise à jour du tableau
    table.innerHTML = `<thead>${headerHtml}</thead><tbody>${bodyHtml}</tbody>`;
}

// Fonction pour afficher le graphique de comparaison
function displayComparisonChart(whiskies, selectedSites) {
    const chartDiv = document.getElementById('compare-chart');
    
    // Note: Dans une implémentation réelle, nous utiliserions une bibliothèque comme Chart.js
    // pour créer un graphique de comparaison des prix
    chartDiv.innerHTML = '<p>Le graphique de comparaison sera affiché ici.</p>';
}

// Fonction pour afficher une erreur
function showError(message) {
    const compareSection = document.querySelector('.compare-section');
    const errorDiv = document.createElement('div');
    errorDiv.classList.add('error-message');
    errorDiv.textContent = message;
    
    // Suppression des erreurs précédentes
    const existingError = compareSection.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    compareSection.insertBefore(errorDiv, compareSection.firstChild.nextSibling);
}
