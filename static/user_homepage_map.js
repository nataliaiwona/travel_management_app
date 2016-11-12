"use strict";
// NB: Used snippets of Google Maps/Places Autocomplete demo

function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 0, lng: 0},
        zoom: 2
    });

    function addPinToMap(pin) {
        return new google.maps.Marker({
            position: new google.maps.LatLng(pin.latitude, pin.longitude),
            map: map,
            icon: pinIcons[pin.pinTypeId]
        });
    }

    // Initializing input variable by selecting the pac-input box.
    var input = document.getElementById('pac-input');

    // Initializing types variable by selecting the type-selector div,
    // which includes pin radio buttons. 
    var types = document.getElementById('type-selector');

    // Setting options variable to restrict the autocomplete search 
    // to cities only.
    var options = {
        types: ['(cities)']
    };

    // Instantiating autocomplete object, including input and options vars
    var autocomplete = new google.maps.places.Autocomplete(input, options);


    // $("#submit").on("click", function () {
    //     console.log("before");
    //     $("#pac-input").val("");
    //     console.log("after");
    // });

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
          
            for (var i = 0; i < place.address_components.length; i++) {
            
                if (place.address_components[i]["types"][0] == "locality") {
                    pin["city"] = place.address_components[i].long_name;
                }

                if (place.address_components[i]["types"][0] == "administrative_area_level_1") {
                    pin["state"] = place.address_components[i].long_name;
                }

                if (place.address_components[i]["types"][0] == "country") {
                    pin["country"] = place.address_components[i].long_name;
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

    $.get('/user_pin_info.json', function (pins) {
        for (var key in pins) {
            var pin =  pins[key];
            addPinToMap(pin);
        }
    });


}

