console.log("CUSTOM DASHBOARD SCRIPT - STARTED");

var xhr2 = new XMLHttpRequest();
// Setup our listener to process completed requests
xhr2.onreadystatechange = function () {
    // Only run if the request is complete
    if (xhr2.readyState !== 4) return;
    // Process our return data
    if (xhr2.status >= 200 && xhr2.status < 300) {
        // What to do when the request is successful
        var response = JSON.parse(xhr2.responseText);
        for (let i = 0; i < response['resource_obj']['exhibitions']['length']; i++) {
            addExhibitions(response['resource_obj']['exhibitions'], i);
        }
        console.log(response);
    } else {
        console.log('error', xhr2);
    }
};
// Create and send a GET request
// The first argument is the post type (GET, POST, PUT, DELETE, etc.)
// The second argument is the endpoint URL
xhr2.open('GET', '/web_app/assignment/get_list/student', false);
xhr2.send();

function addExhibitions(exhibition, i) {
    let div0 = document.createElement('div');
    div0.classList.add('col');
    div0.classList.add('text-center');
    div0.classList.add('mb-9');

    let a0 = document.createElement('a');
    a0.href = "#";
    let img0 = document.createElement('img');
    img0.alt = "exh" + exhibition[i]['id'];
    img0.classList.add('mx-auto');
    img0.classList.add('mb-2');
    img0.classList.add('d-flex');
    img0.classList.add('bgi-no-repeat');
    img0.classList.add('bgi-size-contain');
    img0.classList.add('bgi-position-center');
    img0.classList.add('carou-pics');
    img0.src = '/media/' + exhibition[i]['thumbnail'];

    a0.appendChild(img0);
    div0.appendChild(a0);

    let div1 = document.createElement('div');
    div1.classList.add('mb-0');

    let div2 = document.createElement('div');
    div2.classList.add('text');
    div2.classList.add('fs-6');
    div2.classList.add('fw-semibold');
    div2.textContent = exhibition[i]['title'];

    let div4 = document.createElement('div');
    div4.classList.add('text-muted');
    div4.classList.add('fs-6');
    div4.classList.add('fw-semibold');
    div4.textContent = exhibition[i]['start_date'] + ' - ' + exhibition[i]['end_date'];

    let div5 = document.createElement('div');
    div5.classList.add('text-muted');
    div5.classList.add('fs-6');
    div5.classList.add('fw-semibold');
    div5.textContent = 'assigned by ' + exhibition[i]['instructor'];

    let btn_a0 = document.createElement('a');
    btn_a0.classList.add('btn');
    btn_a0.classList.add('btn-primary');
    btn_a0.classList.add('btn-sm');
    btn_a0.classList.add('flex-shrink-0');
    btn_a0.classList.add('me-3');
    btn_a0.href='/web_app/student/template_selection/?assign=' +  exhibition[i]['id'];
    btn_a0.textContent = "Indoor";

    let btn_a1 = document.createElement('a');
    btn_a1.classList.add('btn');
    btn_a1.classList.add('btn-warning');
    btn_a1.classList.add('btn-sm');
    btn_a1.classList.add('flex-shrink-0');
    btn_a1.classList.add('me-3');
    btn_a1.href='/web_app/create_ar/?assign=' +  exhibition[i]['id'];
    btn_a1.textContent = "Outdoor";

    div1.appendChild(div2);
    div1.appendChild(div5);
    div1.appendChild(div4);
    div1.appendChild(btn_a0);
    div1.appendChild(btn_a1);

    div0.appendChild(div1);

    document.getElementById('exhibition_carousel').appendChild(div0);
}
console.log("CUSTOM DASHBOARD SCRIPT - DONE");