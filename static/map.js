var locations = null
var marker, i;
var heatmap;
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
      for (i = 0; i < locations.length; i++) {
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

  })
  return false
});
