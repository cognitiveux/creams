function submitAssessment() {
    console.log("SAD");
    let value = document.getElementById('textBox1').value;
    assessStudent(user_id, exh_id, student_id, value);
}

function getRandom() {
    return Math.floor(Math.random() * 4);
}
let firlet = document.getElementById('FIRST_LETTER');
let flag = getRandom();
if (flag === 0) {
    firlet.classList.add('text-warning');
    firlet.classList.add('bg-light-warning');
} else if (flag === 1) {
    firlet.classList.add('text-info');
    firlet.classList.add('bg-light-info');
} else if (flag === 2) {
    firlet.classList.add('text-success');
    firlet.classList.add('bg-light-success');
} else if (flag === 3) {
    firlet.classList.add('text-primary');
    firlet.classList.add('bg-light-primary');
}
firlet.textContent = f_name[0].toUpperCase();
