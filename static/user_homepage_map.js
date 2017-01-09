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
    value = parseInt(value);
    return value === 1 ? "2" : "1";
}

function getSecondOption(pinTypeId) {
    pinTypeId = parseInt(pinTypeId);
    return pinTypeId === 1 ? editMap["2"] : editMap["1"];
}

function getThirdValue(value) {
    value = parseInt(value);
    return value === 3 ? "2" : "3";
}

function getThirdOption(pinTypeId) {
    return pinTypeId === 3 ? editMap["2"] : editMap["3"];
}

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 33.997324, lng: -6.894970},
        zoom: 2,
        styles: [
            {
                "featureType": "administrative",
                "elementType": "labels.text.fill",
                "stylers": [{"color": "#444444"}]
            },
            {
                "featureType": "landscape",
                "elementType": "all",
                "stylers": [{"color": "#f2f2f2"}]
            },
            {
                "featureType": "poi",
                "elementType": "all",
                "stylers": [{"visibility": "off"}]
            },
            {
                "featureType": "road",
                "elementType": "all",
                "stylers": [{"saturation": -100},
                            {"lightness": 45}]
            },
            {
                "featureType": "road.highway",
                "elementType": "all",
                "stylers": [{"visibility": "simplified"}]
            },
            {
                "featureType": "road.arterial",
                "elementType": "labels.icon",
                "stylers": [{"visibility": "off"}]
            },
            {   
                "featureType": "transit",
                "elementType": "all",
                "stylers": [{"visibility": "off"}]
            },
            {   
                "featureType": "water",
                "elementType": "all",
                "stylers": [{"color": "#46bcec"},
                            {"visibility": "on"}]
            }
        ]
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

        markers[LatLng] = marker;

        var html = (
            '<div class = "window-content">' +
            '<h3 id="place-name" class="place-name">' + pin.city +
            '</h3>' +
            '<div class="window-body">' +
            '<form action="#" method="post">' +
            // Add this at some point.'Notes:<input type="text" name="notes"' + 
            // 'maxlength="500" size="100"/> <br/>' +
            '<h5 id="edit-pin">EDIT PIN</h5>' +
            '<select name="pin_types" class="form-control selectpicker">' +
            '<option value=' + pin.pinTypeId + '>' +
            editMap[pin.pinTypeId] + '</option>' +
            '<option value=' + getSecondValue(pin.pinTypeId) + '>' +
            getSecondOption(pin.pinTypeId) + '</option>' +
            '<option value=' + getThirdValue(pin.pinTypeId) + '>' +
            getThirdOption(pin.pinTypeId) + '</option>' +
            '</select><br/>' +
            '<input type="hidden" name="pin_id" value=' + pin.pinId + '>' +
            '<input type="hidden" name="city" value=' + pin.city + '>' +
            '<input class="btn btn-primary btn-sm submit-edit" type="submit">' +
            '<button data-remove=' + pin.pinId +
            ' type="button"' +
            'class="btn btn-danger btn-sm remove" name="remove-pin">' +
            'Remove Pin</button>' +
            '</form>' +
            '</div>' +
            '</div>'  
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
        evt.preventDefault();

        var form = $('form').serializeArray();
        var params = {'editPinTypeId': form[0]["value"],
                      'editPinId': form[1]["value"],
                      'editPinCity': form[2]["value"]
                    };

        $.post('/edit_pin.json', params, refreshMap);
    }

    function refreshMap(results){
        var pin = {
            "latitude": parseFloat(results.lat),
            "longitude": parseFloat(results.lng),
            "pinTypeId": parseInt(results.pin_type),
            "pinId": parseInt(results.pin_id),
            "city": String(results.city)
        };

        removePinFromMap(results);
        addPinToMap(pin);
    }

    function removePin(evt){
        var data = {'id': $(this).data("remove")};
        $.post('/remove_pin.json', data, removePinFromMap);
    }

    function removePinFromMap(results) {
        var lat = parseFloat(results.lat);
        var lng = parseFloat(results.lng);

        markers[new google.maps.LatLng(lat, lng)].setMap(null);
    }

    google.maps.event.addListener(autocomplete, 'place_changed', function() {

        $("#submit").unbind("click");

        $('#submit').click(function(evt){
            evt.preventDefault();
            $("#pac-input").val("");
            $(".alert-dismissable").removeAttr("style");
            $(".alert-dismissable").removeClass("hidden").delay(2000).fadeOut();

            var place = autocomplete.getPlace();
            var pinType = $("input[name=pin_type]:checked").val();

            pin = {
                "latitude": place.geometry.location.lat(),
                "longitude": place.geometry.location.lng(),
                "pinTypeId": pinType
            };

            console.log("place.address_components", place.address_components);

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
        
            $.post("/user_homepage", pin, function(result) {
                if (result) {
                    pin.pinId = result.new_pin_id;
                }
                addPinToMap(pin);
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

$(document).ready(function() {
    $('select').addClass('selectpicker');
});
