"use strict";


// Class definition
var KTModalNewTarget = function () {
    var submitButton;
    var cancelButton;
    var validator;
    var form;
    var modal;
    var modalEl;

    // Init form inputs
    var initForm = function () {
        // Due date. For more info, please visit the official plugin site: https://flatpickr.js.org/
        var startDate = $(form.querySelector('[name="start_date"]'));
        startDate.flatpickr({
            enableTime: false,
            dateFormat: "Y-m-d",
            /*%m/%d/%Y*/
        });

        var endDate = $(form.querySelector('[name="end_date"]'));
        endDate.flatpickr({
            enableTime: false,
            dateFormat: "Y-m-d",
        });

    }

    // Handle form validation and submittion
    var handleForm = function () {
        // Stepper custom navigation

        // Init form validation rules. For more info check the FormValidation plugin's official documentation:https://formvalidation.io/
        validator = FormValidation.formValidation(
            form, {
                fields: {
                    exhibition_title: {
                        validators: {
                            notEmpty: {
                                message: 'Exhibition title is required'
                            }
                        }
                    },
                    start_date: {
                        validators: {
                            notEmpty: {
                                message: 'Start date is required'
                            }
                        }
                    },
                    end_date: {
                        validators: {
                            notEmpty: {
                                message: 'End date is required'
                            }
                        }
                    },
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    bootstrap: new FormValidation.plugins.Bootstrap5({
                        rowSelector: '.fv-row',
                        eleInvalidClass: '',
                        eleValidClass: ''
                    })
                }
            }
        );

        // Action buttons
        submitButton.addEventListener('click', function (e) {
            e.preventDefault();

            // Validate form before submit
            if (validator) {
                validator.validate().then(function (status) {
                    console.log('validated!');

                    if (status == 'Valid') {
                        submitButton.setAttribute('data-kt-indicator', 'on');

                        // Disable button to avoid multiple click 
                        submitButton.disabled = true;

                        setTimeout(function () {
                            submitButton.removeAttribute('data-kt-indicator');

                            // Enable button
                            submitButton.disabled = false;

                            // Show success message. For more info check the plugin's official documentation: https://sweetalert2.github.io/
                            Swal.fire({
                                text: "Form has been successfully submitted!",
                                icon: "success",
                                buttonsStyling: false,
                                confirmButtonText: "Ok, got it!",
                                customClass: {
                                    confirmButton: "btn btn-primary"
                                }
                            }).then(function (result) {
                                if (result.isConfirmed) {
                                    modal.hide();
                                }
                            });
                            //let s = form.submit(); // Submit form
                            /***************************/
                            var xhr = new XMLHttpRequest();

                            xhr.addEventListener("readystatechange", function () {
                                // Only run if the request is complete
                                if (xhr.readyState !== 4) return;
                                // Process our return data
                                if (xhr.status >= 200 && xhr.status < 300) {
                                    var response = JSON.parse(xhr.responseText);
                                    window.location.href = "/web_app/teacher/student_selection/?q=" + response['resource_id'];
                                } else {
                                    console.log('error', xhr);
                                }
                            });

                            xhr.open("POST", "/web_app/assignment/create", true);
                            /*INSERT DATA*/
                            let formData = new FormData(); // creates an object, optionally fill from <form>
                            formData.append("exhibition_title ", form.elements['exhibition_title'].value); // appends a field
                            formData.append("start_date ", form.elements['start_date'].value); // appends a field
                            formData.append("end_date  ", form.elements['end_date'].value); // appends a field
                            formData.append("space_assign  ", form.elements['space_assign'].value); // appends a field
                            formData.append("message  ", form.elements['message'].value); // appends a field
                            formData.append("image", form.elements['image'].files[0]); // appends a field
                            xhr.send(formData);
                            /***************************/

                        }, 2000);
                    } else {
                        // Show error message.
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
            }
        });

        cancelButton.addEventListener('click', function (e) {
            e.preventDefault();

            Swal.fire({
                text: "Are you sure you would like to cancel?",
                icon: "warning",
                showCancelButton: true,
                buttonsStyling: false,
                confirmButtonText: "Yes, cancel it!",
                cancelButtonText: "No, return",
                customClass: {
                    confirmButton: "btn btn-primary",
                    cancelButton: "btn btn-active-light"
                }
            }).then(function (result) {
                if (result.value) {
                    form.reset(); // Reset form	
                    modal.hide(); // Hide modal				
                } else if (result.dismiss === 'cancel') {
                    Swal.fire({
                        text: "Your form has not been cancelled!.",
                        icon: "error",
                        buttonsStyling: false,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn btn-primary",
                        }
                    });
                }
            });
        });
    }

    return {
        // Public functions
        init: function () {
            // Elements
            modalEl = document.querySelector('#kt_modal_new_target');

            if (!modalEl) {
                return;
            }

            modal = new bootstrap.Modal(modalEl);

            form = document.querySelector('#kt_modal_new_target_form');
            submitButton = document.getElementById('kt_modal_new_target_submit');
            cancelButton = document.getElementById('kt_modal_new_target_cancel');

            initForm();
            handleForm();
        }
    };
}();

// On document ready
KTUtil.onDOMContentLoaded(function () {
    KTModalNewTarget.init();
});