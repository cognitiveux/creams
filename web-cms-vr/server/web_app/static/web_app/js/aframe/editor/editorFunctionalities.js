console.log("EDITOR FUNCTIONALITIES - START");
var ACTIVE_ELEMENT = 'empty';
var TYPE = 'none';

function changeArtwork(box_id, artwork_id) {
    var box = document.getElementById(box_id);
    //console.log(artwork_id);
    box.setAttribute('material', 'src:#' + artwork_id);
    updateDOM();
}

function changeArtworkByBox(box, artwork_id) {
    //** there should be some code to add the artwork to assets */
    box.setAttribute('material', 'src:#' + artwork_id);
    updateDOM();
}

function insertArtwork(artwork) {
    let nname = "User";
    var asset = document.createElement('img');
    asset.setAttribute('id', artwork['id']);
    asset.setAttribute('src', '/media/' + artwork['src']);
    asset.setAttribute('type', "artwork");
    asset.setAttribute('name', artwork['name']);
    asset.setAttribute('data-height', artwork['height']);
    asset.setAttribute('data-width', artwork['width']);
    asset.setAttribute('creator', nname + " " + surname);
    asset.setAttribute('descr', artwork['technique'] + ' ' + artwork['genre']);

    var assetlist = document.getElementsByTagName('a-assets')[0];
    assetlist.appendChild(asset);
}

function insertAsset(type, id, src) {
    var asset = document.createElement('img');
    asset.setAttribute('id', id);
    asset.setAttribute('src', src);
    asset.setAttribute('type', type);

    var assetlist = document.getElementsByTagName('a-assets')[0];
    assetlist.appendChild(asset);
}

// insertAsset("texture", "gray0", "/static/web_app/media/picassoExhibition/Textures/gray_0.png");
// insertAsset("texture", "gray1", "/static/web_app/media/picassoExhibition/Textures/gray_1.png");
// insertAsset("texture", "gray2", "/static/web_app/media/picassoExhibition/Textures/gray_2.png");
// insertAsset("texture", "gray3", "/static/web_app/media/picassoExhibition/Textures/gray_3.png");
// insertAsset("texture", "gray4", "/static/web_app/media/picassoExhibition/Textures/gray_4.png");
// insertAsset("texture", "lev", "/static/web_app/media/picassoExhibition/Textures/levander.png");
// insertAsset("texture", "red", "/static/web_app/media/picassoExhibition/Textures/red.png");
insertAsset("texture", "wood", "/static/web_app/media/picassoExhibition/Textures/wood.jpeg");
insertAsset("texture", "wood2", "/static/web_app/media/picassoExhibition/Textures/wood2.jpeg");
insertAsset("texture", "rock", "/static/web_app/media/picassoExhibition/Textures/rock.jpeg");
insertAsset("texture", "rock2", "/static/web_app/media/picassoExhibition/Textures/rock2.jpeg");
insertAsset("texture", "brick", "/static/web_app/media/picassoExhibition/Textures/brick.jpg");
insertAsset("texture", "brick2", "/static/web_app/media/picassoExhibition/Textures/brick2.jpeg");
insertAsset("texture", "grass", "/static/web_app/media/picassoExhibition/Textures/grass.jpg");
insertAsset("texture", "grass2", "/static/web_app/media/picassoExhibition/Textures/grass2.jpg");
insertAsset("texture", "sky", "/static/web_app/media/picassoExhibition/Textures/sky.jpeg");


function setMe(clickedElement) {
    //console.log(clickedElement);
    insertAsset('img', 'demo', clickedElement.getAttribute('src'))
    changeArtwork('face', 'demo');
    changeSizeOfBox('face', 8, 4, 0.05);
}

function fetchAssets() {
    var assets = document.getElementsByTagName("a-assets")[0];
    var len = assets.children.length;
    for (let i = 0; i < len; i++) {
        var as = assets.children[i];
    }

}

function assignArtworkOrTexture(clickedElement) {
    changeArtwork(ACTIVE_ELEMENT, clickedElement.getAttribute('param1'));
    document.getElementById('x').value = clickedElement.getAttribute('param2');
    document.getElementById('y').value = clickedElement.getAttribute('param3');
    changeSizeOfBox(ACTIVE_ELEMENT, clickedElement.getAttribute('param2') / 100, clickedElement.getAttribute('param3') / 100, 0.05);
    updateDOM();
}

