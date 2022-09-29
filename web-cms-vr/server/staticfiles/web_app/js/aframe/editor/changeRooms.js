function fetchTemplate(){
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
    xhr1.open('GET', 'http://localhost:10000/web_app/exhibitions/templates/fetch?template-id=3', true);
    xhr1.send();

}

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

function updateDOM() {
    //var scene = document.querySelector('a-scene');
    //scene.flushToDOM(true);
    let z = document.getElementById(ACTIVE_ELEMENT);
    console.log(z.id);
    document.querySelector('#' + z.id).flushToDOM(true);
    console.log('DOM updated');
}

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

function changeSizeOfBox(box_id, x, y, z) {
    var box = document.getElementById(box_id);
    box.setAttribute('scale', {
        x: x,
        y: y,
        z: z
    });

}


function insertAsset(type, id, src) {
    if (type === 'img') {
        var asset = document.createElement('img');
        asset.setAttribute('id', id);
        asset.setAttribute('src', src);

        var assetlist = document.getElementsByTagName('a-assets')[0];
        assetlist.appendChild(asset);
    }
}

function activateArtworkChangeFunctionForABoxes() {
    var places = document.getElementsByTagName('a-box');
    var len = places.length;
    for (let i = 0; i < len; i++) {
        var child = places[i];
        child.setAttribute('setartworkrules', 'txt:' + child.getAttribute('id'));
    }

    places = document.getElementsByTagName('a-entity');
    len = places.length;
    for (let i = 0; i < len; i++) {
        var child = places[i];
        child.setAttribute('setlabelrules', 'txt:' + child.getAttribute('id'));
    }
    /*
    var places = document.getElementsByTagName('a-text');
    var len = places.length;
    for (let i = 0; i < len; i++) {
        var child = places[i];
        child.setAttribute('setartworkrules', 'txt:' + child.getAttribute('id'));
    }*/
}

function fillData() {
    var box = document.getElementById(ACTIVE_ELEMENT);
    if (box !== null) {
        document.getElementById('x').value = box.getAttribute('scale').x;
        document.getElementById('y').value = box.getAttribute('scale').y;

        if (TYPE === 'label') {
            console.log(box.getAttribute('text').value);
            document.getElementById("new_label").setAttribute('value', box.getAttribute('text').value);

            document.getElementById("html5colorpicker").remove();
            var in2 = document.createElement('input');
            in2.type = 'color';
            in2.id = "html5colorpicker";
            in2.style = "width:10%;";
            in2.setAttribute('value', box.getAttribute('text').color);

            const prof = document.getElementById("change_text");
            document.getElementById('txt-btn').insertBefore(in2, prof);

            document.getElementById("text_alteration").classList.remove("unvisible");
        } else if (TYPE === 'box') {
            document.getElementById("text_alteration").classList.add("unvisible");
        }
    } else {

    }

}
AFRAME.registerComponent('setartworkrules', {
    schema: {
        txt: {
            default: 'default'
        }
    },
    init: function () {
        var data = this.data;
        var el = this.el;
        el.addEventListener('click', function () {
            if (data.txt != "null") {
                ACTIVE_ELEMENT = data.txt;
                TYPE = 'box';
                console.log(ACTIVE_ELEMENT + ' is selected ' + TYPE);
                fillData();
            }

        });
    }
});

AFRAME.registerComponent('setlabelrules', {
    schema: {
        txt: {
            default: 'default'
        }
    },
    init: function () {
        var data = this.data;
        var el = this.el;
        el.addEventListener('click', function () {
            if (data.txt != "null") {
                ACTIVE_ELEMENT = data.txt;
                TYPE = 'label';
                console.log(ACTIVE_ELEMENT + ' is selected ' + TYPE);
                fillData();
            }


        });
    }
});


//document.getElementById('test').setAttribute('src',document.getElementById('pic4').getAttribute('src'));
document.getElementById('test2').setAttribute('src', document.getElementById('pic3').getAttribute('src'));
//document.getElementById('test3').setAttribute('href','http://localhost:10000/'+ document.getElementById('pic3').getAttribute('src'));
console.log(document.getElementById('pic3').getAttribute('src'));
document.getElementById('test3').href = "http://localhost:10000" + document.getElementById('pic3').getAttribute('src');

