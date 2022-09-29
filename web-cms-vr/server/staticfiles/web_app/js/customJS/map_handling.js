var map;
var points = [];
var lit = 0;
var artwork_selected = false;
let lat = 35.14478368257859;
let long = 33.410500801214475;
var ACTIVE_ARTWORK_ID = -1;
var ACTIVE_ARTWORK_NAME = '';

function myMap() {
    navigator.geolocation.getCurrentPosition((position) => {
        lat = position.coords.latitude;
        long = position.coords.longitude;
    });
    var mapProp = {
        center: new google.maps.LatLng(lat, long),
        zoom: 15,
    };
    map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
    map.addListener("click", function (e) {
        if (artwork_selected) {
            artwork_selected = false;
            document.getElementById(ACTIVE_ARTWORK_ID).classList.remove('locked');
            ACTIVE_DESCRIPTION = document.getElementById('textArea').value;
            document.getElementById('textArea').value = '';
            var marker = new google.maps.Marker({
                position: new google.maps.LatLng(e.latLng),
                draggable: true,
                icon: {
                    url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
                },
                title: ACTIVE_ARTWORK_NAME,
                id: ACTIVE_ARTWORK_ID,
                descr: ACTIVE_DESCRIPTION,
            });
            lit++;

            marker.setMap(map);
            points.push(marker);
            marker.addListener("dblclick", function () {
                let temp = [];
                for (let i = 0; i < points.length; i++) {
                    if (points[i].id === marker.id) {
                        continue;
                    } else {
                        temp.push(points[i]);
                    }
                }

                points = [];
                marker.setMap(null);
                for (let i = 0; i < temp.length; i++) {
                    points.push(temp[i]);
                }
            });
        }
    });
}

function getPoints() {
    for (let i = 0; i < points.length; i++)
        console.log(points[i].position.lat() + ' , ' + points[i].position.lng() + ' ' + points[i].id + ' ' + points[i].title + ' ' + points[i].descr);
}

function fillScrollableWithAssets() {
    let MEDIA = 'data:image/jpeg;base64,';
    var xhr1 = new XMLHttpRequest();
    var artworks = [];
    // Setup our listener to process completed requests
    xhr1.onreadystatechange = function () {
        // Only run if the request is complete
        if (xhr1.readyState !== 4) return;
        // Process our return data
        if (xhr1.status >= 200 && xhr1.status < 300) {
            // What to do when the request is successful
            var response = JSON.parse(xhr1.responseText);
            for (let i = 0; i < response['resource_obj']['artworks']['length']; i++) {
                artworks[i] = response['resource_obj']['artworks'][i];
            }
            var len = artworks.length;
            for (let i = 0; i < len; i++) {
                var as = artworks[i];
                var div0 = document.createElement('div');
                div0.classList.add('mh-375px', 'scroll-y', 'me-n7', 'pe-7');
                var div1 = document.createElement('div');
                div1.classList.add('border', 'border-hover-primary', 'p-7', 'rounded', 'mb-7');
                div1.setAttribute('id', as.id);
                var div2 = document.createElement('div');
                div2.classList.add('d-flex', 'flex-stack', 'pb-3');
                var div3 = document.createElement('div');
                div3.classList.add('d-flex');
                var div4 = document.createElement('div');
                div4.classList.add('symbol', 'symbol-150px');

                var am1 = document.createElement('a');
                //am1.classList.add('d-block', 'overlay', 'h-100');
                //am1.setAttribute('data-fslightbox', 'lightbox-hot-sales');
                //am1.setAttribute('href', MEDIA + as.src);
                var img0 = document.createElement('img');
                img0.setAttribute('id', 'as' + i);
                img0.setAttribute('src', MEDIA + as.src);
                img0.setAttribute('height', '100px');
                img0.setAttribute('width', '200px');
                am1.appendChild(img0);

                //var divm1 = document.createElement('div');
                //divm1.classList.add('overlay-layer', 'card-rounded', 'bg-dark', 'bg-opacity-25');
                //var i0 = document.createElement('i');
                //i0.classList.add('bi', 'bi-eye-fill', 'fs-2x', 'text-white');
                //divm1.appendChild(i0);
                //am1.appendChild(divm1);

                div4.appendChild(am1);
                var div5 = document.createElement('div');
                div5.classList.add('ms-5');

                var div6 = document.createElement('div');
                div6.classList.add('d-flex', 'align-items-center');
                var p0 = document.createElement('p');
                p0.classList.add('text-dark', 'fw-bold', 'text-hover-primary', 'fs-5', 'me-4');
                p0.textContent = as['name'];
                div6.appendChild(p0);

                var span0 = document.createElement('span');
                span0.classList.add('text-muted', 'fw-semibold', 'mb-3');
                span0.textContent = as['year'];
                div5.appendChild(div6);
                div5.appendChild(span0);

                div3.appendChild(div4);
                div3.appendChild(div5);
                div2.appendChild(div3);
                div1.appendChild(div2);

                var div7 = document.createElement('div');
                div7.classList.add('p-0');
                var div8 = document.createElement('div');
                div8.classList.add('d-flex', 'flex-column');

                var p1 = document.createElement('p');
                p1.classList.add('text-gray-700', 'fw-semibold', 'fs-6', 'mb-4');
                //p1.textContent = as.getAttribute('descr');
                div8.appendChild(p1);

                var a0 = document.createElement('a');
                a0.classList.add('btn', 'btn-sm', 'btn-primary');
                a0.setAttribute('param1', as.id);
                a0.setAttribute('param2', as.name);
                a0.setAttribute('onclick', 'enable(this)');
                a0.textContent = 'Select';
                div8.appendChild(a0);
                div7.appendChild(div8);

                div1.appendChild(div7);
                div0.appendChild(div1);
                document.getElementById('artworks').appendChild(div0);
            }
            console.log(response);
        } else {
            console.log('error', xhr1);
        }
    };
    // Create and send a GET request
    // The first argument is the post type (GET, POST, PUT, DELETE, etc.)
    // The second argument is the endpoint URL
    xhr1.open('GET', '/web_app/artworks/student_list', false);
    xhr1.send();



}
fillScrollableWithAssets();


function enable(clickedElement) {
    if ($('#' + ACTIVE_ARTWORK_ID).length)
        document.getElementById(ACTIVE_ARTWORK_ID).classList.remove('locked');
    ACTIVE_ARTWORK_ID = clickedElement.getAttribute('param1');
    ACTIVE_ARTWORK_NAME = clickedElement.getAttribute('param2');
    let hov = document.getElementById(ACTIVE_ARTWORK_ID);
    hov.classList.add('locked');
    artwork_selected = true;
}

function submitOutdoor() {
    for (let i = 0; i < points.length; i++) {
        let lat = points[i].position.lat();
        let lon = points[i].position.lng();
        let id = points[i].id;
        let descr = points[i].descr;
        let exh = 1;

        var data = new FormData();
        data.append("lat", "" + lat);
        data.append("lon", "" + lon);
        data.append("description", "" + descr);
        data.append("artwork_fk", "" + id);
        data.append("exhibition_fk", "" + exh);

        var xhr = new XMLHttpRequest();
        xhr.withCredentials = true;
        xhr.addEventListener("readystatechange", function () {
            if (this.readyState === 4) {
                console.log(this.responseText);
            }
        });
        xhr.open("POST", "/web_app/exhibitions/outdoor/submit_artwork", true);
        xhr.send(data);
    }
    window.location.replace("/web_app/student/dashboard/");

}