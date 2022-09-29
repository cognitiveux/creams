var map;
var lit = 0;
var artwork_selected = false;
const xy = [{
        'lat': 35.171035661326186,
        'lng': 33.359971390576905,
        'title': 'image 1',
    },
    {
        'lat': 35.171090661926186,
        'lng': 33.358951390576905,
        'title': 'image 2',
    },
    {
        'lat': 35.17280958981999,
        'lng': 33.360925496411866,
        'title': 'image 3',
    },
    {
        'lat': 35.172792049922954,
        'lng': 33.364466012311524,
        'title': 'image 4',
    },
    {
        'lat': 35.17166012752561, 
        'lng': 33.36358693072683,
        'title': 'image 5',
    },
];

function myMap() {
    var mapProp = {
        center: new google.maps.LatLng(35.17153390944222, 33.3617305422768),
        zoom: 16,
    };
    map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
    for (let i = 0; i < xy.length; i++) {
        let v = xy[i];
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(v['lat'], v['lng']),
            icon: {
                url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
            },
            title: v['title'],
        });
        marker.setMap(map);

    }
    const flightPlanCoordinates = [];
    for (let i = 0; i < xy.length; i++) {
        let points = xy[i];
        flightPlanCoordinates.push({
            'lat': points['lat'],
            'lng': points['lng'],
        })
    }
    flightPath = new google.maps.Polyline({
        path: flightPlanCoordinates,
        geodesic: true,
        strokeColor: "#EC4C6C",
        strokeOpacity: 1.0,
        strokeWeight: 2,
    });

    flightPath.setMap(map);

}