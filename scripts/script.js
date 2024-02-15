document.addEventListener('DOMContentLoaded', function () {
    // Initialize the map
    var map = L.map('map').setView([0, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    // Function to create markers on the map
    function createMarkers(data) {
        // Iterate over data and add markers
        data.forEach(function (observation) {
            L.marker([observation.LATITUDE, observation.LONGITUDE])
                .bindPopup(`<strong>${observation['COMMON NAME']}</strong><br>Locality: ${observation.LOCALITY}<br>Date: ${observation['OBSERVATION DATE']}`)
                .addTo(map);
        });
    }

    // Sample data (replace with your JSON data)
    var sampleData = [
        { "COMMON NAME": "Alpine Accentor", "LATITUDE": 42.2960142, "LONGITUDE": 2.1402958, "LOCALITY": "Campelles—Poble", "OBSERVATION DATE": "2023-01-29" },
        { "COMMON NAME": "Alpine Accentor", "LATITUDE": 42.0213619, "LONGITUDE": 2.5360498, "LOCALITY": "El Far--Mirador", "OBSERVATION DATE": "2023-01-18" }
    ];

    // Create markers using sample data
    createMarkers(sampleData);
});