/*
function fetchTemplate() {
    let scene = document.getElementById('myEmbeddedScene');
    var xhr1 = new XMLHttpRequest();
    // Setup our listener to process completed requests
    xhr1.onreadystatechange = function () {
        // Only run if the request is complete
        if (xhr1.readyState !== 4) return;
        // Process our return data
        if (xhr1.status >= 200 && xhr1.status < 300) {
            // What to do when the request is successful
            var response = JSON.parse(xhr1.responseText);
            console.log(response['resource_obj']['basis']);
            //scene.innerHTML = response['resource_obj']['basis'];

        } else {
            console.log('error', xhr1);
        }
    };
    // Create and send a GET request
    // The first argument is the post type (GET, POST, PUT, DELETE, etc.)
    // The second argument is the endpoint URL
    xhr1.open('GET', '/web_app/exhibitions/templates/fetch?template-id=7', true);
    xhr1.send();

}
*/
//fetchTemplate();
/*function getToRoom1() {
    var person = document.getElementById("camera");
    person.setAttribute('position', '2.5 1.6 4');
}

function getToRoom2() {
    var person = document.getElementById("camera");
    person.setAttribute('position', '2.5 1.6 -2');
}

function getToRoom3() {
    var person = document.getElementById("camera");
    person.setAttribute('position', '-4 1.6 -2');
}

function getToRoom4() {
    var person = document.getElementById("camera");
    person.setAttribute('position', '-4 1.6 4');
}
*/
var ACTIVE_ELEMENT = 'empty';
var TYPE = 'none';

function changeArtwork(box_id, artwork_id) {
    var box = document.getElementById(box_id);
    console.log(artwork_id);
    box.setAttribute('material', 'src:#' + artwork_id);
    updateDOM();
}

function changeArtworkByBox(box, artwork_id) {
    //** there should be some code to add the artwork to assets */
    box.setAttribute('material', 'src:#' + artwork_id);
    updateDOM();
}

function insertAsset(type, id, src) {
    var asset = document.createElement('img');
    asset.setAttribute('id', id);
    asset.setAttribute('src', src);
    asset.setAttribute('type', type);

    var assetlist = document.getElementsByTagName('a-assets')[0];
    assetlist.appendChild(asset);

}
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
    console.log(clickedElement);
    insertAsset('img', 'demo', clickedElement.getAttribute('src'))
    changeArtwork('face', 'demo');
    changeSizeOfBox('face', 8, 4, 0.2);
}

function fetchAssets() {
    var assets = document.getElementsByTagName("a-assets")[0];
    var len = assets.children.length;
    for (let i = 0; i < len; i++) {
        var as = assets.children[i];
        console.log(as);
    }

}

function assignArtworkOrTexture(clickedElement) {
    changeArtwork(ACTIVE_ELEMENT, clickedElement.getAttribute('param1'));
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
            var img0 = document.createElement('img');
            img0.setAttribute('id', 'as' + i);
            img0.setAttribute('src', as.currentSrc);
            img0.setAttribute('height', '100px');
            img0.setAttribute('width', '200px');
            am1.appendChild(img0);

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
            a0.setAttribute('onclick', 'assignArtworkOrTexture(this)');
            a0.textContent = 'Select';
            div8.appendChild(a0);
            div7.appendChild(div8);

            div1.appendChild(div7);

            div0.appendChild(div1);

            if (as.getAttribute('type') === 'artwork' && img0.src !== '') {
                document.getElementById('kt_table_widget_5_tab_3').appendChild(div0);
            } else if (as.getAttribute('type') === 'texture' && img0.id !== 'as24') {
                console.log(img0);
                document.getElementById('kt_table_widget_5_tab_2').appendChild(div0);
            }
        }
    }

}


function handleSizeChange() {
    var x = document.getElementById('x').value;
    var y = document.getElementById('y').value;
    var z = 0.2;

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


fillScrollableWithAssets();

function saveExhibit() {
    let exh = document.getElementsByTagName('a-scene')[0];
    console.log(exh);
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