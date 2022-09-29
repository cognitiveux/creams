console.log("CUSTOM DASHBOARD SCRIPT - STARTED");
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
        fetchAndShowArtworks();
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


function fetchAndShowArtworks() {
    let MEDIA = 'data:image/jpeg;base64,';
    for (let i = 0; i < artworks.length; i++) {
        var div0 = document.createElement('div');
        div0.classList.add('col');
        div0.classList.add('text-center');
        div0.classList.add('mb-9');

        var a0 = document.createElement('a');
        a0.setAttribute('href', MEDIA + artworks[i]['src']);
        var img0 = document.createElement('img');
        img0.classList.add('carou-pics');
        img0.classList.add('mx-auto');
        img0.classList.add('mb-2');
        img0.classList.add('d-flex');
        img0.classList.add('bgi-no-repeat');
        img0.classList.add('bgi-size-contain');
        img0.classList.add('bgi-position-center');
        if (i === 0)
            img0.classList.add('thumbnail');


        img0.setAttribute('src', MEDIA + artworks[i]['src']);

        a0.appendChild(img0);
        div0.appendChild(a0);

        var div1 = document.createElement('div');
        div1.classList.add('mb-0');

        var div2 = document.createElement('div');
        div2.classList.add('text-muted');
        div2.classList.add('fs-6');
        div2.classList.add('fw-semibold');
        div2.textContent = artworks[i]['name'];

        div1.appendChild(div2);
        div0.appendChild(div1);

        document.getElementById('artwork_carousel').appendChild(div0);

    }
}

console.log("CUSTOM DASHBOARD SCRIPT - DONE");