function setMe(clickedElement) {
    console.log(clickedElement);
    insertAsset('img', 'demo', clickedElement.getAttribute('src'))
    changeArtwork('face', 'demo');
    changeSizeOfBox('face', 8, 4, 0.5);
}

function fetchAssets() {
    var assets = document.getElementsByTagName("a-assets")[0];
    var len = assets.children.length;
    for (let i = 0; i < len; i++) {
        var as = assets.children[i];
        console.log(as);
    }

}

function assignArtwork(clickedElement) {
    console.log("ECHO");
    console.log(clickedElement.getAttribute('param1'));
    changeArtwork(ACTIVE_ELEMENT, clickedElement.getAttribute('param1'));

}

function showAssets() {
    var assets = document.getElementsByTagName("a-assets")[0];
    var len = assets.children.length;
    for (let i = 0; i < len; i++) {
        var as = assets.children[i];
        if (as.getAttribute('type') === 'artwork') {
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
            img0.setAttribute('src', as.src);
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
            a0.setAttribute('onclick', 'assignArtwork(this)');
            a0.textContent = 'Select';
            div8.appendChild(a0);
            div7.appendChild(div8);

            div1.appendChild(div7);

            div0.appendChild(div1);

            document.getElementById('kt_table_widget_5_tab_3').appendChild(div0);
        }
    }

}


function handleSizeChange() {
    var x = document.getElementById('x').value;
    var y = document.getElementById('y').value;
    var z = 0.5;

    changeSizeOfBox(ACTIVE_ELEMENT, x, y, z);
    updateDOM();

}

function left() {
    document.getElementById(ACTIVE_ELEMENT).setAttribute('position', {
        x: document.getElementById(ACTIVE_ELEMENT).getAttribute('position').x - 0.33,
        y: document.getElementById(ACTIVE_ELEMENT).getAttribute('position').y,
        z: document.getElementById(ACTIVE_ELEMENT).getAttribute('position').z
    });
    updateDOM();

}

function right() {
    document.getElementById(ACTIVE_ELEMENT).setAttribute('position', {
        x: document.getElementById(ACTIVE_ELEMENT).getAttribute('position').x + 0.33,
        y: document.getElementById(ACTIVE_ELEMENT).getAttribute('position').y,
        z: document.getElementById(ACTIVE_ELEMENT).getAttribute('position').z
    });
    updateDOM();

}

function down() {
    document.getElementById(ACTIVE_ELEMENT).setAttribute('position', {
        x: document.getElementById(ACTIVE_ELEMENT).getAttribute('position').x,
        y: document.getElementById(ACTIVE_ELEMENT).getAttribute('position').y - 0.33,
        z: document.getElementById(ACTIVE_ELEMENT).getAttribute('position').z
    });
    updateDOM();

}

function up() {
    document.getElementById(ACTIVE_ELEMENT).setAttribute('position', {
        x: document.getElementById(ACTIVE_ELEMENT).getAttribute('position').x,
        y: document.getElementById(ACTIVE_ELEMENT).getAttribute('position').y + 0.33,
        z: document.getElementById(ACTIVE_ELEMENT).getAttribute('position').z
    });
    updateDOM();

}

function deleteActiveElement() {
    document.getElementById(ACTIVE_ELEMENT).remove();
    ACTIVE_ELEMENT = "";
    document.getElementById('x').value = "";
    document.getElementById('y').value = "";
    document.getElementById("text_alteration").value = "";
    document.getElementById("text_alteration").classList.add('unvisible');
}

function changeText() {
    document.getElementById("text_alteration").value = "";
    document.getElementById(ACTIVE_ELEMENT).setAttribute('text', {
        color: document.getElementById('html5colorpicker').value,
        value: document.getElementById('new_label').value
    });
    updateDOM();
}


activateArtworkChangeFunctionForABoxes();
showAssets();

function saveExhibit(){
    let exh = document.getElementsByTagName('a-scene')[0];
    console.log(exh);
}
