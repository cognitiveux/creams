"use strict";
// Class definition

var KTSigninGeneral = function () {
    // Elements
    var form;
    var submitButton;
    var validator;
    var resultObj;


    // Handle form
    var handleForm = function (e) {

        // Init form validation rules. For more info check the FormValidation plugin's official documentation:https://formvalidation.io/
        validator = FormValidation.formValidation(
            form, {
                fields: {
                    'email': {
                        validators: {
                            regexp: {
                                regexp: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                                message: 'The value is not a valid email address',
                            },
                            notEmpty: {
                                message: 'Email address is required'
                            }
                        }
                    },
                    'password': {
                        validators: {
                            notEmpty: {
                                message: 'The password is required'
                            }
                        }
                    }
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    bootstrap: new FormValidation.plugins.Bootstrap5({
                        rowSelector: '.fv-row',
                        eleInvalidClass: '', // comment to enable invalid state icons
                        eleValidClass: '' // comment to enable valid state icons
                    })
                }
            }
        );

        // Handle form submit
        submitButton.addEventListener('click', function (e) {
            // Prevent button default action
            e.preventDefault();

            // Validate form
            validator.validate().then(function (status) {

                if (status == 'Valid') {
                    // Show loading indication
                    submitButton.setAttribute('data-kt-indicator', 'on');

                    // Disable button to avoid multiple click 
                    submitButton.disabled = true;

                    var email = form.querySelector('[name="email"]').value;
                    var password = form.querySelector('[name="password"]').value;

                    var xhr1 = new XMLHttpRequest();
                    // Setup our listener to process completed requests
                    xhr1.onreadystatechange = function () {
                        // Only run if the request is complete
                        if (xhr1.readyState !== 4) return;
                        // Process our return data
                        if (xhr1.status >= 200 && xhr1.status < 300) {
                            // What to do when the request is successful
                            var response = JSON.parse(xhr1.responseText);
                            var tkn_access = response['resource_obj']['access'];
                            var tkn_refresh = response['resource_obj']['refresh'];

                            var base64Url = tkn_access.split('.')[1];
                            var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
                            var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function (c) {
                                return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
                            }).join(''));
                            resultObj = JSON.parse(jsonPayload);

                            form.querySelector('[name="email"]').value = "";
                            form.querySelector('[name="password"]').value = "";

                            //form.submit(); // submit form
                            if (resultObj.role === "INSTRUCTOR") {
                                submitButton.removeAttribute('data-kt-indicator');
                                console.log("Welcome " + resultObj.name + " " + resultObj.surname);
                                location.href = '/web_app/teacher/dashboard/';

                            } else if (resultObj.role === 'STUDENT') {
                                console.log("Welcome " + resultObj.name + " " + resultObj.surname);
                                submitButton.removeAttribute('data-kt-indicator');
                                location.href = '/web_app/student/dashboard/';
                            } else {
                                alert("Something went wrong!");
                            }

                            // Simulate ajax request
                            /*
                            setTimeout(function () {
                                // Hide loading indication
                                submitButton.removeAttribute('data-kt-indicator');

                                // Enable button
                                submitButton.disabled = false;

                                // Show message popup. For more info check the plugin's official documentation: https://sweetalert2.github.io/
                                Swal.fire({
                                    text: "You have successfully logged in!",
                                    icon: "success",
                                    buttonsStyling: false,
                                    confirmButtonText: "Ok, got it!",
                                    customClass: {
                                        confirmButton: "btn btn-primary"
                                    }
                                }).then(function (result) {
                                    if (result.isConfirmed) {

                                        form.querySelector('[name="email"]').value = "";
                                        form.querySelector('[name="password"]').value = "";

                                        //form.submit(); // submit form
                                        if (resultObj.role === "INSTRUCTOR") {
                                            console.log("Welcome " + resultObj.name + " " + resultObj.surname);
                                            location.href = '/web_app/teacher/dashboard/';

                                        } else if (resultObj.role === 'STUDENT') {
                                            console.log("Welcome " + resultObj.name + " " + resultObj.surname);
                                            location.href = '/web_app/student/dashboard/';
                                        } else {
                                            alert("Something went wrong!");
                                        }

                                    }
                                });
                            }, 2000);*/


                        } else {
                            // What to do when the request has failed
                            // Hide loading indication
                            submitButton.removeAttribute('data-kt-indicator');

                            // Enable button
                            submitButton.disabled = false;
                            //form.querySelector('[name="email"]').value = "";
                            form.querySelector('[name="password"]').value = "";
                            Swal.fire({
                                text: "Wrong credentials, please try again.",
                                icon: "error",
                                buttonsStyling: false,
                                confirmButtonText: "Ok, got it!",
                                customClass: {
                                    confirmButton: "btn btn-primary"
                                }
                            });
                            console.log('error', xhr1);
                        }
                    };
                    // Create and send a GET request
                    // The first argument is the post type (GET, POST, PUT, DELETE, etc.)
                    // The second argument is the endpoint URL
                    xhr1.open('POST', '/web_app/account-mgmt/login', true);
                    let formData = new FormData(); // creates an object, optionally fill from <form>
                    formData.append("email", email); // appends a field
                    formData.append("password", password); // appends a field
                    xhr1.send(formData);


                } else {
                    // Show error popup. For more info check the plugin's official documentation: https://sweetalert2.github.io/
                    Swal.fire({
                        text: "Sorry, looks like there are some errors detected, please try again.",
                        icon: "error",
                        buttonsStyling: false,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn btn-primary"
                        }
                    });
                }
            });
        });
    }

    // Public functions
    return {
        // Initialization
        init: function () {
            form = document.querySelector('#kt_sign_in_form');
            submitButton = document.querySelector('#kt_sign_in_submit');

            handleForm();
        }
    };
}();

// On document ready
KTUtil.onDOMContentLoaded(function () {
    KTSigninGeneral.init();
});