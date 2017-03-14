var locations = null
var marker, tweet;
var heatmap;
var markerSet = new Array();
var infowindow = new google.maps.InfoWindow();
var map = new google.maps.Map(document.getElementById('map'), {
  zoom: 3,
  center: new google.maps.LatLng(40.8, -73.96),
  mapTypeId: google.maps.MapTypeId.ROADMAP
});


$('button').on('click',function(){
  $.ajax({
    type: 'POST',
    url: '/keyword' ,
    data:
    {
      "tags": $("#tags option:selected").val()
    },
    dataType: 'json',
    success: function(data) {
      console.log('Keyword! Backend to Frontend!');
      locations = data.locs
      console.log(locations)

      var heatmapData = []
      for (var i = 0; i < locations.length; i++) {
        var latLng = new google.maps.LatLng(locations[i][0], locations[i][1])
        heatmapData.push(latLng);
      //marker = new google.maps.Marker({
      //  position: latLng,
      //  map: map
      //});
      }
      if (heatmap) {
        heatmap.setMap(null)
      }
      if (marker) {
        marker.setMap(null)
      }
      if (markerSet) {
        if (markerSet.length > 0) {
          for (var i = 0; i < markerSet.length; i++) {
            markerSet[i].setMap(null)
          }
        }
      }
      heatmap = new google.maps.visualization.HeatmapLayer({
        data: heatmapData,
        dissipating: false,
        map: map
      });
    },
    error: function(xhr, type) {
      console.log('Error!')
    }
  })
})

//event.preventDefault();

google.maps.event.addListener(map, 'click', function(event) {
  if (heatmap) {
    heatmap.setMap(null)
  }
  if (markerSet) {
    if (markerSet.length > 0) {
      for (var i = 0; i < markerSet.length; i++) {
        markerSet[i].setMap(null)
      }
    }
  }
  var lat = event.latLng.lat();
  var lng = event.latLng.lng();
  if (marker) {
    marker.setMap(null);
  }
  marker = new google.maps.Marker({
    position: {lat: lat, lng: lng},
    map: map
  })

  $.getJSON('/local', {
    lat: lat,
    lng: lng
  }, function(data) {
    console.log("Click! Backend to Frontend!")
    locations = data.locs
    console.log(locations)

    var image = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png';
    for (var i = 0; i < locations.length; i++) {
      var latLng = new google.maps.LatLng(locations[i][0], locations[i][1])
      tweet = new google.maps.Marker({
        position: latLng,
        map: map,
        icon: image
      })
      markerSet.push(tweet)
    }
  })
  return false
});
