const students = document.getElementById("student_table");
const instructors = document.getElementById("instructor_table");
let selected_studs = [];
let selected_instr = [];
function submit() {
    //window.location.href = "/web_app/teacher/student_selection/?q=haha"
    selected_studs = [];
    for (var i = 0; i < students.childElementCount; i++) {
        var student = students.children[i];
        // EXTRA CAUTION WHEN CHANGING THE TABLE LAYOUT
        if(student.children[3].children[0].children[0].checked){
            selected_studs.push(student.id);
            postStudentConnection(student.id,exh_id);
        }

    }
    selected_instr = [];
    for (var i = 0; i < instructors.childElementCount; i++) {
        var instructor = instructors.children[i];
        // EXTRA CAUTION WHEN CHANGING THE TABLE LAYOUT
        if(instructor.children[3].children[0].children[0].checked)
            selected_instr.push(instructor.id);

    }
    console.log(selected_studs);
    console.log(selected_instr);
    window.location.href = "/web_app/teacher/dashboard/";

}

function createTableElement() {

    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function () {
        // Only run if the request is complete
        if (xhr.readyState !== 4) return;
        // Process our return data
        if (xhr.status >= 200 && xhr.status < 300) {
            // What to do when the request is successful
            var response = JSON.parse(xhr.responseText)['resource_obj']['users'];
            let student_table = document.getElementById("student_table");
            let instructor_table = document.getElementById("instructor_table");
            let j = 0;
            for (let i = 0; j < 5 * response.length; i++) {
                j++;
                if (i === 2) i = 0;
                let tr = document.createElement('tr');
                // att 1 
                let td0 = document.createElement('td');
                let a0 = document.createElement('a');
                //a0.href = '#'; 
                a0.classList.add('text-gray-800');
                a0.classList.add('text-hover-primary');
                a0.classList.add('mb-1');
                a0.textContent = response[i]['name'] + ' ' + response[i]['surname'];
                td0.appendChild(a0);
                tr.appendChild(td0);
                // attr 2
                let td1 = document.createElement('td');
                let a1 = document.createElement('a');
                //a1.href = '#'; 
                a1.classList.add('text-gray-600');
                a1.classList.add('text-hover-primary');
                a1.classList.add('mb-1');
                a1.textContent = response[i]['email'];
                td1.appendChild(a1);
                tr.appendChild(td1);
                // attr 3
                let td2 = document.createElement('td');
                let a2 = document.createElement('a');
                //a2.href = '#'; 
                a2.classList.add('badge');
                if (response[i]['role'] === 'INSTRUCTOR')
                    a2.classList.add('badge-light-info');
                else
                    a2.classList.add('badge-light-success');
                a2.textContent = response[i]['class_level'];
                td2.appendChild(a2);
                tr.appendChild(td2);
                // attr 4
                let td3 = document.createElement('td');
                let div3 = document.createElement('div');
                div3.classList.add('form-check');
                div3.classList.add('form-check-sm');
                div3.classList.add('form-check-custom');
                div3.classList.add('form-check-solid');
                let in0 = document.createElement('input');
                in0.classList.add('form-check-input');
                in0.type = 'checkbox';
                in0.value = "1";
                div3.appendChild(in0);
                td3.appendChild(div3);
                tr.appendChild(td3);
                tr.id = response[i]['id'];
                if (response[i]['role'] === 'STUDENT')
                    student_table.appendChild(tr);
                else
                    instructor_table.appendChild(tr);
            }

        } else {
            console.log('error', xhr);
        }
    });

    xhr.open("GET", "/web_app/teacher/other_users", false);
    xhr.send();

}

createTableElement();


function postStudentConnection(student,assignment){
    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function () {
        // Only run if the request is complete
        if (xhr.readyState !== 4) return;
        // Process our return data
        if (xhr.status >= 200 && xhr.status < 300) {
            // What to do when the request is successful
            var response = JSON.parse(xhr.responseText);
            console.log(response);
        } else {
            console.log('error', xhr);
        }
    });

    xhr.open("POST", "/web_app/assignment/assign_student", true);
    let formData = new FormData(); 
    formData.append("student_fk", student); 
    formData.append("assignment_fk", assignment); 
    xhr.send(formData);
}