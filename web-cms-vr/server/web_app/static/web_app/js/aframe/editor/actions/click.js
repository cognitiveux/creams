/// Click Functionality ///
CLICK_EVENT_ACTIONS = [];

CLICK_EVENT_START = `
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
`;

CLICK_EVENT_END = `
        });
    }
});
`;

function addClickEvent(id, action) {
    let condition = `if (data.txt ===\'` + id + `\' ){` + action + `}`
    CLICK_EVENT_ACTIONS.push(condition);
}

function addPopUp(id) {
    addClickEvent(id, POP_UP);
}

function getClickEventCode(items_list) {
    let EVENTS = '';
    for (let i = 0; i < CLICK_EVENT_ACTIONS.length; i++) {
        EVENTS += CLICK_EVENT_ACTIONS[i];
    }
    CLICK_EVENT_ACTIONS = [];
    return createList(items_list) + CLICK_EVENT_START + EVENTS + CLICK_EVENT_END;
}


POP_UP = `                
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
            value: it['text'] + ";"
        });
        plane.setAttribute('editorFunctionalities', {
            txt: it['id']
        });
        plane.setAttribute('position', {
            x: it['x'],
            y: it['y'],
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
`

function createList(list) {
    return `var items = ` + JSON.stringify(list) + `;
    `;
}


function getNewScript(items) {
    for (let i = 0; i < items.length; i++) {
        addPopUp(items[i]['alias']);
    }
    return getClickEventCode(items);
}