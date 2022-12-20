function assessStudent(user_id, exh_id, student_id, value) {
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
    var xhr1 = new XMLHttpRequest();
    // Setup our listener to process completed requests
    xhr1.onreadystatechange = function () {
        // Only run if the request is complete
        if (xhr1.readyState !== 4) return;
        // Process our return data
        if (xhr1.status >= 200 && xhr1.status < 300) {
            // What to do when the request is successful
            var response = JSON.parse(xhr1.responseText);
            console.table(response);
            toastr.success("Insertion successful!");
        } else {
            console.log('error', xhr1);
            toastr.error("Something went wrong!");
        }
    };
    xhr1.open('POST', '/web_app/assignment/assessment/assess/', true);
    let formData = new FormData(); // creates an object, optionally fill from <form>
    formData.append("instructor_fk", user_id); // appends a field
    formData.append("assignment_fk", exh_id); // appends a field
    formData.append("student_fk", student_id); // appends a field
    formData.append("assessement", value); // appends a field
    xhr1.send(formData);
}

