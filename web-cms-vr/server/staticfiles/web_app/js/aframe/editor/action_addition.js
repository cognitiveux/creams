AFRAME.registerComponent('editorfunctionalities', {
    schema: {
        txt: {
            default: 'default'
        }
    },
    init: function () {
        var data = this.data;
        var el = this.el;
        el.addEventListener('click', function () {
            if (el.id != "null" && !ACTIVE_WALLS) {
                ACTIVE_ELEMENT = el.id;
                TYPE = 'extra';
                console.log(ACTIVE_ELEMENT + ' is selected ' + TYPE);
                fillData();
            }


        });
    }
});

function addPane(data) {
    let it = find(data.txt);
    if (document.getElementById("parent_" + it['alias'] + "_" + it['id']) === null) {
        let a = $("#" + it['alias']).parent();
        let parent = document.getElementById(a[0].id);
        let holder = document.createElement('a-entity');
        holder.id = "parent_" + it['alias'] + "_" + it['id'];
        let plane = document.createElement('a-plane');
        plane.id = it['id'];
        plane.setAttribute('width', it['width']);
        plane.setAttribute('height', it['height']);
        plane.setAttribute('material', 'color: ' + it['color']);
        plane.setAttribute('text', {
            value: it['text'] + "; color:#000000"
        });
        plane.setAttribute('editorFunctionalities', {
            txt: it['id']
        });
        let height = it['y'] - 2;
        if( height <= 1)
            height = 1;

        plane.setAttribute('position', {
            x: it['x'],
            y: height,
            z: it['z']
        });
        holder.appendChild(plane);
        plane.setAttribute('rotation', {
            x: it['r1'],
            y: it['r2'],
            z: it['r3']
        });
        holder.appendChild(plane);
        parent.appendChild(holder);
        document.querySelector('#' + holder.id).flushToDOM(true);
    } else {
        document.getElementById("parent_" + it['alias'] + "_" + it['id']).remove();
    }
}
var items = []; 

function find(alias) {
    for (let i = 0; i < items.length; i++) {
        if (alias === items[i]['alias'])
            return items[i];
    }
}
AFRAME.registerComponent('clickhandler', {
    schema: {
        txt: {
            default: 'default'
        }
    },

    init: function () {

        var data = this.data;
        var el = this.el;
        el.addEventListener('click', function () {
            console.log("TEST");
            addPane(data);

        });
    }
});
let cnt = 0;

function getWall(id) {
    console.log($("#" + id).parent());
    let a = $("#" + id).parent();
    let len = a[0].id.length;
    let room = a[0].id[len - 1];
    if (room === '1')
        return "front";
    if (room === '2')
        return "right";
    if (room === '3')
        return "back";
    if (room === '4')
        return "left";

}

function addItem() {
    let WALL = getWall(ACTIVE_ELEMENT);
    if (ACTIVE_ELEMENT !== 'empty') {
        let flag = false;
        for (let i = 0; i < items.length; i++) {
            if (items[i]['alias'] === ACTIVE_ELEMENT) {
                items[i] = {
                    alias: ACTIVE_ELEMENT,
                    id: items[i]['id'],
                    color: items[i]['color'],
                    text: document.getElementById('plane_msg').value,
                    height: items[i]['height'],
                    width: items[i]['width'],
                    x: items[i]['x'],
                    y: items[i]['y'],
                    z: items[i]['z'],
                    r1: 0,
                    r2: 0,
                    r3: 0,
                }
                flag = true;
                break;
            }
        }
        if (flag === false) {
            let x = document.getElementById(ACTIVE_ELEMENT).getAttribute('position').x;
            let y = document.getElementById(ACTIVE_ELEMENT).getAttribute('position').y;
            console.log($("#" + ACTIVE_ELEMENT).parent());
            items.push({
                alias: ACTIVE_ELEMENT,
                id: "" + cnt,
                color: "#C0C0C0",
                text: document.getElementById('plane_msg').value,
                height: "1",
                width: "2.5",
                x: x,
                y: y,
                z: "1",
                r1: 0,
                r2: 0,
                r3: 0,
            });
            cnt++;
        }
    }
    document.getElementById('plane_msg').value = '';
}
