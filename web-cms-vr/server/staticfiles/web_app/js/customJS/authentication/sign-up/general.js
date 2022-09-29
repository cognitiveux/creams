"use strict";


function de_list_python(list) {
    let words = [];
    let word = [];
    let flag = false;
    for (let i = 0; i < list.length; i++) {
        if (list[i] === ';') {
            flag = true;
            continue;
        } else if (flag && list[i] === '&') {
            flag = false;
            if (word.join("") !== " ")
                words.push(word.join(""));
            word = [];
            continue;
        }
        if (flag && list[i] !== ',') {
            word.push(list[i]);
        }
    }
    return words;
}

let real_list_roles = de_list_python(roles);

let rolelist = document.getElementById('rolelist');
console.log(real_list_roles);
for (let rl in real_list_roles) {
    let opt = document.createElement('option');
    opt.value = real_list_roles[rl];
    //if (real_list_roles[rl] !== 'INSTRUCTOR')
    rolelist.appendChild(opt);

}
let real_list_org = de_list_python(organizations);

let orglist = document.getElementById('orglist');
console.log(real_list_org);
for (let rl in real_list_org) {
    let opt = document.createElement('option');
    opt.value = real_list_org[rl];
    orglist.appendChild(opt);

}

let real_list_st = de_list_python(student_choices);
let real_list_te = de_list_python(teacher_choices);

function onInput(input, list) {
    let selection = input.value;
    if (selection === 'INSTRUCTOR') {
        list.innerHTML = '';
        let rolelist = document.getElementById('classlist');
        document.getElementById('class').placeholder = "Select instructor position";
        for (let rl in real_list_te) {
            let opt = document.createElement('option');
            opt.value = real_list_te[rl];
            rolelist.appendChild(opt);
        }
    } else if (selection === 'STUDENT') {
        list.innerHTML = '';
        let rolelist = document.getElementById('classlist');
        document.getElementById('class').placeholder = "Select class";
        for (let rl in real_list_st) {
            let opt = document.createElement('option');
            opt.value = real_list_st[rl];
            rolelist.appendChild(opt);
        }
    } else {
        list.innerHTML = '';
        document.getElementById('class').placeholder = "Select role first";
    }
}


// Class definition
var KTSignupGeneral = function () {
    // Elements
    var form;
    var submitButton;
    var validator;
    var passwordMeter;

    // Handle form
    var handleForm = function (e) {
        // Init form validation rules. For more info check the FormValidation plugin's official documentation:https://formvalidation.io/
        validator = FormValidation.formValidation(
            form, {
                fields: {
                    'first-name': {
                        validators: {
                            notEmpty: {
                                message: 'First Name is required'
                            }
                        }
                    },
                    'last-name': {
                        validators: {
                            notEmpty: {
                                message: 'Last Name is required'
                            }
                        }
                    },

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
                            },
                            callback: {
                                message: 'Please enter valid password',
                                callback: function (input) {
                                    if (input.value.length > 0) {
                                        return validatePassword();
                                    }
                                }
                            }
                        }
                    },
                    'confirm-password': {
                        validators: {
                            notEmpty: {
                                message: 'The password confirmation is required'
                            },
                            identical: {
                                compare: function () {
                                    return form.querySelector('[name="password"]').value;
                                },
                                message: 'The password and its confirm are not the same'
                            }
                        }
                    },
                    'role-selection': {
                        validators: {
                            notEmpty: {
                                message: 'Role selection is required'
                            }
                        }
                    },
                    'class-selection': {
                        validators: {
                            notEmpty: {
                                message: 'Class/Position selection is required'
                            }
                        }
                    },
                    'toc': {
                        validators: {
                            notEmpty: {
                                message: 'You must accept the terms and conditions'
                            }
                        }
                    }
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger({
                        event: {
                            password: false
                        }
                    }),
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
            e.preventDefault();

            validator.revalidateField('password');

            validator.validate().then(function (status) {
                if (status == 'Valid') {
                    // Show loading indication
                    submitButton.setAttribute('data-kt-indicator', 'on');
                    let email = form.querySelector('[name="email"]').value;
                    let password = form.querySelector('[name="password"]').value;
                    let first = form.querySelector('[name="first-name"]').value;
                    let last = form.querySelector('[name="last-name"]').value;
                    let role = form.querySelector('[name="role-selection"]').value;
                    let org = form.querySelector('[name="org-selection"]').value;
                    let _class = form.querySelector('[name="class-selection"]').value;

                    console.log(email);
                    console.log(password);
                    console.log(first);
                    console.log(last);
                    console.log(role);
                    console.log(org);
                    console.log(_class);

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
                            // Simulate ajax request
                            setTimeout(function () {
                                // Hide loading indication
                                submitButton.removeAttribute('data-kt-indicator');

                                // Enable button
                                submitButton.disabled = false;

                                // Show message popup. For more info check the plugin's official documentation: https://sweetalert2.github.io/
                                Swal.fire({
                                    text: "You have successfully signed up!",
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
                                        form.querySelector('[name="confirm-password"]').value = "";
                                        form.querySelector('[name="first-name"]').value = "";
                                        form.querySelector('[name="last-name"]').value = "";
                                        form.querySelector('[name="role-selection"]').value = "";
                                        form.querySelector('[name="org-selection"]').value = "";
                                        form.querySelector('[name="class-selection"]').value = "";

                                        window.location.href = "/web_app/verify-account/";


                                    }
                                });
                            }, 2000);


                        } else {
                            // What to do when the request has failed
                            // Hide loading indication
                            submitButton.removeAttribute('data-kt-indicator');

                            // Enable button
                            submitButton.disabled = false;
                            form.querySelector('[name="email"]').value = "";
                            form.querySelector('[name="password"]').value = "";
                            form.querySelector('[name="confirm-password"]').value = "";
                            form.querySelector('[name="first-name"]').value = "";
                            form.querySelector('[name="last-name"]').value = "";
                            form.querySelector('[name="role-selection"]').value = "";
                            form.querySelector('[name="org-selection"]').value = "";
                            form.querySelector('[name="class-selection"]').value = "";

                            Swal.fire({
                                text: "Something went wrong, please try again.",
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
                    xhr1.open('POST', '/web_app/account-mgmt/create-user', true);
                    let formData = new FormData(); // creates an object, optionally fill from <form>
                    formData.append("email", email); // appends a field
                    formData.append("password", password); // appends a field   
                    formData.append("name", first); // appends a field   
                    formData.append("surname", last); // appends a field      
                    formData.append("role", role); // appends a field       
                    formData.append("organization", org); // appends a field      
                    formData.append("class_level", _class); // appends a field      
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

        // Handle password input
        form.querySelector('input[name="password"]').addEventListener('input', function () {
            if (this.value.length > 0) {
                validator.updateFieldStatus('password', 'NotValidated');
            }
        });
    }

    // Password input validation
    var validatePassword = function () {
        return (passwordMeter.getScore() === 100);
    }

    // Public functions
    return {
        // Initialization
        init: function () {
            // Elements
            form = document.querySelector('#kt_sign_up_form');
            submitButton = document.querySelector('#kt_sign_up_submit');
            passwordMeter = KTPasswordMeter.getInstance(form.querySelector('[data-kt-password-meter="true"]'));

            handleForm();
        }
    };
}();

// On document ready

KTUtil.onDOMContentLoaded(function () {
    KTSignupGeneral.init();
});