const INDOOR = "Indoor";
const OUTDOOR = "Outdoor";

function showCarousel(exhibitions, i, target, TYPE) {
    let MEDIA = '/media/';
    var div0 = document.createElement('div');
    div0.classList.add('col');
    div0.classList.add('text-center');
    div0.classList.add('mb-9');
    var a0 = document.createElement('a');
    if (TYPE === INDOOR) {
        a0.setAttribute('href', '/web_app/visitor/vr_display/?assign=' + exhibitions[i]['id']);
    } else if (TYPE === OUTDOOR) {
        a0.setAttribute('href', '/web_app/visitor/ar_display/?assign=' + exhibitions[i]['id']);
    }
    a0.setAttribute('target', "_blank");
    var img0 = document.createElement('img');
    img0.classList.add('landingpageimages');
    img0.classList.add('mx-auto');
    img0.classList.add('mb-2');
    img0.classList.add('d-flex');
    img0.classList.add('bgi-no-repeat');
    img0.classList.add('bgi-size-contain');
    img0.classList.add('bgi-position-center');
    img0.setAttribute('src', MEDIA + exhibitions[i]['thumbnail']);

    a0.appendChild(img0);
    div0.appendChild(a0);

    var div1 = document.createElement('div');
    div1.classList.add('mb-0');

    var div2 = document.createElement('div');
    div2.classList.add('text-muted');
    div2.classList.add('fs-6');
    div2.classList.add('fw-semibold');
    div2.textContent = "Student: " + exhibitions[i]['owner_name'];

    var div3 = document.createElement('div');
    div3.classList.add('text');
    div3.classList.add('fs-6');
    div3.classList.add('fw-bold');
    div3.textContent = exhibitions[i]['title'];

    var div5 = document.createElement('div');
    div5.classList.add('text');
    div5.classList.add('fs-6');
    div5.classList.add('fw-bold');
    div5.classList.add(decodeColours(TYPE));
    div5.textContent = "Type: " + TYPE;

    var div4 = document.createElement('div');
    div4.classList.add('text-muted');
    div4.classList.add('fs-6');
    div4.classList.add('fw-semibold');
    div4.textContent = exhibitions[i]['start_date'] + " to " + exhibitions[i]['end_date'];

    div1.appendChild(div3);
    div1.appendChild(div2);
    div1.appendChild(div5);
    div1.appendChild(div4);
    div0.appendChild(div1);

    target.appendChild(div0);


}

function decodeColours(TYPE) {
    if (TYPE === INDOOR)
        return "greenText";
    else if (TYPE === OUTDOOR)
        return "cyanText";
}

let AR_MR = document.getElementById('ARMR');
var xhr2 = new XMLHttpRequest();
// Setup our listener to process completed requests
xhr2.onreadystatechange = function () {
    // Only run if the request is complete
    if (xhr2.readyState !== 4) return;
    // Process our return data
    if (xhr2.status >= 200 && xhr2.status < 300) {
        // What to do when the request is successful
        var response = JSON.parse(xhr2.responseText);
        console.log(response);
        for (let i = 0; i < response['resource_obj']['exhibitions']['length']; i++) {
            showCarousel(response['resource_obj']['exhibitions'], i, AR_MR, OUTDOOR);
        }
    } else {
        console.log('error', xhr2);
    }
};
// Create and send a GET request
// The first argument is the post type (GET, POST, PUT, DELETE, etc.)
// The second argument is the endpoint URL
xhr2.open('GET', '/web_app/exhibitions/outdoor/all', false);
xhr2.send();

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
        for (let i = 0; i < response['resource_obj']['exhibitions']['length']; i++) {
            showCarousel(response['resource_obj']['exhibitions'], i, VR, INDOOR);
        }
    } else {
        console.log('error', xhr1);
    }
};
// Create and send a GET request
// The first argument is the post type (GET, POST, PUT, DELETE, etc.)
// The second argument is the endpoint URL
xhr1.open('GET', '/web_app/exhibitions/indoor/all', false);
xhr1.send();