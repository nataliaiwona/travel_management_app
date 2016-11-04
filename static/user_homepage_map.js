function initMap() {
    var myLatLng = {lat: 72, lng: -140};
}

var map = new google.maps.Map(document.getElementById('map'), {
    center: myLatLng,
    scrollwheel: false,
    zoom: 5, 
    zoomControl: true,
    panControl: false,
    streetViewControl: false,
    // styles: default,
    // mapTypeId: default
});

