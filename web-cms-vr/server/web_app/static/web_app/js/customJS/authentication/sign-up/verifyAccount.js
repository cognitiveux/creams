"use strict";

// Class Definition
var KTSigninTwoSteps = function () {
    // Elements
    var form;
    var submitButton;

    // Handle form
    var handleForm = function (e) {
        // Handle form submit
        submitButton.addEventListener('click', function (e) {
            
            e.preventDefault();

            var validated = true;

            var inputs = [].slice.call(form.querySelectorAll('input[maxlength="32"]'));
            var email = document.getElementById('emailinput');
            inputs.map(function (input) {
                if (input.value === '' || input.value.length !== 32 || email.value.length <= 3 ) {
                    validated = false;
                }
            });

            if (validated === true) {
                let code = inputs[0].value;
                let email_value = email.value;
                // Show loading indication
                submitButton.setAttribute('data-kt-indicator', 'on');

                // Disable button to avoid multiple click 
                submitButton.disabled = true;

                var xhr1 = new XMLHttpRequest();
                // Setup our listener to process completed requests
                xhr1.onreadystatechange = function () {
                    // Only run if the request is complete
                    if (xhr1.readyState !== 4) return;
                    // Process our return data
                    if (xhr1.status >= 200 && xhr1.status < 300) {
                        // What to do when the request is successful
                        var response = JSON.parse(xhr1.responseText);
                       
                        console.log(response);
                        submitButton.removeAttribute('data-kt-indicator');
                        
                        

                        // Enable button
                        submitButton.disabled = false;

                        // Show message popup. For more info check the plugin's official documentation: https://sweetalert2.github.io/
                        Swal.fire({
                            text: "You have been successfully verified!",
                            icon: "success",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn btn-primary"
                            }
                        }).then(function (result) {
                            if (result.isConfirmed) {
                                inputs.map(function (input) {
                                    input.value = '';
                                });

                                var redirectUrl = form.getAttribute('data-kt-redirect-url');
                                if (redirectUrl) {
                                    location.href = redirectUrl;
                                }
                            }
                            window.location.href = "/web_app/login/";

                        });

                    } else {
                        document.getElementById('code').value = '';
                        document.getElementById('kt_sing_in_two_steps_submit').setAttribute('data-kt-indicator', 'off');
                        document.getElementById('kt_sing_in_two_steps_submit').removeAttribute('disabled');
                        swal.fire({
                            text: "Please enter valid securtiy code and try again.",
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn fw-bold btn-light-primary"
                            }
                        }).then(function () {
                            KTUtil.scrollTop();
                        });
                    }

                }
                // Create and send a GET request
                // The first argument is the post type (GET, POST, PUT, DELETE, etc.)
                // The second argument is the endpoint URL
                xhr1.open('POST', '/web_app/account-mgmt/activate-account', true);
                let formData = new FormData(); // creates an object, optionally fill from <form>
                formData.append("email", email_value); // appends a field
                console.log(code);
                formData.append("verification_code", code); // appends a field
                xhr1.send(formData);

            } else {
                document.getElementById('code').value = '';
                document.getElementById('kt_sing_in_two_steps_submit').setAttribute('data-kt-indicator', 'off');
                document.getElementById('kt_sing_in_two_steps_submit').removeAttribute('disabled');
                swal.fire({
                    text: "Please enter valid securtiy code and try again.",
                    icon: "error",
                    buttonsStyling: false,
                    confirmButtonText: "Ok, got it!",
                    customClass: {
                        confirmButton: "btn fw-bold btn-light-primary"
                    }
                }).then(function () {
                    KTUtil.scrollTop();
                });
            }
        });
    }

    var handleType = function () {
        var input1 = form.querySelector("[name=code_1]");

        input1.focus();

    }

    // Public functions
    return {
        // Initialization
        init: function () {
            form = document.querySelector('#kt_sing_in_two_steps_form');
            submitButton = document.querySelector('#kt_sing_in_two_steps_submit');

            handleForm();
            handleType();
        }
    };
}();

// On document ready
KTUtil.onDOMContentLoaded(function () {
    KTSigninTwoSteps.init();
});