function scaleUp() {
    let active = document.getElementById(ACTIVE_ELEMENT);
    if (TYPE === 'box') {
        document.getElementById('x').value = active.getAttribute('scale').x * 100 * 2;
        document.getElementById('y').value = active.getAttribute('scale').y * 100 * 2;
    } else if (TYPE === 'label') {
        console.log("UP");
        document.getElementById('x').value = active.getAttribute('text').width * 100 * 2;
        document.getElementById('y').value = active.getAttribute('text').height * 100 *2;
    }
    handleSizeChange();

}

function scaleDown() {
    let active = document.getElementById(ACTIVE_ELEMENT);
    if (TYPE === 'box') {
        document.getElementById('x').value = active.getAttribute('scale').x * 100 * 0.5;
        document.getElementById('y').value = active.getAttribute('scale').y * 100 * 0.5;
    } else if (TYPE === 'label') {
        console.log("DOWN");
        document.getElementById('x').value = active.getAttribute('text').width * 100 * 0.5;
        document.getElementById('y').value = active.getAttribute('text').height * 100 * 0.5;
    }
    handleSizeChange();

}

function fillScrollableWithAssets() {
    var assets = document.getElementsByTagName("a-assets")[0];
    var len = assets.children.length;
    for (let i = 0; i < len; i++) {
        var as = assets.children[i];
        if (as['attributes']['type']['value'] === 'artwork' || as['attributes']['type']['value'] === 'texture') {
            var div0 = document.createElement('div');
            div0.classList.add('mh-375px', 'scroll-y', 'me-n7', 'pe-7');
            var div1 = document.createElement('div');
            div1.classList.add('border', 'border-hover-primary', 'p-7', 'rounded', 'mb-7');
            var div2 = document.createElement('div');
            div2.classList.add('d-flex', 'flex-stack', 'pb-3');
            var div3 = document.createElement('div');
            div3.classList.add('d-flex');
            var div4 = document.createElement('div');
            div4.classList.add('symbol', 'symbol-150px');

            var am1 = document.createElement('a');
            am1.classList.add('d-block', 'overlay', 'h-100');
            am1.setAttribute('data-fslightbox', 'lightbox-hot-sales');
            am1.setAttribute('href', as.src);

            var div_extra = document.createElement('div');
            div_extra.classList.add('overlay-wrapper');
            div_extra.classList.add('bgi-no-repeat');
            div_extra.classList.add('bgi-position-center');
            div_extra.classList.add('bgi-size-cover');
            div_extra.classList.add('card-rounded');
            div_extra.classList.add('min-h-200px');
            div_extra.classList.add('h-100');

            var img0 = document.createElement('img');
            img0.classList.add('carou-pics');
            img0.setAttribute('id', 'as' + i);
            img0.setAttribute('src', as.src);

            div_extra.appendChild(img0);
            am1.appendChild(div_extra);

            var divm1 = document.createElement('div');
            divm1.classList.add('overlay-layer', 'card-rounded', 'bg-dark', 'bg-opacity-25');
            var i0 = document.createElement('i');
            i0.classList.add('bi', 'bi-eye-fill', 'fs-2x', 'text-white');
            divm1.appendChild(i0);
            am1.appendChild(divm1);

            div4.appendChild(am1);
            var div5 = document.createElement('div');
            div5.classList.add('ms-5');

            var div6 = document.createElement('div');
            div6.classList.add('d-flex', 'align-items-center');
            var p0 = document.createElement('p');
            p0.classList.add('text-dark', 'fw-bold', 'text-hover-primary', 'fs-5', 'me-4');
            p0.textContent = as.getAttribute('name');
            div6.appendChild(p0);

            var span0 = document.createElement('span');
            span0.classList.add('text-muted', 'fw-semibold', 'mb-3');
            span0.textContent = as.getAttribute('creator');
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
            p1.textContent = as.getAttribute('descr');
            div8.appendChild(p1);

            var a0 = document.createElement('a');
            a0.classList.add('btn', 'btn-sm', 'btn-primary');
            a0.setAttribute('param1', as.id);
            a0.setAttribute('param2', as.getAttribute('data-width'));
            a0.setAttribute('param3', as.getAttribute('data-height'));
            a0.setAttribute('onclick', 'assignArtworkOrTexture(this)');
            a0.textContent = 'Select';
            div8.appendChild(a0);
            div7.appendChild(div8);

            div1.appendChild(div7);

            div0.appendChild(div1);

            if (as.getAttribute('type') === 'artwork' && img0.src !== '') {
                document.getElementById('kt_table_widget_5_tab_3').appendChild(div0);
            } else if (as.getAttribute('type') === 'texture' && img0.id !== 'as24') {
                //console.log(img0);
                document.getElementById('kt_table_widget_5_tab_2').appendChild(div0);
            }
        }
    }

}


