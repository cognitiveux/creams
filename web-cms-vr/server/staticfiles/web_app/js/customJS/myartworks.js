function gotoAddArtwork() {
    window.location.href = "/web_app/submit_artwork/";
}
const first_row = document.getElementById('first_row');
const second_row = document.getElementById('kt_followers_show_more_cards');

function addArtworkCards() {
    let tar = first_row;
    var xhr1 = new XMLHttpRequest();
    // Setup our listener to process completed requests
    xhr1.onreadystatechange = function () {
        // Only run if the request is complete
        if (xhr1.readyState !== 4) return;
        // Process our return data
        if (xhr1.status >= 200 && xhr1.status < 300) {
            // What to do when the request is successful
            var response = JSON.parse(xhr1.responseText);
            for (let i = 0; i < response['resource_obj']['artworks']['length']; i++) {
                if (i > 2)
                    tar = second_row;
                createCards(response['resource_obj']['artworks'], i, tar);
            }
            console.log(response);
        } else {
            console.log('error', xhr1);
        }
    };
    // Create and send a GET request
    // The first argument is the post type (GET, POST, PUT, DELETE, etc.)
    // The second argument is the endpoint URL
    xhr1.open('GET', '/web_app/artworks/student_list', true);
    xhr1.send();

}

function createCards(artworks, i, target) {
    let MEDIA = '/media/';
    let div0 = document.createElement('div');
    div0.classList.add('col-md-6');
    div0.classList.add('col-xxl-4');

    let div1 = document.createElement('div');
    div1.classList.add('card');

    let div2 = document.createElement('div');
    div2.classList.add('card-body');
    div2.classList.add('d-flex');
    div2.classList.add('flex-center');
    div2.classList.add('flex-column');
    div2.classList.add('py-9');
    div2.classList.add('px-5');

    div1.appendChild(div2);

    let div3 = document.createElement('div');
    div3.classList.add('mb-5');
    div3.classList.add('carou-pics-holder');

    let img0 = document.createElement('img');
    img0.classList.add('carou-pics');
    img0.src = MEDIA + artworks[i]['src'];
    img0.alt = artworks[i]['id'];

    div3.appendChild(img0);

    let a0 = document.createElement('a');
    a0.href = MEDIA + artworks[i]['src'];
    a0.classList.add('fs-4');
    a0.classList.add('text-gray-800');
    a0.classList.add('fw-bold');
    a0.classList.add('mb-0');
    a0.classList.add('text-hover-primary');
    a0.setAttribute('target',"_blank");
    a0.textContent = artworks[i]['name'];

    div2.appendChild(div3);
    div2.appendChild(a0);
    div1.appendChild(div2);
    div0.appendChild(div1);

    target.appendChild(div0);
}

addArtworkCards();

