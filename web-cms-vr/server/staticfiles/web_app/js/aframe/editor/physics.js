function updateDOM() {
    //var scene = document.querySelector('a-scene');
    //scene.flushToDOM(true);
    let z = document.getElementById(ACTIVE_ELEMENT);
    console.log(z.id);
    document.querySelector('#' + z.id).flushToDOM(true);
    console.log('DOM updated');
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
    updateDOM();
}

function changeSizeOfBox(box_id, x, y, z) {
    var box = document.getElementById(box_id);
    if( TYPE === 'box' ){
        box.setAttribute('scale', {
            x: x,
            y: y,
            z: z
        });
    }
    else if( TYPE === 'label' ){
        box.setAttribute('text', {
            width: x,
            height: y,
        });
    }

}
