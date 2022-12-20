var selected = "nothing";

function enable(that) {
    if (selected != "nothing") {
        document.getElementById(selected).classList.remove('locked');
        document.getElementById(selected).classList.remove('rowlist');
    }
    that.classList.add('locked');
    that.classList.add('rowlist');
    selected = that.id;

}

function lightUp(that) {
    that.classList.add('locked');

}

function goOn() {
    window.location.href = "/web_app/student/editor/?assign=" + exh_id + "&temp=" + selected;
}
const targetElement = document.getElementById('getItems');

function createTemplateWindow(template, i, targer) {
    let div0 = document.createElement('div');
    let img0 = document.createElement('img');
    let div1 = document.createElement('div');
    let div2 = document.createElement('div');

    div0.id = template[i]['id'];
    div0.classList.add('col-xl-4');
    div0.classList.add('col-4');
    div0.classList.add('col-md-4');
    div0.setAttribute('onclick', "enable(this)");
    div0.setAttribute('onhover', "enable(this)");
    img0.classList.add('form-pics');
    img0.src = template[i]['thumbnail'];
    div0.appendChild(img0);
    div1.classList.add('text');
    div1.classList.add('fs-6');
    div1.classList.add('fw-bold');
    div1.textContent = template[i]['name'];
    div0.appendChild(div1);
    div2.classList.add('text-muted');
    div2.classList.add('fs-6');
    div2.classList.add('fw-semibold');
    div2.textContent = "Rooms: " + template[i]['rooms'];
    div0.appendChild(div2);

    targer.appendChild(div0);
}

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
        for (let i = 0; i < response['resource_obj']['templates']['length']; i++) {
            createTemplateWindow(response['resource_obj']['templates'], i, targetElement);
        }
    } else {
        console.log('error', xhr2);
    }
};
// Create and send a GET request
// The first argument is the post type (GET, POST, PUT, DELETE, etc.)
// The second argument is the endpoint URL
xhr2.open('GET', '/web_app/exhibitions/templates/fetch/all', true);
xhr2.send();