async function openGraphModal(indicatorId) {
    values = await getIndicatorValues(indicatorId);
    if (values.length === 0) {
        showToast("Erreur", "Aucune donnée disponible pour cet indicateur.");
        return;
    }

    // Trier les valeurs par date
    values.sort((a, b) => new Date(a.date) - new Date(b.date));

    // Créer une chronologie complète avec interpolation pour les gaps
    function createCompleteTimeline(values) {
        if (values.length === 0) return { labels: [], dataPoints: [] };
        
        const timelineData = [];
        const startDate = new Date(values[0].date);
        const endDate = new Date(values[values.length - 1].date);
        
        // Déterminer l'intervalle optimal basé sur la durée totale
        const totalDuration = endDate - startDate;
        let intervalMs;
        
        if (totalDuration <= 3600000) { // <= 1 heure
            intervalMs = 60000; // 1 minute
        } else if (totalDuration <= 86400000) { // <= 1 jour
            intervalMs = 600000; // 10 minutes
        } else if (totalDuration <= 604800000) { // <= 1 semaine
            intervalMs = 3600000; // 1 heure
        } else {
            intervalMs = 86400000; // 1 jour
        }
        
        // Créer les points de données avec interpolation
        let currentTime = new Date(Math.floor(startDate.getTime() / intervalMs) * intervalMs);
        let valueIndex = 0;
        
        while (currentTime <= endDate) {
            // Trouver la valeur la plus proche pour ce timestamp
            let closestValue = 0;
            let minDistance = Infinity;
            
            for (let i = 0; i < values.length; i++) {
                const valueTime = new Date(values[i].date);
                const distance = Math.abs(valueTime - currentTime);
                
                // Si on trouve une valeur dans un intervalle raisonnable (2x l'intervalle)
                if (distance < intervalMs * 2 && distance < minDistance) {
                    minDistance = distance;
                    closestValue = values[i].value;
                }
            }
            
            timelineData.push({
                timestamp: new Date(currentTime),
                value: closestValue
            });
            
            currentTime = new Date(currentTime.getTime() + intervalMs);
        }
        
        return timelineData;
    }

    // Créer la chronologie complète
    const timelineData = createCompleteTimeline(values);

    // Préparer les données pour Chart.js avec échelle temporelle
    const chartData = timelineData.map(item => ({
        x: item.timestamp,
        y: item.value
    }));

    // Créer le graphique avec Chart.js
    const modalBody = document.getElementById('modalGraphBody');
    modalBody.innerHTML = '<canvas id="indicatorChart" style="width: 100%; height: 200px;"></canvas>';
    const ctx = document.getElementById('indicatorChart').getContext('2d');

    new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Valeurs de l\'indicateur',
                data: chartData,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
                tension: 0.1,
                pointRadius: 3,
                pointHoverRadius: 5
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        tooltipFormat: 'dd/MM/yyyy HH:mm:ss',
                        displayFormats: {
                            minute: 'HH:mm',
                            hour: 'dd/MM HH:mm',
                            day: 'dd/MM',
                            week: 'dd/MM',
                            month: 'MMM yyyy'
                        }
                    },
                    display: true,
                    title: {
                        display: true,
                        text: 'Temps'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Valeur'
                    },
                    beginAtZero: true
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        title: function(context) {
                            return new Date(context[0].parsed.x).toLocaleDateString('fr-FR') + ' ' + 
                                    new Date(context[0].parsed.x).toLocaleTimeString('fr-FR', {hour12: false});
                        }
                    }
                }
            }
        }
    });

    // Afficher le modal
    const graphModal = new bootstrap.Modal(document.getElementById('modalGraphique'));
    graphModal.show();
}