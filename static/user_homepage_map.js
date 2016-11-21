"use strict";
// NB: Used snippets of Google Maps/Places Autocomplete demo

var $;
var google;
var marker;
var markers = {};
var map;
var pin;
var editMap = {
    "1": "Wish List",
    "2": "Going Back",
    "3": "Never Going Back"
};
var pinIcons = {
    1: 'http://maps.google.com/mapfiles/ms/micons/green.png',
    2: 'http://maps.google.com/mapfiles/ms/micons/blue.png',
    3: 'http://maps.google.com/mapfiles/ms/micons/red.png'
};

function getSecondValue(value) {
    return value === 1 ? "2" : "1";
}

function getSecondOption(pinTypeId) {
    return pinTypeId === 1 ? editMap["2"] : editMap["1"];
}

function getThirdValue(value) {
    return value === 3 ? "2" : "3";
}

function getThirdOption(pinTypeId) {
    return pinTypeId === 3 ? editMap["2"] : editMap["3"];
}

function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 0, lng: 0},
        zoom: 2
    });
    var infoWindow = new google.maps.InfoWindow({
        width: 350,
        height: 200
    });
    var options = {
        types: ['(cities)']
    };
    var input = document.getElementById('pac-input');
    var autocomplete = new google.maps.places.Autocomplete(input, options);

    function addPinToMap(pin) {
        var LatLng = new google.maps.LatLng(pin.latitude, pin.longitude);
        marker = new google.maps.Marker({
            position: LatLng,
            map: map,
            icon: pinIcons[pin.pinTypeId]
        });

        console.log("value of pin.pinId", pin.pinId);
        console.log("value of pin.pinTypeId", pin.pinTypeId);
        console.log("value of getSecondValue", getSecondValue(pin.pinTypeId));
        console.log("value of getSecondOption", getSecondOption(pin.pinTypeId));
        console.log("value of getThirdValue", getThirdValue(pin.pinTypeId));
        console.log("value of getThirdOption", getThirdOption(pin.pinTypeId));
        //console.log("value of pin. ", );

        markers[LatLng] = marker;
        
        var html = (
            '<div class = "window-content">' +
            '<h1 id="place-name" class="place-name">' + pin.city +
            '</h1>' +
            '<div class="window-body">' +
            '<form action="#" method="post">' +
            // Add this at some point.'Notes:<input type="text" name="notes"' + 
            // 'maxlength="500" size="100"/> <br/>' +
            'Update Your Pin:<br/>' +
            '<select name="pin_types">' +
            '<option value=' + pin.pinTypeId + '>' +
            editMap[pin.pinTypeId] + '</option>' +
            '<option value=' + getSecondValue(pin.pinTypeId) + '>' +
            getSecondOption(pin.pinTypeId) + '</option>' +
            '<option value=' + getThirdValue(pin.pinTypeId) + '>' +
            getThirdOption(pin.pinTypeId) + '</option>' +
            '</select><br/>' +
            '<input type="hidden" name="pin_id" value=' + pin.pinId + '>' +
            '<input type="hidden" name="city" value=' + pin.city + '>' +
            '<p><input class="submit-edit" type="submit"></p>' +
            '</form>' +
            '</div>' +
            '</div>' +
            '<button data-remove=' + pin.pinId +
            ' type="button"' +
            'class="btn btn-default remove" name="remove-pin">' +
            'Remove Pin</button>'
        );

        bindInfoWindow(marker, map, infoWindow, html);

        return marker;
    }

    function bindInfoWindow(marker, map, infoWindow, html) {
        google.maps.event.addListener(marker, 'click', function () {
            infoWindow.close();
            infoWindow.setContent(html);
            infoWindow.open(map, marker);

            $(".submit-edit").on('click', editPin);
            $(".remove").on('click', removePin);
        });
    }

    function editPin(evt){
        // Add some Jasmine error handling: check that names match
        evt.preventDefault();

        var form = $('form').serializeArray();
        var params = {'editPinTypeId': form[0]["value"],
                      'editPinId': form[1]["value"],
                      'editPinCity': form[2]["value"]
                    };

        console.log("These are the params", params);

        $.post('/edit_pin.json', params, refreshMap);
    }

    function refreshMap(results){
        console.log(results);

        var pin = {
            "latitude": parseFloat(results.lat),
            "longitude": parseFloat(results.lng),
            "pinTypeId": parseInt(results.pin_type),
            "pinId": parseInt(results.pin_id),
            "city": String(results.city)
        }

        removePinFromMap(results);
        addPinToMap(pin);
    }

    function removePin(evt){
        var data = {'id': $(this).data("remove")};

        $.post('/remove_pin.json', data, removePinFromMap);
    }

    function removePinFromMap(results) {
        console.log(results);
        
        var lat = parseFloat(results.lat);
        console.log(lat);
        var lng = parseFloat(results.lng);
        console.log(lng);

        markers[new google.maps.LatLng(lat, lng)].setMap(null);
    }

    // Make the callback a named function
    google.maps.event.addListener(autocomplete, 'place_changed', function() {

        $('#submit').click(function(evt){
            evt.preventDefault();
            $("#pac-input").val("");

            var place = autocomplete.getPlace();
            var pinType = $("input[name=pin_type]:checked").val();

            pin = {
                "latitude": place.geometry.location.lat(),
                "longitude": place.geometry.location.lng(),
                "pinTypeId": pinType
            };

            console.log(place.address_components);

            for (var i = 0; i < place.address_components.length; i++) {
                var placeObject = place.address_components[i]["types"][0];
                var longName = place.address_components[i].long_name;

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
        
            $.post("/user_homepage", pin, function(results) {
                if (results !== "None") {
                    pin.pinId = results;
                }
                addPinToMap(pin, results);
            });

        });
    });    

    $.get('/user_pin_info.json', {user_id: userId}, function (pins) {
        for (var key in pins) {
            var pin = pins[key];
            addPinToMap(pin);
        }
    });   
}


