const first = document.getElementById('first_row');
const second = document.getElementById('kt_followers_show_more_cards');

function getRandom() {
    return Math.floor(Math.random() * 4);
}

function createStudentThumbnail(students, i, target) {
    let div0 = document.createElement('div');
    div0.classList.add('col-md-6');
    div0.classList.add('col-xxl-4');

    let div1 = document.createElement('div');
    div1.classList.add('card');

    let div2 = document.createElement('div');
    div2.classList.add('card-body');
    div2.classList.add('d-flex');
    div2.classList.add('flex-center');
    div2.classList.add('flex-column');
    div2.classList.add('py-9');
    div2.classList.add('px-5');

    let div3 = document.createElement('div');
    div3.classList.add('symbol');
    div3.classList.add('symbol-65px');
    div3.classList.add('symbol-circle');
    div3.classList.add('mb-5');

    let span0 = document.createElement('span');
    span0.classList.add('symbol-label');
    span0.classList.add('fs-2x');
    span0.classList.add('fw-semibold');
    let flag = getRandom();
    if (flag === 0) {
        span0.classList.add('text-warning');
        span0.classList.add('bg-light-warning');
    } else if (flag === 1) {
        span0.classList.add('text-info');
        span0.classList.add('bg-light-info');
    } else if (flag === 2) {
        span0.classList.add('text-success');
        span0.classList.add('bg-light-success');
    } else if (flag === 3) {
        span0.classList.add('text-primary');
        span0.classList.add('bg-light-primary');
    }
    span0.textContent = students[i]['name'][0].toUpperCase();
    div3.appendChild(span0);
    div2.appendChild(div3);

    let a0 = document.createElement('a');
    a0.href = "#";
    a0.classList.add('fs-4');
    a0.classList.add('text-gray-800');
    a0.classList.add('fw-bold');
    a0.classList.add('mb-0');
    a0.textContent = students[i]['name'] + " " + students[i]['surname'];
    div2.appendChild(a0);

    let br0 = document.createElement('br');
    div2.appendChild(br0);

    let a1 = document.createElement('a');
    a1.href = "#";
    a1.classList.add('fs-5');
    a1.classList.add('text-gray-800');
    a1.classList.add('fw-bold');
    a1.classList.add('mb-0');
    a1.classList.add('text-hover-primary');
    a1.textContent = "VR Exhibition";
    div2.appendChild(a1);


    let div4 = document.createElement('div');
    div4.classList.add('fw-semibold');
    div4.classList.add('text-gray-400');
    div4.classList.add('mb-6');
    div4.textContent = "Remaining Artworks: 3";
    div2.appendChild(div4);

    let a2 = document.createElement('a');
    a2.href = "#";
    a2.classList.add('fs-5');
    a2.classList.add('text-gray-800');
    a2.classList.add('fw-bold');
    a2.classList.add('mb-0');
    a2.classList.add('text-hover-primary');
    a2.textContent = "AR Exhibition";
    div2.appendChild(a2);

    let div5 = document.createElement('div');
    div5.classList.add('fw-semibold');
    div5.classList.add('text-gray-400');
    div5.classList.add('mb-6');
    div5.textContent = "Remaining Artworks: 2";
    div2.appendChild(div5);

    let br1 = document.createElement('br');
    div2.appendChild(br1);

    let a3 = document.createElement('a');
    a3.href = "/web_app/teacher/assessment/students/?q=" + exh_id + "&s=" + students[i]['id'];
    a3.classList.add('btn');
    a3.classList.add('btn-success');
    a3.classList.add('fw-semibold');
    a3.classList.add('px-6');
    a3.classList.add('py-3');
    a3.textContent = "Assess";
    div2.appendChild(a3);

    div1.appendChild(div2);
    div0.appendChild(div1);

    target.appendChild(div0);
}

function addStudents() {
    var xhr1 = new XMLHttpRequest();
    // Setup our listener to process completed requests
    xhr1.onreadystatechange = function () {
        // Only run if the request is complete
        if (xhr1.readyState !== 4) return;
        // Process our return data
        if (xhr1.status >= 200 && xhr1.status < 300) {
            // What to do when the request is successful
            var response = JSON.parse(xhr1.responseText)['resource_obj']['students'];
            for (let i = 0; i < response.length; i++) {
                let tar = first;
                if (i > 8)
                    tar = second;
                createStudentThumbnail(response, i, tar);
            }
        } else {
            console.log('error', xhr1);
        }
    };
    xhr1.open('GET', '/web_app/assignment/assessment/getStudents?exh_id=' + exh_id, true);
    xhr1.send();
}
addStudents();