function callAndAddExhibitions() {
    var xhr1 = new XMLHttpRequest();
    // Setup our listener to process completed requests
    xhr1.onreadystatechange = function () {
        // Only run if the request is complete
        if (xhr1.readyState !== 4)
            return;
        // Process our return data
        if (xhr1.status >= 200 && xhr1.status < 300) {
            // What to do when the request is successful
            var response = JSON.parse(xhr1.responseText);
            if (response['resource_obj']['exhibitions'].length == 0) {
                document.getElementById('exh_page').classList.add('hidden');
                document.getElementById('error_filtering').classList.remove('hidden');
            }
            for (i = 0; i < response['resource_obj']['exhibitions'].length; i++) {
                addExhibitions(response['resource_obj']['exhibitions'], i);
            }
            console.log(response);
        } else {
            console.log('error', xhr1);
            document.getElementById('exh_page').classList.add('hidden');
            document.getElementById('error_filtering').classList.remove('hidden');
        }
    };
    // Create and send a GET request
    // The first argument is the post type (GET, POST, PUT, DELETE, etc.)
    // The second argument is the endpoint URL
    xhr1.open('GET', '/web_app/assignment/filter?status=' + filter, true);
    xhr1.send();
}

function addExhibitions(exhibition, i) {
    let div0 = document.createElement('div');
    div0.classList.add('col');
    div0.classList.add('text-center');
    div0.classList.add('mb-9');
    let a0 = document.createElement('a');
    a0.href = "/web_app/teacher/student_assessment/?q=" + exhibition[i]['id'];
    let img0 = document.createElement('img');
    img0.alt = "exh" + exhibition[i]['id'];
    img0.classList.add('carou-pics');
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

    let div3 = document.createElement('div');
    div3.classList.add('text-muted');
    div3.classList.add('fs-6');
    div3.classList.add('fw-semibold');
    div3.textContent = 'Start Date: ' + exhibition[i]['start_date'];

    let div4 = document.createElement('div');
    div4.classList.add('text-muted');
    div4.classList.add('fs-6');
    div4.classList.add('fw-semibold');
    div4.textContent = 'End Date: ' + exhibition[i]['end_date'];

    let div5 = document.createElement('div');
    div5.classList.add('text-muted');
    div5.classList.add('fs-6');
    div5.classList.add('fw-semibold');
    div5.classList.add(decodeStatus(exhibition[i]['status']));
    div5.textContent = exhibition[i]['status'];

    let div6 = document.createElement('div');
    div6.classList.add('text-muted');
    div6.classList.add('fs-6');
    div6.classList.add('fw-semibold');
    div6.textContent = "Number of participants: " + exhibition[i]['participants'];

    div1.appendChild(div2);
    div1.appendChild(div3);
    div1.appendChild(div4);
    div1.appendChild(div5);
    div1.appendChild(div6);

    div0.appendChild(div1);

    document.getElementById('exh_page').appendChild(div0);
}

callAndAddExhibitions();

function decodeStatus(status) {
    if (status === "Temporary Stored")
        return "redText";
    if (status === "Published")
        return "greenText";
    if (status === "Accepting Artworks")
        return "orangeText";
    if (status === "Ready to be Assessed")
        return "yellowText";
    if (status === "Assessed")
        return "blueText";
    if (status === "Assessment Started")
        return "cyanText";

}