var map;
var lit = 0;
var artwork_selected = false;
var xy = [];


function getCenter() {
    let sumx = 0,
        sumy = 0;
    for (let i = 0; i < xy.length; i++) {
        sumx += xy[i]['lat'];
        sumy += xy[i]['lng'];
    }
    return {
        'lat': sumx / xy.length,
        'lng': sumy / xy.length
    };
}

function calculateDistance(lat1, lon1, lat2, lon2) {
    // The math module contains a function
    // named toRadians which converts from
    // degrees to radians.
    lon1 = lon1 * Math.PI / 180;
    lon2 = lon2 * Math.PI / 180;
    lat1 = lat1 * Math.PI / 180;
    lat2 = lat2 * Math.PI / 180;

    // Haversine formula
    let dlon = lon2 - lon1;
    let dlat = lat2 - lat1;
    let a = Math.pow(Math.sin(dlat / 2), 2) +
        Math.cos(lat1) * Math.cos(lat2) *
        Math.pow(Math.sin(dlon / 2), 2);

    let c = 2 * Math.asin(Math.sqrt(a));

    // Radius of earth in kilometers. Use 3956
    // for miles
    let r = 6371;

    // calculate the result
    return (c * r);
}

function addImageToGrid(image, i) {
    let MEDIA = "/media/";
    let a0 = document.createElement('a');
    let img0 = document.createElement('img');
    img0.classList.add('w-100');
    img0.classList.add('shadow-1-strong');
    img0.classList.add('rounded');
    img0.classList.add('mb-4');
    img0.src = MEDIA + image[i]['src'];
    img0.id = image[i]['id'];
    a0.appendChild(img0);
    document.getElementById('imagegrid').appendChild(a0);
}

function calculateZoom() {
    let max = 0;
    let center = getCenter();
    for (let i = 0; i < xy.length - 1; i++) {
        let other = xy[i + 1];
        let temp = calculateDistance(other['lat'], other['lng'], xy[i]['lat'], xy[i]['lng']);
        if (temp >= max)
            max = temp;
    }
    if (max > 1000)
        return 2;
    if (max > 200)
        return 5;
    if (max > 100)
        return 7;
    if (max > 10)
        return 9;
    if (max >= 5)
        return 14;
    if (max < 5)
        return 15;
}


function myMap2() {

    let directionsService = new google.maps.DirectionsService();
    let directionsRenderer = new google.maps.DirectionsRenderer();
    let temp = getCenter();
    var mapProp = {
        center: new google.maps.LatLng(temp['lat'], temp['lng']),
        zoom: calculateZoom(),
    };
    map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
    var start = new google.maps.LatLng(xy[0]['lat'], xy[0]['lng']);
    var len = xy.length - 1;
    var end = new google.maps.LatLng(xy[len]['lat'], xy[len]['lng']);
    var listXY = []
    for (let i = 1; i < len; i++) {
        let point = xy[i];
        listXY.push({
            location: new google.maps.LatLng(point['lat'], point['lng']),
            stopover: true,
        })
    }
    // PoC2
    //calcRoute(start, end, listXY, directionsService, directionsRenderer);

}
var directionsService;
var directionsRenderer;
xy = [];

function myMap() {
    var xhr1 = new XMLHttpRequest();
    // Setup our listener to process completed requests
    xhr1.onreadystatechange = function () {
        // Only run if the request is complete
        if (xhr1.readyState !== 4) return;
        // Process our return data
        if (xhr1.status >= 200 && xhr1.status < 300) {
            // What to do when the request is successful
            var response = JSON.parse(xhr1.responseText);
            console.log(response);
            document.getElementById('title_field').textContent = response['resource_obj']['title'];
            document.getElementById('owner_name_field').textContent = "by " + response['resource_obj']['owner_name'];
            for (let i = 0; i < response['resource_obj']['artworks'].length; i++) {
                let val = response['resource_obj']['artworks'][i];
                xy.push({
                    'lat': val['lat'],
                    'lng': val['lon'],
                    'title': val['name']
                });

                //PoC2
                addImageToGrid(response['resource_obj']['artworks'], i);
            }
            directionsService = new google.maps.DirectionsService();
            directionsRenderer = new google.maps.DirectionsRenderer();
            let temp = getCenter();
            var mapOptions = {
                center: new google.maps.LatLng(temp['lat'], temp['lng']),
                zoom: calculateZoom(),
            };
            map = new google.maps.Map(document.getElementById('map'), mapOptions);
            directionsRenderer.setMap(map);

            var start = new google.maps.LatLng(xy[0]['lat'], xy[0]['lng']);
            var len = xy.length - 1;
            var end = new google.maps.LatLng(xy[len]['lat'], xy[len]['lng']);
            var listXY = []
            //PoC2
            var listAll = []
            for (let i = 0; i < len + 1; i++) {
                let point = xy[i];
                listAll.push({
                    x: point['lat'],
                    y: point['lng'],
                })
            }
            for (let i = 1; i < len; i++) {
                let point = xy[i];
                listXY.push({
                    location: new google.maps.LatLng(point['lat'], point['lng']),
                    stopover: true,
                })
            }
            //PoC2
            //calcRoute(start, end, listXY);
            addPoints(listAll, map)

            //var script = document.createElement('script');
            //script.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyAYt547YY2r22dJMgJF9iq6otztcfsCGUY&callback=myMap";
            //console.log("ADD GOOGLE API");
            //document.head.appendChild(script);

        } else {
            console.log('error', xhr1);
        }
    };
    // Create and send a GET request
    // The first argument is the post type (GET, POST, PUT, DELETE, etc.)
    // The second argument is the endpoint URL
    xhr1.open('GET', '/web_app/exhibitions/outdoor/details?outdoor-exhibition-id=' + exh_id, false);
    xhr1.send();


}

function addPoints(list, map) {
    for (let i = 0; i < list.length; i++) {
        console.log(list[i])
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(list[i]['x'], list[i]['y']),
            draggable: false,
            icon: {
                url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
            },
            //PoC2
            //title: ACTIVE_ARTWORK_NAME,
            id: i,
        });
        lit++;

        marker.setMap(map);
    }
}

function calcRoute(start, end, passList) {
    console.log(start);
    console.log(end);
    console.log(passList);
    var request = {
        origin: start,
        destination: end,
        waypoints: passList,
        travelMode: 'WALKING',
    };
    directionsService.route(request, function (result, status) {
        if (status == 'OK') {
            directionsRenderer.setDirections(result);
        }
    });
}