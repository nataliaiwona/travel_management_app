"use strict";
// NB: Used snippets of Google Maps/Places Autocomplete demo


var marker; 

function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 0, lng: 0},
        zoom: 2
    });

    function addPinToMap(pin) {
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(pin.latitude, pin.longitude),
            map: map,
            icon: pinIcons[pin.pinTypeId]
        });
        return marker;
    }

    // Initializing input variable by selecting the pac-input box.
    // Can't make this jquery bc the instantiating autocomplete can't be jquery
    var input = document.getElementById('pac-input');

    // Initializing types variable by selecting the type-selector div,
    // which includes pin radio buttons. 
    // var types = document.getElementById('type-selector');

    // Setting options variable to restrict the autocomplete search 
    // to cities only.
    var options = {
        types: ['(cities)']
    };

    // Instantiating autocomplete object, including input and options vars
    var autocomplete = new google.maps.places.Autocomplete(input, options);

    var infoWindow = new google.maps.InfoWindow({
      width: 150
    });

    google.maps.event.addListener(autocomplete, 'place_changed', function() {

        // jQuery to bind an event handler to the click event
        $('#submit').click(function(evt){
            evt.preventDefault();
            $("#pac-input").val("");

            // Initialize address as empty string and place object.
            // Check to see if certain address components exist in the place object
            var place = autocomplete.getPlace();
            var pinType = $("input[name=pin_type]:checked").val();

            var pin = {
                "latitude": place.geometry.location.lat(),
                "longitude": place.geometry.location.lng(),
                "pinTypeId": pinType
            };
            // TODO add switch statement
            console.log(place.address_components);

            for (var i = 0; i < place.address_components.length; i++) {
                var placeObject = place.address_components[i]["types"][0];
                var longName = place.address_components[i].long_name;
// TODO add comments
                if (placeObject == "locality") {
                    pin["city"] = longName;
                } else if (placeObject == "administrative_area_level_1") {
                    pin["state"] = longName;
                } else if (placeObject == "country") {
                    pin["country"] = longName;
                } else {
                    pin["city"] = place.name;
                }
            }
        
            $.post("/user_homepage",
                pin, function() {
                addPinToMap(pin);
            });

        });
    });
    
    var pinIcons = {
        1: 'http://maps.google.com/mapfiles/ms/micons/blue.png',
        2: 'http://maps.google.com/mapfiles/ms/micons/green.png',
        3: 'http://maps.google.com/mapfiles/ms/micons/red.png'
    };

    $.get('/user_pin_info.json', {user_id: userId}, function (pins) {
        for (var key in pins) {
            var pin = pins[key];
            addPinToMap(pin);

            var html = (
                '<div class = "window-content">' +
                '<h1 id="place-name" class="place-name">' + pin.city +
                '</h1>' +
                '<div class="window-body">' +
                '<button id="edit_' + pin.pinId + 
                '" type="button" class="btn btn-default edit"' +
                'name="edit-pin">Edit Pin</button>' +
                '<button id="remove_' + pin.pinId +
                '" type="button"' +
                'class="btn btn-default remove" name="remove-pin">Remove Pin</button>' +
                '<label>Notes:' +
                '<textarea id ="note" name="note" rows="5" cols="30"></textarea>' +
                '</label>' +
                '</div>' +
                '</div>');

            bindInfoWindow(marker, map, infoWindow, html);
        }
    });

    function editPin (evt){
        $.post('/edit_pin.json');
    }

    function removePin (evt){
        $.post('/remove_pin.json', {'id': this.id});
    }

    function bindInfoWindow(marker, map, infoWindow, html) {
        google.maps.event.addListener(marker, 'click', function () {
            infoWindow.close();
            infoWindow.setContent(html);
            infoWindow.open(map, marker);

            $(".edit").on('click', editPin);
            $(".remove").on('click', removePin);
        });

    }

}

// google.maps.event.addDomListener(window, 'load', initMap);
