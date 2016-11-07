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

$.get('/add_pins.json', function(pins) {

    var pin, marker, html;

    for (var key in pins) {
        pin = pins[key];

        marker = new google.maps.Marker({
            position: new google.maps.LatLng(pin.capLat, pin.capLong),
            map: map,
            title: 'Pin ID: ' + pin.pinID,
            icon: "https://maps.gstatic.com/mapfiles/ms2/micons/blue-dot.png"
        });

    }
});