ACTIVE_WALLS = false;
var previous_state;

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
            if (data.txt != "null" && !ACTIVE_WALLS) {
                ACTIVE_ELEMENT = data.txt;
                TYPE = 'box';
                console.log(ACTIVE_ELEMENT + ' is selected ' + TYPE);
                fillData();
            }

        });
    }
});
AFRAME.registerComponent('setwallrules', {
    schema: {
        txt: {
            default: 'default'
        }
    },
    init: function () {
        var data = this.data;
        var el = this.el;
        el.addEventListener('click', function () {
            if (data.txt != "null" && ACTIVE_WALLS) {
                ACTIVE_ELEMENT = data.txt;
                TYPE = 'wall';
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
            if (data.txt != "null" && !ACTIVE_WALLS) {
                ACTIVE_ELEMENT = data.txt;
                TYPE = 'label';
                console.log(ACTIVE_ELEMENT + ' is selected ' + TYPE);
                fillData();
            }


        });
    }
});


function activateArtworkChangeFunctionForABoxes() {
    var places = document.getElementsByTagName('a-box');
    var len = places.length;
    for (let i = 0; i < len; i++) {
        var child = places[i];
        child.setAttribute('setartworkrules', 'txt:' + child.getAttribute('id'));
        child.flushToDOM(true);
    }

    places = document.getElementsByTagName('a-entity');
    len = places.length;
    for (let i = 0; i < len; i++) {
        var child = places[i];
        child.setAttribute('setlabelrules', 'txt:' + child.getAttribute('id'));
        child.flushToDOM(true);
    }

    places = document.getElementsByTagName('rw-wall');
    len = places.length;
    for (let i = 0; i < len; i++) {
        var child = places[i];
        child.setAttribute('setwallrules', 'txt:' + child.getAttribute('id'));
    }

    places = document.getElementsByTagName('rw-ceiling');
    len = places.length;
    for (let i = 0; i < len; i++) {
        var child = places[i];
        child.setAttribute('setwallrules', 'txt:' + child.getAttribute('id'));
    }


}

activateArtworkChangeFunctionForABoxes();

function setWalls(flag) {
    previous_state = ACTIVE_WALLS;
    ACTIVE_WALLS = flag;
    if (ACTIVE_WALLS || TYPE==='wall' ) {
        ACTIVE_ELEMENT ='';
    }
}

function fillData() {
    var box = document.getElementById(ACTIVE_ELEMENT);
    if (box !== null) {
        if (TYPE === 'label') {
            document.getElementById('x').value = box.getAttribute('text').width;
            document.getElementById('y').value = box.getAttribute('text').height;
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
            document.getElementById('x').value = box.getAttribute('scale').x;
            document.getElementById('y').value = box.getAttribute('scale').y;
            document.getElementById("text_alteration").classList.add("unvisible");
        }
    } else {

    }

}