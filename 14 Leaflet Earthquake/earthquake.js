// Parse dealer location csv using d3
d3.json('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson', function(data){

    // Get all 8 options ready
    var emerald = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "mapbox.emerald",
        accessToken: API_KEY
    });

    var pirates = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "mapbox.pirates",
        accessToken: API_KEY
    });

    var streetsSatellite = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "mapbox.streets-satellite",
        accessToken: API_KEY
    });

    var dark = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "mapbox.dark",
        accessToken: API_KEY
    });

    var outdoors = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "mapbox.outdoors",
        accessToken: API_KEY
    });

    var light = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "mapbox.light",
        accessToken: API_KEY
    });

    var runBikeHike = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "mapbox.run-bike-hike",
        accessToken: API_KEY
    });

    var streets = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "mapbox.streets",
        accessToken: API_KEY
    });

    var myMap = L.map("map", {
        center: [42.877742, -97.380979],
        zoom: 4,
        layers: [dark]
    });

    // 8 choices: dark, light, pirates, streets, emerald, outdoors, run-bike-hike, streets-satellite
    var baseMaps = {
        Dark: dark,
        Light: light,
        Pirates: pirates,
        Streets: streets,
        Emerald: emerald,
        Outdoors: outdoors,
        'Run Bike Hike': runBikeHike,
        'Streets Satellite': streetsSatellite  
    };

    var overlayMarkers = [];

    for (var i = 0; i < data.features.length; i++) {
        var magnitude = +data.features[i].properties.mag;
        // Get color based on magnitude 
        function getColor(d) {
            return d < 1 ? '#feebe2' :
              d < 2 ?  '#fcc5c0':
              d < 3 ? '#fa9fb5' :
              d < 4 ? '#f768a1' : 
              d < 5 ? '#c51b8a' :
              '#7a0177';
        };
        // Get radius
        var radius = (Math.exp(magnitude/1.01-0.08))*1000;
        // Push data to empty overlayMarkers list
        overlayMarkers.push(L.circle([data.features[i].geometry.coordinates[1], data.features[i].geometry.coordinates[0]], {
            color: 'black',
            weight: .1,
            fillColor: getColor(magnitude),
            fillOpacity: .8,
            radius: radius
        }).bindPopup(`<b>Place: ${data.features[i].properties.place}</b><br><b>Magnitude: ${String(magnitude)}</b>`));
    };

    var overlayLayer = L.layerGroup(overlayMarkers);

    var overlayMaps = {'Earthquake Markers': overlayLayer};

    // Add custom legend on bottom right
    var legend = L.control({position: 'bottomright'});

    legend.onAdd = function (map) {
    
        var div = L.DomUtil.create('div', 'info legend'),
            grades = [0, 1, 2, 3, 4, 5];
            var labels = [];
        // loop through our density intervals and generate a label with a colored square for each interval
        for (var i = 0; i < grades.length; i++) {
            labels +=
                '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
                grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
        }
        div.innerHTML = '<strong> Earthquake<br> Magnitude </strong><br>' + labels;
        return div;
    };

    // Put control on legend
    myMap.on('overlayadd', function (eventLayer) {
        // Turn legend on when overlay is clicked
        if (eventLayer.name === 'Earthquake Markers') {
            legend.addTo(this);
        }
    });
    myMap.on('overlayremove', function (eventLayer) {
        // Turn legend off when overlay is removed
        this.removeControl(legend);
    });

    // Add Control
    L.control.layers(baseMaps, overlayMaps).addTo(myMap);
}); 



