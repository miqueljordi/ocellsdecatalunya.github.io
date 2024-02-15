function loadMap() {
    var speciesSelect = document.getElementById("species");
    var species = speciesSelect.value;
    var startDate = document.getElementById("start-date").value;
    var endDate = document.getElementById("end-date").value;
    var url = "/map?species=" + encodeURIComponent(species) + "&start_date=" + encodeURIComponent(startDate) + "&end_date=" + encodeURIComponent(endDate);
    
    var mapContainer = document.getElementById("map-container");
    mapContainer.innerHTML = "<iframe src='" + url + "' width='800' height='600'></iframe>";
}