function handleSizeChange() {
    var x = document.getElementById('x').value / 100;
    var y = document.getElementById('y').value / 100;
    var z = 0.05;

    changeSizeOfBox(ACTIVE_ELEMENT, x, y, z);
    updateDOM();

}

function changeText() {
    document.getElementById("text_alteration").value = "";
    document.getElementById(ACTIVE_ELEMENT).setAttribute('text', {
        color: document.getElementById('html5colorpicker').value,
        value: document.getElementById('new_label').value
    });
    updateDOM();
}

if (getArtworksFlag === '0') {
    var xhr3 = new XMLHttpRequest();
    // Setup our listener to process completed requests
    xhr3.onreadystatechange = function () {
        // Only run if the request is complete
        if (xhr3.readyState !== 4) return;
        // Process our return data
        if (xhr3.status >= 200 && xhr3.status < 300) {
            // What to do when the request is successful
            var response = JSON.parse(xhr3.responseText)['resource_obj']['artworks'];
            for (let i = 0; i < response.length; i++)
                insertArtwork(response[i]);

        } else {
            console.log('error', xhr3);
        }
    };
    // Create and send a GET request
    // The first argument is the post type (GET, POST, PUT, DELETE, etc.)
    // The second argument is the endpoint URL
    xhr3.open('GET', '/web_app/artworks/student_list', false);
    xhr3.send();
}

fillScrollableWithAssets();

function saveExhibit() {
    let exh = document.getElementsByTagName('a-scene')[0].cloneNode(true);
    exh.getElementsByTagName('canvas')[0].remove();
    toastr.options = {
        "closeButton": false,
        "debug": false,
        "newestOnTop": false,
        "progressBar": false,
        "positionClass": "toastr-top-right",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    };
    let falseCameras = exh.getElementsByTagName('a-entity');
    let toBeDeletedIds = [];
    for (let i = 0; i < falseCameras.length; i++)
        if (falseCameras[i].getAttribute('camera') !== null)
            toBeDeletedIds.push(i);
    for (let i = 0; i < toBeDeletedIds.length; i++) {
        falseCameras[i].remove();
    }
    exh = exh.outerHTML;

    var xhr = new XMLHttpRequest();
    xhr.addEventListener("readystatechange", function () {
        // Only run if the request is complete
        if (xhr.readyState !== 4) return;
        // Process our return data
        if (xhr.status >= 200 && xhr.status < 300) {
            var response = JSON.parse(xhr.responseText);
            toastr.success("Exhibition saved!");
        } else {
            toastr.error("Something went wrong!");
        }
    });

    xhr.open("POST", "/web_app/exhibitions/indoor/create/vr", true);
    /*INSERT DATA*/
    let formData = new FormData(); // creates an object, optionally fill from <form>
    formData.append("vr_exhibition ", new Blob([exh], {
        type: "text/plain"
    }), "" + user_id + "_" + exh_id + ".txt");
    formData.append("vr_script ", new Blob([getNewScript(items)], {
        type: "text/plain"
    }), "" + user_id + "_" + exh_id + ".js");


    formData.append("exhibition_fk", exh_id); // appends a field
    xhr.send(formData);

}

function addLight() {
    var light = document.createElement("a-light");
    light.setAttribute('type', 'spot');
    light.setAttribute('color', '#FFF');
    light.setAttribute('target', '#' + ACTIVE_ELEMENT);
    light.setAttribute('id', 'zzz');
    document.getElementsByTagName('a-scene')[0].appendChild(light);
}


function play() {
    geometry = "primitive: plane; height: auto; width: auto"
    var sa = document.getElementById(ACTIVE_ELEMENT);
    sa.setAttribute('geometry', {
        primitive: plane,
        height: auto,
        width: auto
    });
}


console.log("EDITOR FUNCTIONALITIES - END");