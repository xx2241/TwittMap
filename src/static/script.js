// Reference - http://stackoverflow.com/questions/27721671/call-a-flask-function-every-few-minutes
// https://developers.google.com/maps/documentation/javascript/markers

var plotter;
var map;

function initMap(locs) {
    plotter = new google.maps.Geocoder();
    var markers = locs;
    plotPoints(markers);
    map = new google.maps.Map(document.getElementById('map'));
}

function plotPoints(markers) {
        for (i=0; i<markers; i++)
        {
            coordinates = markers[i];
            plotter.geocode( { 'address': coordinates}, function(queryresults, status) {
              if (status == google.maps.GeocoderStatus.OK) {
                var marker = new google.maps.Marker({
                    map: map,
                    position: queryresults[0].geometry.location
                });
                  marker.addListener('click', toggleBounce);
              }
            });
        }
    }
function toggleBounce() {
    if (marker.getAnimation() !== null) {
         marker.setAnimation(null);
    }
    else {
    marker.setAnimation(google.maps.Animation.BOUNCE);
    }
}
