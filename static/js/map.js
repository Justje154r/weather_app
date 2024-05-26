function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 0, lng: 0},
        zoom: 2
    });

    // Пример маркера
    var marker = new google.maps.Marker({
        position: {lat: 0, lng: 0},
        map: map,
        title: 'Weather Location'
    });
}