"use strict";
// NB: Used snippets of Google Maps/Places Autocomplete demo


var marker;
var markers = {};
var map;
var pin;

function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 0, lng: 0},
        zoom: 2
    });

    function addPinToMap(pin) {
        var LatLng = new google.maps.LatLng(pin.latitude, pin.longitude);
        
        marker = new google.maps.Marker({
            position: LatLng,
            map: map,
            icon: pinIcons[pin.pinTypeId]
        });

        markers[LatLng] = marker;

        var html = (
            '<div class = "window-content">' +
            '<h1 id="place-name" class="place-name">' + pin.city +
            '</h1>' +
            '<div class="window-body">' +
            '<div class="dropdown open">' +
            '<button data-edit=' + pin.pinId +
            ' type="button" class="btn btn-secondary dropdown-toggle edit"' +
            'name="edit-pin" id="dropdownMenu2" data-toggle="dropdown"' +
            'aria-haspopup="true" aria-expanded="false">Edit Pin</button>' +
            '<div class="dropdown-menu" aria-labelledby="dropdownMenu2">' +
            '<button class="dropdown-item" type="button"' + 
            'name="pin_type" id="pin_type_1" value="1">Wish List</button>' +
            '<button class="dropdown-item" type="button"' +
            'name="pin_type" id="pin_type_2" value="2">Going back!</button>' +
            '<button class="dropdown-item" type="button"' + 
            'name="pin_type" id="pin_type_3" value="3">Never Going Back</button>' +
            '</div>' +
            '</div>' +
            '<button data-remove=' + pin.pinId +
            ' type="button"' +
            'class="btn btn-default remove" name="remove-pin">Remove Pin</button>' +
            '<label>Notes:' +
            '<textarea id ="note" name="note" rows="5" cols="50"></textarea>' +
            '</label>' +
            '</div>' +
            '</div>');

        bindInfoWindow(marker, map, infoWindow, html);

        return marker;
    }

    // Make an autocomplete function
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
      width: 350,
      height: 200
    });

    // Make the callback a named function
    google.maps.event.addListener(autocomplete, 'place_changed', function() {

        // jQuery to bind an event handler to the click event
        $('#submit').click(function(evt){
            evt.preventDefault();
            $("#pac-input").val("");

            // Initialize address as empty string and place object.
            // Check to see if certain address components exist in the place object
            var place = autocomplete.getPlace();
            var pinType = $("input[name=pin_type]:checked").val();

            pin = {
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
    
    // Put outside
    var pinIcons = {
        1: 'http://maps.google.com/mapfiles/ms/micons/blue.png',
        2: 'http://maps.google.com/mapfiles/ms/micons/green.png',
        3: 'http://maps.google.com/mapfiles/ms/micons/red.png'
    };

    $.get('/user_pin_info.json', {user_id: userId}, function (pins) {
        for (var key in pins) {
            var pin = pins[key];
            addPinToMap(pin);
        }
    });

    function refreshMap(results) {
        console.log(results);
        
        var lat = parseFloat(results.lat);
        console.log(lat);
        var lng = parseFloat(results.lng);
        console.log(lng);

        markers[new google.maps.LatLng(lat, lng)].setMap(null);
        console.log("Done with refreshMap");
    }

    function editPin(evt){
        $.post('/edit_pin.json', pin, {'id': $(this).data("edit")}, function(){
            addPinToMap(pin);
        });
    }

    function removePin(evt){
  
        $.post('/remove_pin.json', {'id': $(this).data("remove")}, refreshMap);
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
    google.maps.event.addDomListener(window, 'load', initMap);
}


